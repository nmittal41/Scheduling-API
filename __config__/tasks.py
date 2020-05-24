__all__ = ['request_url_task']

from django.conf import settings

import requests

from .celery import app


@app.task
def request_url_task(url):
    try:
        res = requests.get(url)

        if settings.DEBUG:
            print(res.status_code)
            print(res.content)

        return True
    except Exception:
        return False
