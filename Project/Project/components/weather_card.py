import reflex as rx

def weather_card():
    return rx.el.div(        
        width="250px",
        height="250px",
        bg="white",
        border_radius="12px",
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
        p="4",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",        
    )
