from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import MPDSREvent


@login_required
@require_POST
@csrf_exempt  # CSRF exempt for simplicity in this example with HTMX
def update_action_status(request, event_id):
    event = get_object_or_404(MPDSREvent, event_id=event_id)
    new_status = request.POST.get('action_status')

    # Check if the body contains the selected value directly from the select element
    # HTMX sends the value using the name of the select, if it has one.
    # We will grab the first key since HTMX sends the form data
    if not new_status and request.POST:
        new_status = list(request.POST.values())[0]

    if new_status in dict(MPDSREvent.ACTION_STATUS_CHOICES):
        event.action_status = new_status
        event.save()

    return render(request, 'dashboard/partials/status_dropdown.html', {'event': event})
