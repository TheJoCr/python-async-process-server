from starlette.routing import Route
from .handlers import *

routes = [
    Route('/health', check_health),
    Route('/process', start_process, methods=['POST']),
    Route('/blocking-process', run_process, methods=['POST']),
    Route('/process/{id}', get_process, methods=['GET']),
    Route('/log/{id}', watch_log, methods=['GET']),
]
