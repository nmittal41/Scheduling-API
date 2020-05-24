__all__ = ['ping_view', 'scheduler_view']

from datetime import datetime

from django.conf import settings
from django.http.response import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .tasks import request_url_task

validate_url = URLValidator()


def error_response(error, status_code=400):
    return JsonResponse(
        {'status': 'error', 'error': error},
        status=status_code
    )


def ping_view(request):
    """Check for running server"""
    return JsonResponse({'status': 'ok'})


def scheduler_view(request):
    from dateutil.parser import parse as dt_parser

    try:
        url, dt = request.GET['url'], request.GET['dt']
        if not (url and dt):
            raise KeyError

        validate_url(url)
        # dt = datetime.strptime(dt,  '%Y-%m-%dT%H:%M:%S%z')
        dt = dt_parser(dt)

        request_url_task.apply_async(args=[url], eta=dt)
        return JsonResponse({'status': 'ok', 'message': f'URL {url} will be requested at {dt} UTC.'})

    except KeyError:
        return error_response('url and dt must be provided in params. Either one or both missing.')

    except ValidationError:
        return error_response('url is not valid. Insure that it has protocol included.')

    # except ParserError:
    #     return error_response('dt is not valid. Insure that is in ISO 8601 format.')

    except Exception as err:
        if settings.DEBUG:
            print(err)

        return error_response('An unknown error occurred.', status_code=500)
