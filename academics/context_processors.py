from .services import get_current_session


def current_session(request):
    return {'current_session': get_current_session()}
