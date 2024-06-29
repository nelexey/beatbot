from .handlers import handle_new_query, handle_main_page

urls = [
    {'method': 'GET', 'path': '/', 'handler': handle_main_page},
    {'method': 'POST', 'path': '/new_query', 'handler': handle_new_query},
]
