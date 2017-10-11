"""
config.py

Configuration and settings
"""
import os


class Config(object):
    DEBUG = False
    TESTING = False
    PRODUCTION = False

    SUBSCRIBERS = 'hermes_subscribers'
    SUBSCRIPTIONS = 'hermes_subscriptions'
    LOG = 'hermes_log'

    DB_URL = os.environ.get("DB_URL", "http://dynamodb:8000")
    ROOT_URL = os.environ.get("MEERKAT_HERMES_ROOT", "/hermes")

    SENTRY_DNS = os.environ.get('SENTRY_DNS', '')

    SENDER = 'Notifications <notifications@emro.info>'
    CHARSET = 'UTF-8'
    FROM = 'Meerkat'

    API_KEY = "test-hermes"

    PUBLISH_RATE_LIMIT = int(os.environ.get("MESSAGE RATE LIMIT", "40"))
    CALL_TIMES = []

    NEXMO_PUBLIC_KEY = ''
    NEXMO_PRIVATE_KEY = ''

    ERROR_REPORTING = ['error-reporting']
    NOTIFY_DEV = ['notify-dev']

    GCM_API_URL = "https://gcm-http.googleapis.com/gcm/send"
    GCM_AUTHENTICATION_KEY = ''
    GCM_ALLOWED_TOPICS = ['/topics/demo']
    GCM_MOCK_RESPONSE_ONLY = 1


class Production(Config):
    PRODUCTION = True
    DB_URL = os.environ.get(
        "DB_URL",
        "https://dynamodb.eu-west-1.amazonaws.com"
    )
    GCM_MOCK_RESPONSE_ONLY = 0
    GCM_ALLOWED_TOPICS = [
        '/topics/demo',
        '/topics/jordan',
        '/topics/madagascar',
        '/topics/somalia',
        '/topics/somaliland',
        '/topics/puntland'
    ]


class Development(Config):
    DEBUG = True
    TESTING = True


class Testing(Config):
    TESTING = True
    API_KEY = ""
    SUBSCRIBERS = 'test_hermes_subscribers'
    SUBSCRIPTIONS = 'test_hermes_subscriptions'
    LOG = 'test_hermes_log'
    DB_URL = "https://dynamodb.eu-west-1.amazonaws.com"
    GCM_MOCK_RESPONSE_ONLY = 0