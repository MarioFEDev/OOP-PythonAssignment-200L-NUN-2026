"""
chat_state.py — State for the AI chat interface.

Manages the conversation history between the user and
their AI companion. Each message has a sender, text content,
and a timestamp.
"""

import os
import datetime
import reflex as rx
import google.generativeai as genai
from dotenv import load_dotenv

from Project.state.user_state import UserState
from Project.state.planner_state import PlannerState
from Project.state.weather_state import WeatherState

# Load env variables and configure Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


class ChatState(rx.State):
    """
    Manages the chat conversation with the AI companion.

    Attributes:
        messages: List of message dicts with "sender", "text", and "time" keys.
                  sender is either "user" or "buddy".
        current_input: The text currently typed in the input field.
        is_buddy_typing: Whether the buddy is currently "typing" a response.
    """

    # ---- Chat Messages ----
    # Empty by default
    messages: list[dict[str, str]] = []

    # ---- Input State ----
    current_input: str = ""
    is_buddy_typing: bool = False

    # ---- Quick Suggestion Chips ----
    quick_suggestions: list[str] = [
        "Plan my day",
        "Check weather",
        "Show tasks",
    ]

    # ---- Settings ----
    model_provider: str = "groq"

    # ---- Event Handlers ----

    @rx.event
    def set_model_provider(self, provider: str):
        """Switch between Gemini and Groq."""
        self.model_provider = provider

    @rx.event
    def set_input(self, value: str):
        """Update the current input text as the user types."""
        self.current_input = value

    @rx.event
    async def send_message(self):
        """
        Send the current input as a user message.
        Then fetch response from Gemini or Groq API.
        """
        # Don't send empty messages
        if self.current_input.strip() == "":
            return

        # Add the user's message
        now_str = datetime.datetime.now().strftime("%I:%M %p")
        user_message = {
            "sender": "user",
            "text": self.current_input,
            "time": now_str,
        }
        self.messages = self.messages + [user_message]

        # Clear the input field and show typing indicator
        user_input_text = self.current_input
        self.current_input = ""
        self.is_buddy_typing = True
        yield

        try:
            # Fetch context from other states
            user_state = await self.get_state(UserState)
            planner_state = await self.get_state(PlannerState)
            weather_state = await self.get_state(WeatherState)

            # Build system prompt
            companion_name = user_state.assistant_name
            personality = user_state.assistant_info.get("personality", "Helpful")
            user_name = user_state.user_name or "User"
            location = user_state.location_name
            weather = weather_state.current_condition
            temp = weather_state.current_temp

            tasks = []
            for t in planner_state.tasks:
                status = "Done" if t.get("is_done") == "true" else "Pending"
                tasks.append(f"- [ID: {t.get('id')}] {t.get('title')} ({t.get('time')}) [{status}]")
            
            tasks_str = "\\n".join(tasks) if tasks else "No tasks scheduled."

            system_instruction = f"""
You are {companion_name}, an AI companion. Your personality is: {personality}.
You are chatting with your friend {user_name}.
Current Location: {location}
Current Weather: {weather}, {temp}°C
Current Tasks:
{tasks_str}

You have the ability to manage the user's planner using the add_task, remove_task, and edit_task tools. Use them whenever the user asks to add, remove, or change a task. Note the IDs of tasks when editing or removing.
Keep your responses concise, friendly, and in-character. 
IMPORTANT: DO NOT use any markdown formatting, hashtags, asterisks, bold text, bullet points, or special tokens (e.g. <|start_header_id|>). Provide plain conversational text only.
"""

            import uuid
            import json

            if self.model_provider == "groq":
                groq_key = os.getenv("GROQ_API_KEY")
                if not groq_key:
                    raise ValueError("GROQ_API_KEY is not set in the .env file")
                
                from groq import AsyncGroq
                client = AsyncGroq(api_key=groq_key)
                
                # Format messages for Groq
                groq_messages = [{"role": "system", "content": system_instruction}]
                for msg in self.messages[:-1]:
                    role = "assistant" if msg["sender"] == "buddy" else "user"
                    groq_messages.append({"role": role, "content": msg["text"]})
                groq_messages.append({"role": "user", "content": user_input_text})
                
                tools = [{
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Add a new task to the user's daily planner.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "time": {"type": "string"},
                                "category": {"type": "string", "enum": ["work", "health", "errands", "personal"]},
                                "period": {"type": "string", "enum": ["morning", "afternoon", "evening"]}
                            },
                            "required": ["title", "time", "category", "period"]
                        }
                    }
                }, {
                    "type": "function",
                    "function": {
                        "name": "remove_task",
                        "description": "Remove a task from the user's daily planner.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "The ID of the task to remove."}
                            },
                            "required": ["task_id"]
                        }
                    }
                }, {
                    "type": "function",
                    "function": {
                        "name": "edit_task",
                        "description": "Edit an existing task in the user's daily planner.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "The ID of the task to edit."},
                                "title": {"type": "string"},
                                "time": {"type": "string"},
                                "category": {"type": "string", "enum": ["work", "health", "errands", "personal"]},
                                "period": {"type": "string", "enum": ["morning", "afternoon", "evening"]}
                            },
                            "required": ["task_id", "title", "time", "category", "period"]
                        }
                    }
                }]
                
                response = await client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=groq_messages,
                    tools=tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                
                if tool_calls:
                    groq_messages.append(response_message)
                    for tool_call in tool_calls:
                        if tool_call.function.name == "add_task":
                            args = json.loads(tool_call.function.arguments)
                            
                            title = args.get("title", "New Task")
                            time_val = args.get("time", "No time set")
                            category = args.get("category", "work")
                            period = args.get("period", "morning")
                            
                            if category not in ["work", "health", "errands", "personal"]:
                                category = "work"
                            if period not in ["morning", "afternoon", "evening"]:
                                period = "morning"

                            new_task = {
                                "id": uuid.uuid4().hex[:8],
                                "title": title,
                                "time": time_val,
                                "category": category,
                                "period": period,
                                "is_done": "false",
                            }
                            
                            planner_state.add_task_from_external(new_task)
                            
                            groq_messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": "add_task",
                                "content": json.dumps({"result": f"Success: Task '{title}' added."})
                            })
                        elif tool_call.function.name == "remove_task":
                            args = json.loads(tool_call.function.arguments)
                            task_id = args.get("task_id", "")
                            planner_state.remove_task_from_external(task_id)
                            groq_messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": "remove_task",
                                "content": json.dumps({"result": f"Success: Task '{task_id}' removed."})
                            })
                        elif tool_call.function.name == "edit_task":
                            args = json.loads(tool_call.function.arguments)
                            task_id = args.get("task_id", "")
                            title = args.get("title", "")
                            time_val = args.get("time", "")
                            category = args.get("category", "work")
                            period = args.get("period", "morning")
                            
                            if category not in ["work", "health", "errands", "personal"]:
                                category = "work"
                            if period not in ["morning", "afternoon", "evening"]:
                                period = "morning"
                                
                            planner_state.edit_task_from_external(task_id, title, time_val, category, period)
                            groq_messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": "edit_task",
                                "content": json.dumps({"result": f"Success: Task '{task_id}' edited."})
                            })
                            
                    second_response = await client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=groq_messages
                    )
                    reply_text = second_response.choices[0].message.content
                else:
                    reply_text = response_message.content

            else:
                # Gemini execution
                if not os.getenv("GEMINI_API_KEY"):
                    raise ValueError("GEMINI_API_KEY is not set in the .env file")
                    
                # Prepare history for Gemini
                history = []
                for msg in self.messages[:-1]:
                    role = "model" if msg["sender"] == "buddy" else "user"
                    history.append({
                        "role": role,
                        "parts": [msg["text"]]
                    })

                def add_task(title: str, time: str, category: str, period: str):
                    pass
                def remove_task(task_id: str):
                    pass
                def edit_task(task_id: str, title: str, time: str, category: str, period: str):
                    pass

                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=system_instruction,
                    tools=[add_task, remove_task, edit_task]
                )
                
                chat = model.start_chat(history=history)
                response = await chat.send_message_async(user_input_text)
                
                if getattr(response, "function_call", None) or (response.parts and getattr(response.parts[0], "function_call", None)):
                    fc = getattr(response, "function_call", None) or response.parts[0].function_call
                    if fc.name == "add_task":
                        try:
                            args = type(fc.args).to_dict(fc.args) if hasattr(type(fc.args), "to_dict") else dict(fc.args)
                        except Exception:
                            args = {k: v for k, v in fc.args.items()}
                            
                        title = args.get("title", "New Task")
                        time_val = args.get("time", "No time set")
                        category = args.get("category", "work")
                        period = args.get("period", "morning")
                        
                        if category not in ["work", "health", "errands", "personal"]:
                            category = "work"
                        if period not in ["morning", "afternoon", "evening"]:
                            period = "morning"

                        new_task = {
                            "id": uuid.uuid4().hex[:8],
                            "title": title,
                            "time": time_val,
                            "category": category,
                            "period": period,
                            "is_done": "false",
                        }
                        
                        planner_state.add_task_from_external(new_task)
                        
                        try:
                            part = genai.types.Part.from_function_response(
                                name="add_task",
                                response={"result": f"Success: Task '{title}' added."}
                            )
                        except AttributeError:
                            part = {"function_response": {"name": "add_task", "response": {"result": f"Success: Task '{title}' added."}}}

                        response = await chat.send_message_async(part)
                    elif fc.name == "remove_task":
                        try:
                            args = type(fc.args).to_dict(fc.args) if hasattr(type(fc.args), "to_dict") else dict(fc.args)
                        except Exception:
                            args = {k: v for k, v in fc.args.items()}
                        task_id = args.get("task_id", "")
                        planner_state.remove_task_from_external(task_id)
                        
                        try:
                            part = genai.types.Part.from_function_response(
                                name="remove_task",
                                response={"result": f"Success: Task '{task_id}' removed."}
                            )
                        except AttributeError:
                            part = {"function_response": {"name": "remove_task", "response": {"result": f"Success: Task '{task_id}' removed."}}}
                        response = await chat.send_message_async(part)
                    elif fc.name == "edit_task":
                        try:
                            args = type(fc.args).to_dict(fc.args) if hasattr(type(fc.args), "to_dict") else dict(fc.args)
                        except Exception:
                            args = {k: v for k, v in fc.args.items()}
                        task_id = args.get("task_id", "")
                        title = args.get("title", "")
                        time_val = args.get("time", "")
                        category = args.get("category", "work")
                        period = args.get("period", "morning")
                        
                        if category not in ["work", "health", "errands", "personal"]:
                            category = "work"
                        if period not in ["morning", "afternoon", "evening"]:
                            period = "morning"
                            
                        planner_state.edit_task_from_external(task_id, title, time_val, category, period)
                        
                        try:
                            part = genai.types.Part.from_function_response(
                                name="edit_task",
                                response={"result": f"Success: Task '{task_id}' edited."}
                            )
                        except AttributeError:
                            part = {"function_response": {"name": "edit_task", "response": {"result": f"Success: Task '{task_id}' edited."}}}
                        response = await chat.send_message_async(part)

                reply_text = response.text

        except Exception as e:
            reply_text = f"Oops, something went wrong: {str(e)}"

        # Add buddy response
        buddy_response = {
            "sender": "buddy",
            "text": reply_text,
            "time": datetime.datetime.now().strftime("%I:%M %p"),
        }
        self.messages = self.messages + [buddy_response]
        self.is_buddy_typing = False

    @rx.event
    def send_quick_suggestion(self, suggestion: str):
        """Send one of the quick suggestion chips as a message."""
        self.current_input = suggestion
        return ChatState.send_message
