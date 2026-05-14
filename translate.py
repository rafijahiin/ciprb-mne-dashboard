import re

file_path = 'locale/bn/LC_MESSAGES/django.po'
with open(file_path, 'r') as f:
    content = f.read()

translations = {
    "CIPRB M&E Dashboard": "সিআইপিআরবি এমএন্ডই ড্যাশবোর্ড",
    "Real-time Reporting Dashboard": "রিয়েল-টাইম রিপোর্টিং ড্যাশবোর্ড",
    "Fistula Surgery Targets": "ফিস্টুলা সার্জারি লক্ষ্যমাত্রা",
    "MPDSR Deaths by District": "জেলা ভিত্তিক এমপিডিএসআর মৃত্যু",
    "AI Newsletter": "এআই নিউজলেটার",
    "Generate Now": "এখনই তৈরি করুন",
    "Data-to-Action Gap": "ডাটা-টু-অ্যাকশন গ্যাপ",
    "Lagging Behind Districts": "পিছিয়ে পড়া জেলাগুলো",
    "Recent Day-to-Day Activities": "সাম্প্রতিক দৈনন্দিন কার্যক্রম",
    "MPDSR Action Tracking": "এমপিডিএসআর অ্যাকশন ট্র্যাকিং"
}

for en, bn in translations.items():
    content = re.sub(rf'msgid "{en}"\nmsgstr ""', f'msgid "{en}"\nmsgstr "{bn}"', content)

with open(file_path, 'w') as f:
    f.write(content)
