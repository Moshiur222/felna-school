from .models import Notice
from .models import Gallery
from .models import Founder, HeadmasterMessage, AssistantHeadmasterMessage,Facility

def notice_board(request):
    notices = Notice.objects.all()[:5]  # Get latest 5 notices
    return {'notices': notices}


def gallery_images(request):
    """
    Returns a dictionary of context variables for the gallery.
    """
    # Fetch the latest 7 images from the Gallery model
    gallery_images = Gallery.objects.all().order_by('-created_at')[:7]
    return {'gallery_images': gallery_images}

def school_context(request):
    """
    Context processor to make Founder, HeadmasterMessage, and AssistantHeadmasterMessage
    available in all templates.
    """
    return {
        "founders": Founder.objects.all(),
        "headmaster_message": HeadmasterMessage.objects.first(),  # only one expected
        "assistant_headmaster_message": AssistantHeadmasterMessage.objects.first(),  # only one expected
    }


def facility_titles(request):
    # Get all facility titles
    facilities = Facility.objects.filter(status=True).order_by('title')
    return {
        'facility_titles': facilities
    }


from django.utils import timezone
from .models import Visitor
from datetime import timedelta

def visitor_stats(request):
    now = timezone.now()
    today = now.date()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)
    start_year = today.replace(month=1, day=1)
    
    visitors_today = Visitor.objects.filter(visited_at__date=today).count()
    visitors_week = Visitor.objects.filter(visited_at__date__gte=start_week).count()
    visitors_month = Visitor.objects.filter(visited_at__date__gte=start_month).count()
    visitors_year = Visitor.objects.filter(visited_at__date__gte=start_year).count()
    total_visitors = Visitor.objects.all().count()
    
    # Active visitors: sessions visited in last 5 minutes
    last_5min = now - timedelta(minutes=5)
    active_visitors = Visitor.objects.filter(visited_at__gte=last_5min).count()
    
    return {
        'visitors_today': visitors_today,
        'visitors_week': visitors_week,
        'visitors_month': visitors_month,
        'visitors_year': visitors_year,
        'total_visitors': total_visitors,
        'active_visitors': active_visitors
    }

def active_menu(request):
    return {
        'active_url': request.resolver_match.url_name
    }