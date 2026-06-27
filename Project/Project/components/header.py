import reflex as rx



class HeaderState(rx.State):
    is_logged_in: bool = False

def header(is_logged_in: bool = False):
    return rx.el.div(
        rx.text("weather app", color="black", font_size="24px", font_weight="bold",),  
        rx.el.div(
            
        )      
    )