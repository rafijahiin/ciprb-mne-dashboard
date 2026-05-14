from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tracker.models import FistulaCase
from mpdsr.models import MPDSREvent
from activities.models import ActivityLog
from django.db.models import Count, Q

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard_main')
    return render(request, 'dashboard/landing.html')

@login_required
def dashboard_main(request):
    # Data for Fistula Progress Ring
    fistula_operated = FistulaCase.objects.filter(
        referral_status='OPERATED').count()
    fistula_goal = 100
    fistula_progress = (fistula_operated / fistula_goal *
                        100) if fistula_goal > 0 else 0

    # Data for MPDSR Heatmap / Bar Chart (Deaths by district)
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

    # Lagging Behind Groups (Districts with most pending/stalled actions)
    lagging_districts = MPDSREvent.objects.values('district').annotate(
        lagging_count=Count('event_id', filter=Q(action_status__in=['PENDING', 'STALLED']))
    ).filter(lagging_count__gt=0).order_by('-lagging_count')[:5]

    # Recent Day-to-Day Activities
    recent_activities = ActivityLog.objects.all().order_by('-id')[:5]  # Fallback ordering

    context = {
        'fistula_operated': fistula_operated,
        'fistula_goal': fistula_goal,
        'fistula_progress': fistula_progress,
        'heatmap_labels': heatmap_labels,
        'heatmap_data': heatmap_data,
        'action_gap_percent': action_gap_percent,
        'mpdsr_events': mpdsr_events,
        'lagging_districts': lagging_districts,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard/main.html', context)
