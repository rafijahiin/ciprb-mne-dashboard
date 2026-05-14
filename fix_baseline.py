with open('baseline/views.py', 'r') as f:
    content = f.read()

content = content.replace("expected_secret = os.environ.get('KOBO_WEBHOOK_SECRET', 'test_secret')", """expected_secret = os.environ.get('KOBO_WEBHOOK_SECRET')
        if not expected_secret:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured("KOBO_WEBHOOK_SECRET environment variable is required.")""")

with open('baseline/views.py', 'w') as f:
    f.write(content)
