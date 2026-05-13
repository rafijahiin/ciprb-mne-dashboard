from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tracker.models import FistulaCase
from mpdsr.models import MPDSREvent


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard_main')
    return render(request, 'dashboard/landing.html')


@login_required
def dashboard_main(request):
    # Data for Fistula Progress Ring
    fistula_operated = FistulaCase.objects.filter(
        referral_status='OPERATED').count()
    # fistula_total = FistulaCase.objects.all().count()
    # Simple goal representation for now
    fistula_goal = 100
    fistula_progress = (fistula_operated / fistula_goal *
                        100) if fistula_goal > 0 else 0

    # Data for MPDSR Heatmap / Bar Chart (Deaths by district)
    from django.db.models import Count
    mpdsr_districts = MPDSREvent.objects.values('district').annotate(
        death_count=Count('event_id')).order_by('-death_count')
    heatmap_labels = [item['district'] for item in mpdsr_districts]
    heatmap_data = [item['death_count'] for item in mpdsr_districts]

    # Data for MPDSR Data-to-Action Gap Status Gauge
    total_mpdsr = MPDSREvent.objects.count()
    implemented_mpdsr = MPDSREvent.objects.filter(
        action_status='IMPLEMENTED').count()
    action_gap_percent = (implemented_mpdsr / total_mpdsr *
                          100) if total_mpdsr > 0 else 0

    # Events for HTMX table
    mpdsr_events = MPDSREvent.objects.all().order_by('-event_id')

    context = {
        'fistula_operated': fistula_operated,
        'fistula_goal': fistula_goal,
        'fistula_progress': fistula_progress,
        'heatmap_labels': heatmap_labels,
        'heatmap_data': heatmap_data,
        'action_gap_percent': action_gap_percent,
        'mpdsr_events': mpdsr_events,
    }
    return render(request, 'dashboard/main.html', context)
