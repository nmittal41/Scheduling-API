# Django Scheduling API


## Running
- Requirements: Python, Redis Server (running on default port)

Run server
```shell script
git clone https://github.com/nmittal41/Scheduling-API.git
cd Scheduling-API

# use virtualenv for sandboxing
pip install -r requirements.txt
./manage.py runserver
```

Run Celery
```shell script
celery worker -l info -A __config__
```

Example for requesting URL in your browser
```
http://127.0.0.1:8000/scheduler/?url=https://www.google.com&dt=2020-05-24T19:00:00
```


Testing
```shell script
./manage.py test
```

## API
### `/ping/`
- Response
```json
{
  "status": "ok"
}
```

### `/scheduler/`
#### GET
- Request
    - Params
        - `url`: URL to be requested. Make sure to include protocol.
        - `dt`: DateTime on which it will be requested. Make sure to be in ISO 8601 format.

- Response: `success`
```json
{
  "status": "ok",
  "message": "..."
}
```

- Response: `failure`
```json
{
  "status": "error",
  "error": "..."
}
```

NOTE: Do encode url before request
