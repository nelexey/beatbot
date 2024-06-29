from bot.web.handlers import handle_send_option, handle_send_beat, handle_payment

urls = [
    {'method': 'POST', 'path': '/option_done', 'handler': handle_send_option},
    {'method': 'POST', 'path': '/beat_done', 'handler': handle_send_beat},
    {'method': 'POST', 'path': '/handle_payment', 'handler': handle_payment},
]
