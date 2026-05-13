import os
from google import genai
from tracker.models import FistulaCase
from mpdsr.models import MPDSREvent


def generate_newsletter_narrative(month, year):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return "Error: GEMINI_API_KEY not configured."

    # Query the database
    # Just using count for dummy date logic
    total_deaths = MPDSREvent.objects.filter(event_id__isnull=False).count()
    pending_actions = MPDSREvent.objects.filter(
        action_status='PENDING').count()
    fistula_surgeries = FistulaCase.objects.filter(
        referral_status='OPERATED').count()

    prompt = f"""
    Write a 3-paragraph policy advocacy newsletter for month {month} and year {year}.
    The newsletter should highlight the "data-to-action" gap and project impact based on the following data:
    - Total MPDSR Deaths: {total_deaths}
    - Pending Corrective Actions: {pending_actions}
    - Successful Fistula Surgeries: {fistula_surgeries}

    The tone should be professional and encourage stakeholders to take action on the pending issues.
    """

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error generating narrative: {str(e)}"
