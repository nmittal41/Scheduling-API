from datetime import datetime

from django.test import TestCase, Client, override_settings
from django.urls import reverse


class PingTests(TestCase):
    url = reverse('ping')

    def test_status_ok(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'ok'}
        )


class SchedulerTests(TestCase):
    url = reverse('scheduler')

    def test_no_url(self):
        client = Client()
        response = client.get(self.url, {'dt': str(datetime.now().isoformat())})
        self.assertEqual(response.status_code, 400)

    def test_no_dt(self):
        client = Client()
        response = client.get(self.url, {'url': 'http://example.com'})
        self.assertEqual(response.status_code, 400)

    def test_url_not_valid(self):
        client = Client()
        response = client.get(self.url, {'url': 'example.com', 'dt': str(datetime.now().isoformat())})
        self.assertEqual(response.status_code, 400)

    def test_dt_not_valid(self):
        client = Client()
        response = client.get(self.url, {'url': 'example.com', 'dt': 'random'})
        self.assertEqual(response.status_code, 400)

    def test_success(self):
        client = Client()
        response = client.get(self.url, {'url': 'http://example.com', 'dt': str(datetime.now().isoformat())})
        self.assertEqual(response.status_code, 200)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_task(self):
        from .tasks import request_url_task
        self.assertTrue(request_url_task.delay('http://example.com'))
