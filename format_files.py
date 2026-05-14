with open('baseline/tests.py', 'r') as f:
    content = f.read()

content = content.replace("self.secret = 'test_secret'", "self.secret = 'test_secret'\n        os.environ['KOBO_WEBHOOK_SECRET'] = self.secret")

with open('baseline/tests.py', 'w') as f:
    f.write(content)
