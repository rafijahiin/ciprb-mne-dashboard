import os

files = ['dashboard/views.py', 'mpdsr/views.py', 'reports/views.py']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # remove excessive blank lines
    while '\n\n\n' in content:
        content = content.replace('\n\n\n', '\n\n')

    with open(file, 'w') as f:
        f.write(content)
