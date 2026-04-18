from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from .models import Notice
from .models import ExamResult
from .models import AdmissionResult
from .models import Gallery
from .models import OurHistory
from .models import Donor
from .models import *
from .models import Management
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Create your views here.



def home(request):
    # Active sliders
    sliders = Slider.objects.filter(is_active=True).order_by('order')
    
    # Welcome message (optional)
    welcome_message = WelcomeMessage.objects.first()

    # Teacher list
    teachers = Teacher.objects.all().order_by('id')  # or any ordering you prefer

    # Active students
    students = Student.objects.filter(is_active=True).order_by('class_name', 'roll_number')

    context = {
        'sliders': sliders,
        'welcome_message': welcome_message,
        'teachers': teachers,
        'students': students,  # added here
    }
    
    return render(request, 'index.html', context)


def contact(request):
    return render(request, "contact.html")


def notice_list(request):
    notices = Notice.objects.all()  # Already ordered by -date
    paginator = Paginator(notices, 10)  # 10 notices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notice.html', {'page_obj': page_obj})




def exam_result_view(request):
    results = None
    class_choices = ExamResult.CLASS_CHOICES

    # Get all years dynamically from existing ExamResult records
    years = ExamResult.objects.order_by('-year').values_list('year', flat=True).distinct()

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')
        year = request.POST.get('year')
        roll_number = request.POST.get('roll_number')

        # Start filtering
        results = ExamResult.objects.all()

        if class_name:
            results = results.filter(student__class_name=class_name)
        if section:
            results = results.filter(student__section=section)
        if year:
            results = results.filter(year=year)
        if roll_number:
            results = results.filter(student__roll_number=roll_number)

        # Optional: order results
        results = results.order_by('student__roll_number', 'subject')

    context = {
        'results': results,
        'years': years,
        'class_choices': class_choices,
    }

    return render(request, 'exam_result.html', context)


def admission_result_view(request):
    results = None
    class_choices = AdmissionResult.CLASS_CHOICES
    # Get distinct years from DB
    years = AdmissionResult.objects.order_by('-year').values_list('year', flat=True).distinct()

    if request.method == 'POST':
        exam_track_number = request.POST.get('exam_track_number')
        class_name = request.POST.get('class_name')
        year = request.POST.get('year')

        results = AdmissionResult.objects.filter(
            exam_track_number=exam_track_number,
            class_name=class_name,
            year=year
        )

    context = {
        'results': results,
        'class_choices': class_choices,
        'years': years
    }
    return render(request, 'admission_result.html', context)

from django.db.models import Count

# সব অ্যালবাম দেখানোর জন্য
def gallery_view(request):
    # প্রতিটি অ্যালবামের সাথে তার মধ্যে কয়টি ছবি আছে তা গণনা করা হচ্ছে
    albums = Album.objects.annotate(photo_count=Count('photos')).order_by('-id')
    return render(request, 'gallery.html', {'albums': albums})

# একটি নির্দিষ্ট অ্যালবামের ছবি দেখানোর জন্য
def album_detail_view(request, slug):
    album = get_object_or_404(Album, slug=slug)
    photos = album.photos.all().order_by('-created_at') # related_name="photos" ব্যবহার করে
    return render(request, 'album_detail.html', {'album': album, 'photos': photos})




def history_view(request):
    # get the latest history entry
    history = OurHistory.objects.first()
    return render(request, 'history.html', {'history': history})




def donor_list(request):
    donors = Donor.objects.all()  # Fetch all donors
    return render(request, 'donors.html', {'donors': donors})


# View to list all management members
def management_list(request):
    members = Management.objects.all()  # fetch all management entries
    context = {
        'members': members
    }
    return render(request, 'management_list.html', context)

# View to show a single management member detail (optional)
def management_detail(request, pk):
    member = get_object_or_404(Management, pk=pk)
    context = {
        'member': member
    }
    return render(request, 'management_detail.html', context)


def founder(request):
    founders = Founder.objects.all()
    return render (request,'founder.html',{'founders': founders})


def mv(request):
    mission_vision = MissionVision.objects.last()
    return render (request,'mv.html', {"mission_vision": mission_vision})

def profile(request):
    profile = SchoolProfile.objects.last()  # Only one profile record
    return render (request,'profile.html', {"profile": profile})
    
    
    
def teacher_list(request):
    """
    View to display all teachers with their details.
    """
    # ডাটাবেস থেকে শুধুমাত্র একটি কুয়েরিতে ডেটা আনা হচ্ছে
    teachers = Teacher.objects.filter(is_active=True).order_by('name')
    
    context = {
        'teachers': teachers,
        'title': 'Faculty Directory'
    }
    
    return render(request, 'teacher_list.html', context)


def founder_detail(request, pk):
    founder = get_object_or_404(Founder, pk=pk)
    return render(request, "founder_detail.html", {"founder": founder})

def headmaster_message_detail(request, pk):
    message = get_object_or_404(HeadmasterMessage, pk=pk)
    return render(request, "headmaster_message_detail.html", {"message": message})

def assistant_headmaster_message_detail(request, pk):
    message = get_object_or_404(AssistantHeadmasterMessage, pk=pk)
    return render(request, "assistant_headmaster_message_detail.html", {"message": message})

def teacher_detail(request, pk):
    """
    Display details of a single teacher.
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teacher_detail.html', {'teacher': teacher})


# Student List
def student_list(request):
    class_choices = Student.CLASS_CHOICES
    gender_choices = Student.GENDER_CHOICES

    selected_class = request.GET.get('class_name', '')
    selected_gender = request.GET.get('gender', '')

    students = Student.objects.filter(is_active=True)

    if selected_class:
        students = students.filter(class_name=selected_class)
    if selected_gender:
        students = students.filter(gender=selected_gender)

    students = students.order_by('class_name', 'roll_number')

    context = {
        'students': students,
        'class_choices': class_choices,
        'gender_choices': gender_choices,
        'selected_class': selected_class,
        'selected_gender': selected_gender,
    }
    return render(request, 'student_list.html', context)

# Student Detail
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    exam_results = student.exam_results.all().order_by('-year')
    context = {
        'student': student,
        'exam_results': exam_results
    }
    return render(request, 'student_detail.html', context)

# Class Routine List
def class_routine_list(request):
    selected_class = request.GET.get('class', '')
    
    routines = ClassRoutine.objects.filter()
    
    if selected_class:
        routines = routines.filter(class_name=selected_class)
    
    context = {
        'routines': routines,
        'class_choices': ClassRoutine.CLASS_CHOICES,
        'selected_class': selected_class,
    }
    
    return render(request, 'class_routine.html', context)

def class_routine_detail(request, pk):
    routine = get_object_or_404(ClassRoutine, pk=pk)
    return render(request, 'class_routine_detail.html', {'routine': routine})



def achievements_list(request):
    achievements = SchoolAchievement.objects.all().order_by('-year', '-date_awarded')
    context = {
        'achievements': achievements,
    }
    return render(request, 'achievements_list.html', context)


# Optional: view a single achievement detail
def achievement_detail(request, pk):
    achievement = get_object_or_404(SchoolAchievement, pk=pk)
    context = {
        'achievement': achievement,
    }
    return render(request, 'achievement_detail.html', context)


def syllabus_view(request):
    class_choices = Syllabus.CLASS_CHOICES
    selected_class = request.GET.get('class', '')

    if selected_class:
        syllabuses = Syllabus.objects.filter(class_name=selected_class)
    else:
        syllabuses = Syllabus.objects.all()

    context = {
        'syllabuses': syllabuses,
        'class_choices': class_choices,
        'selected_class': selected_class,
    }
    return render(request, 'syllabus.html', context)


def exam_routine_view(request):
    class_choices = ExamRoutine.CLASS_CHOICES
    selected_class = request.GET.get('class', '')

    if selected_class:
        routines = ExamRoutine.objects.filter(class_name=selected_class)
    else:
        routines = ExamRoutine.objects.all()

    context = {
        'routines': routines,
        'class_choices': class_choices,
        'selected_class': selected_class,
    }
    return render(request, 'exam_routine.html', context)


def admission_circular_list(request):
    class_choices = AdmissionCircular.CLASS_CHOICES
    selected_class = request.GET.get('class', '')

    # Filter circulars by selected class if provided
    if selected_class:
        circulars = AdmissionCircular.objects.filter(class_name=selected_class).order_by('-created_at')
    else:
        circulars = AdmissionCircular.objects.all().order_by('-created_at')

    context = {
        'circulars': circulars,
        'class_choices': class_choices,
        'selected_class': selected_class,
    }
    return render(request, 'admission_circular_list.html', context)

def prospectus_list(request):
    class_choices = Prospectus.CLASS_CHOICES
    selected_class = request.GET.get('class', '')

    # Filter by class if selected
    if selected_class:
        prospectuses = Prospectus.objects.filter(class_name=selected_class).order_by('-year')
    else:
        prospectuses = Prospectus.objects.all().order_by('-year')

    context = {
        'prospectuses': prospectuses,
        'class_choices': class_choices,
        'selected_class': selected_class,
    }
    return render(request, 'prospectus_list.html', context)


def facility_list(request):
    # Get all facilities
    facilities = Facility.objects.all().order_by('title')

    # Optional filters
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')

    if category_filter:
        facilities = facilities.filter(category=category_filter)
    
    if status_filter:
        facilities = facilities.filter(status=status_filter)

    # Pass unique categories and statuses for the filter dropdowns
    categories = Facility.objects.values_list('category', flat=True).distinct()
    statuses = Facility.objects.values_list('status', flat=True).distinct()

    context = {
        'facilities': facilities,
        'categories': categories,
        'statuses': statuses,
        'selected_category': category_filter,
        'selected_status': status_filter,
    }
    return render(request, 'facility_list.html', context)


def facility_detail(request, pk):
    # Get a single facility or 404
    facility = get_object_or_404(Facility, pk=pk)
    
    context = {
        'facility': facility
    }
    return render(request, 'facility_detail.html', context)


def board_permission(request):
    """
    Display all board members on the Board Permission page
    """
    
    return render(request, 'board_permission.html')

import os
import re
import datetime
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from school.models import StudentRegistration, Village
from django_countries import countries
from .utils import *

def get_common_data():
    return {
        'villages': Village.objects.all(),
        'batch_years': [(year) for year in range(2000, datetime.datetime.now().year)],
        'occupation_choices': StudentRegistration.OCCUPATION_CHOICES,
        'education_choices': StudentRegistration.EDUCATION_CHOICES,
        'gender_choices': StudentRegistration.GENDER_CHOICES,
        'maritalstatus_choices': StudentRegistration.MARITAL_STATUS_CHOICES,
        'is_whatsapp_bd_choices': StudentRegistration.IS_WHATSAPP_BD_CHOICES,
        'is_whatsapp_abroad_choices': StudentRegistration.IS_WHATSAPP_ABROAD_CHOICES,
        'is_no_hide_choices': StudentRegistration.NUMBER_HIDE_CHOICES,
        'countries': list(countries),
    }


def student_registration(request):
    context = get_common_data()
    
    if request.method == "POST":
        step = request.POST.get("step")
        
        # Step 1: Initial form submission - Send OTP (Phone or Email based on location)
        if not step or step == "":
            bd_no = request.POST.get("bangladesh_number", "").strip()
            email = request.POST.get("email", "").strip()
            current_location = request.POST.get("current_location", "").strip()
            
            # Check if current location is Bangladesh
            is_bangladesh = (current_location == 'BD' or current_location == 'bd')
            
            # For non-Bangladesh residents, email is required
            # For Bangladesh residents, email is NOT required
            if not is_bangladesh and not email:
                messages.error(request, 'বর্তমান অবস্থান বাংলাদেশ না হওয়ায় ইমেইল ঠিকানা প্রয়োজন')
                context['form_data'] = request.POST
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)
            
            # Check duplicate based on location type
            if is_bangladesh:
                # For BD residents: Check phone number duplication only
                if bd_no and StudentRegistration.objects.filter(bd_no=bd_no).exists():
                    messages.error(request, 'এই নম্বরটি ইতিমধ্যে নিবন্ধিত।')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
            else:
                # For non-BD residents: Check email duplication only
                if email and StudentRegistration.objects.filter(email=email).exists():
                    messages.error(request, 'এই ইমেইলটি ইতিমধ্যে নিবন্ধিত।')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)

            try:
                # Get form values
                is_whatsapp_bd_value = request.POST.get("is_whatsapp_bd")
                if not is_whatsapp_bd_value:
                    is_whatsapp_bd_value = 2
                else:
                    is_whatsapp_bd_value = int(is_whatsapp_bd_value)
                
                is_whatsapp_abroad_value = request.POST.get("is_whatsapp_abroad")
                if not is_whatsapp_abroad_value:
                    is_whatsapp_abroad_value = 2
                else:
                    is_whatsapp_abroad_value = int(is_whatsapp_abroad_value)
                
                is_no_hide_value = request.POST.get("is_no_hide")
                if not is_no_hide_value:
                    is_no_hide_value = 2
                else:
                    is_no_hide_value = int(is_no_hide_value)
                
                abroad_no = request.POST.get("abroad_number", "").strip()
                if not abroad_no:
                    abroad_no = None
                
                student_bio = request.POST.get("student_bio", "").strip()
                if not student_bio:
                    student_bio = None
                
                facebook_profile = request.POST.get("facebook_profile", "").strip()
                if not facebook_profile:
                    facebook_profile = None
                
                student_name = request.POST.get("student_name", "").strip()
                
                # Validate English only for student name
                if student_name and not re.match(r'^[A-Za-z\s\.\-]+$', student_name):
                    messages.error(request, 'শিক্ষার্থীর নাম শুধুমাত্র ইংরেজি অক্ষরে হতে হবে')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
                
                gender = request.POST.get("gender")
                marital_status = request.POST.get("marital_status")
                batch = request.POST.get("batch", "").strip()
                village_id = request.POST.get("village", "").strip()
                job_location = request.POST.get("job_location", "").strip()
                job_description = request.POST.get("job_description", "").strip()
                occupation = request.POST.get("occupation", "").strip()
                last_edu = request.POST.get("last_edu", "").strip()
                photo = request.FILES.get('student_photo')
                
                # Validation
                errors = []
                if not student_name:
                    errors.append("শিক্ষার্থীর নাম প্রয়োজন")
                elif not re.match(r'^[A-Za-z\s\.\-]+$', student_name):
                    errors.append("শুধুমাত্র ইংরেজি অক্ষর ব্যবহার করুন")
                
                if not gender:
                    errors.append("লিঙ্গ নির্বাচন করুন")
                
                if not marital_status:
                    errors.append("বৈবাহিক অবস্থা নির্বাচন করুন")
                if not batch:
                    errors.append("ব্যাচের বছর নির্বাচন করুন")
                if not village_id or village_id == "0":
                    errors.append("গ্রাম নির্বাচন করুন")
                if not current_location:
                    errors.append("বর্তমান অবস্থান নির্বাচন করুন")
                if not job_location:
                    errors.append("কর্মস্থলের দেশ নির্বাচন করুন")
                if not occupation:
                    errors.append("পেশা নির্বাচন করুন")
                if not last_edu:
                    errors.append("শিক্ষাগত যোগ্যতা নির্বাচন করুন")
                
                # Phone validation for BD residents
                if is_bangladesh:
                    if not bd_no:
                        errors.append("বাংলাদেশ নম্বর দিন")
                    elif not bd_no.startswith('01') or len(bd_no) < 10 or len(bd_no) > 11 or not bd_no.isdigit():
                        errors.append("সঠিক বাংলাদেশি নম্বর দিন (যেমন: 01712345678)")
                    if not request.POST.get("is_whatsapp_bd"):
                        errors.append("হোয়াটসঅ্যাপ নম্বর কিনা নির্বাচন করুন")
                else:
                    # Email validation for non-BD residents
                    if not email:
                        errors.append("ইমেইল ঠিকানা দিন")
                    elif not re.match(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', email):
                        errors.append("সঠিক ইমেইল ঠিকানা দিন")
                
                if not request.POST.get("is_no_hide"):
                    errors.append("নম্বর হাইড কিনা নির্বাচন করুন")
                if not photo:
                    errors.append("শিক্ষার্থীর ছবি আপলোড করুন")
                
                if errors:
                    for error in errors:
                        messages.error(request, error)
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
                
                student_data = {
                    'student_name': student_name,
                    'email': email, 
                    'student_bio': student_bio,
                    'facebook_profile': facebook_profile,
                    'gender': int(gender),
                    'marrital_status': int(marital_status),
                    'is_whatsapp_bd': is_whatsapp_bd_value,
                    'is_whatsapp_abroad': is_whatsapp_abroad_value,
                    'is_no_hide': is_no_hide_value,
                    'batch': int(batch),
                    'village_id': int(village_id),
                    'current_location': current_location,
                    'job_location': job_location,
                    'job_description': job_description,
                    'bd_no': bd_no,
                    'abroad_no': abroad_no,
                    'occupation': int(occupation),
                    'last_edu': int(last_edu),
                }
                    
            except (ValueError, TypeError) as e:
                messages.error(request, f'ডেটা সাবমিশনে সমস্যা: {str(e)}')
                context['form_data'] = request.POST
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)

            # Save photo temporarily
            temp_path = None
            if photo:
                temp_identifier = bd_no if is_bangladesh else email
                temp_path = default_storage.save(f"temp/{temp_identifier}_{photo.name}", ContentFile(photo.read()))

            request.session['pending_student'] = student_data
            request.session['pending_student']['temp_photo_path'] = temp_path
            
            # Send OTP based on location
            if is_bangladesh:
                # Send SMS OTP to phone (for BD residents)
                request.session['pending_destination'] = bd_no
                request.session['pending_otp_type'] = 'phone'
                success, result = send_otp(bd_no)
                if success:
                    context['show_otp_form'] = True
                    context['otp_destination'] = bd_no
                    context['otp_destination_type'] = 'ফোন নম্বর'
                    context['otp_type'] = 'phone'
                    messages.info(request, f'{bd_no} নম্বরে OTP পাঠানো হয়েছে।')
                    return render(request, 'student_registration.html', context)
                else:
                    messages.error(request, f'OTP পাঠাতে ব্যর্থ: {result}')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
            else:
                # Send Email OTP (for non-BD residents)
                request.session['pending_destination'] = email
                request.session['pending_otp_type'] = 'email'
                
                # Generate OTP
                otp_code = str(random.randint(100000, 999999))
                request.session['pending_otp_code'] = otp_code
                request.session['pending_otp_time'] = datetime.datetime.now().isoformat()
                
                # Send email
                try:
                    send_mail(
                        'আপনার OTP কোড - প্রাক্তন শিক্ষার্থী নিবন্ধন',
                        f'প্রিয় {student_name},\n\nআপনার OTP কোড: {otp_code}\n\nএই কোডটি ৫ মিনিটের জন্য বৈধ।\n\nধন্যবাদ।',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    context['show_otp_form'] = True
                    context['otp_destination'] = email
                    context['otp_destination_type'] = 'ইমেইল'
                    context['otp_type'] = 'email'
                    messages.info(request, f'{email} ইমেইলে OTP পাঠানো হয়েছে।')
                    return render(request, 'student_registration.html', context)
                except Exception as e:
                    messages.error(request, f'ইমেইল পাঠাতে ব্যর্থ: {str(e)}')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)

        # Step 2: Verify OTP
        elif step == "verify_otp":
            destination = request.session.get('pending_destination')
            otp_type = request.session.get('pending_otp_type', 'phone')
            data = request.session.get('pending_student')
            
            if not destination or not data:
                messages.error(request, 'সেশন এক্সপায়ার্ড হয়েছে। আবার চেষ্টা করুন।')
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)
            
            entered_otp = request.POST.get("otp_code", "")
            is_valid = False
            
            if otp_type == 'phone':
                # Verify phone OTP
                success, msg = verify_otp(destination, entered_otp)
                is_valid = success
                if not is_valid:
                    messages.error(request, msg)
            else:
                # Verify email OTP
                saved_otp = request.session.get('pending_otp_code')
                otp_time_str = request.session.get('pending_otp_time')
                
                if saved_otp and entered_otp == saved_otp:
                    # Check if OTP is not expired (5 minutes)
                    if otp_time_str:
                        otp_time = datetime.datetime.fromisoformat(otp_time_str)
                        if datetime.datetime.now() > otp_time + datetime.timedelta(minutes=5):
                            is_valid = False
                            messages.error(request, 'OTP-এর মেয়াদ শেষ হয়ে গেছে। আবার OTP পাঠান।')
                        else:
                            is_valid = True
                    else:
                        is_valid = True
                else:
                    messages.error(request, 'ভুল OTP। দয়া করে সঠিক কোড দিন।')
            
            if is_valid:
                try:
                    village = None
                    if data.get('village_id'):
                        village = Village.objects.get(id=data['village_id'])
                    
                    student = StudentRegistration.objects.create(
                        student_name=data['student_name'],
                        email=data.get('email'),
                        student_bio=data.get('student_bio'),
                        facebook_profile=data.get('facebook_profile'),
                        gender=data.get('gender'),
                        marrital_status=data.get('marrital_status'),
                        is_whatsapp_bd=data.get('is_whatsapp_bd', 2),
                        is_whatsapp_abroad=data.get('is_whatsapp_abroad', 2),
                        is_no_hide=data.get('is_no_hide', 2),
                        batch=data.get('batch'),
                        village=village,
                        current_location=data.get('current_location'),
                        job_location=data.get('job_location'),
                        job_description=data.get('job_description'),
                        bd_no=data.get('bd_no'),
                        abroad_no=data.get('abroad_no'),
                        occupation=data.get('occupation'),
                        last_edu=data.get('last_edu'),
                        is_verified=False
                    )
                    
                    if data.get('temp_photo_path'):
                        if default_storage.exists(data['temp_photo_path']):
                            with default_storage.open(data['temp_photo_path'], 'rb') as f:
                                student.student_photo.save(
                                    os.path.basename(data['temp_photo_path']), 
                                    ContentFile(f.read())
                                )
                            default_storage.delete(data['temp_photo_path'])
                    
                    # Clear session data
                    request.session.flush()
                    messages.success(request, 'আপনার নিবন্ধন সফল হয়েছে! ধন্যবাদ।')
                    return redirect('student_registration')
                    
                except Village.DoesNotExist:
                    messages.error(request, 'গ্রামটি পাওয়া যায়নি।')
                    context['show_otp_form'] = True
                    context['otp_destination'] = destination
                    context['otp_destination_type'] = 'ইমেইল' if otp_type == 'email' else 'ফোন নম্বর'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
                except Exception as e:
                    messages.error(request, f'নিবন্ধন সংরক্ষণে সমস্যা: {str(e)}')
                    context['show_otp_form'] = True
                    context['otp_destination'] = destination
                    context['otp_destination_type'] = 'ইমেইল' if otp_type == 'email' else 'ফোন নম্বর'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
            else:
                context['show_otp_form'] = True
                context['otp_destination'] = destination
                context['otp_destination_type'] = 'ইমেইল' if otp_type == 'email' else 'ফোন নম্বর'
                context['otp_type'] = otp_type
                return render(request, 'student_registration.html', context)
        
        # Step 3: Resend OTP
        elif step == "resend_otp":
            destination = request.session.get('pending_destination')
            otp_type = request.session.get('pending_otp_type', 'phone')
            
            if not destination:
                messages.error(request, 'সেশন এক্সপায়ার্ড হয়েছে।')
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)
            
            if otp_type == 'phone':
                success, msg = send_otp(destination)
                if success:
                    messages.success(request, "নতুন OTP পাঠানো হয়েছে।")
                else:
                    messages.error(request, msg)
            else:
                # Resend email OTP
                new_otp = str(random.randint(100000, 999999))
                request.session['pending_otp_code'] = new_otp
                request.session['pending_otp_time'] = datetime.datetime.now().isoformat()
                
                student_name = request.session.get('pending_student', {}).get('student_name', 'বন্ধু')
                
                try:
                    send_mail(
                        'আপনার নতুন OTP কোড - প্রাক্তন শিক্ষার্থী নিবন্ধন',
                        f'প্রিয় {student_name},\n\nআপনার নতুন OTP কোড: {new_otp}\n\nএই কোডটি ৫ মিনিটের জন্য বৈধ।\n\nধন্যবাদ।',
                        settings.DEFAULT_FROM_EMAIL,
                        [destination],
                        fail_silently=False,
                    )
                    messages.success(request, "নতুন OTP আপনার ইমেইলে পাঠানো হয়েছে।")
                except Exception as e:
                    messages.error(request, f'ইমেইল পাঠাতে ব্যর্থ: {str(e)}')
            
            context['show_otp_form'] = True
            context['otp_destination'] = destination
            context['otp_destination_type'] = 'ইমেইল' if otp_type == 'email' else 'ফোন নম্বর'
            context['otp_type'] = otp_type
            return render(request, 'student_registration.html', context)
        
        # Step 4: Change destination (phone or email)
        elif step == 'change_destination':
            new_destination = request.POST.get('new_destination', '').strip()
            otp_type = request.POST.get('otp_type', 'phone')
            
            if not new_destination:
                messages.error(request, "দয়া করে তথ্য দিন")
                context['show_otp_form'] = True
                context['otp_destination'] = request.session.get('pending_destination', '')
                context['otp_destination_type'] = 'ইমেইল' if otp_type == 'email' else 'ফোন নম্বর'
                context['otp_type'] = otp_type
                return render(request, 'student_registration.html', context)
            
            if otp_type == 'phone':
                # Validate phone number
                if len(new_destination) < 10 or len(new_destination) > 11:
                    messages.error(request, "সঠিক ১০-১১ অঙ্কের নম্বর দিন")
                    context['show_otp_form'] = True
                    context['otp_destination'] = request.session.get('pending_destination', '')
                    context['otp_destination_type'] = 'ফোন নম্বর'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
                
                if not new_destination.startswith('01') or not new_destination.isdigit():
                    messages.error(request, "সঠিক বাংলাদেশি নম্বর দিন (যেমন: 01xxxxxxxxx)")
                    context['show_otp_form'] = True
                    context['otp_destination'] = request.session.get('pending_destination', '')
                    context['otp_destination_type'] = 'ফোন নম্বর'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
                
                # Check if phone already registered
                if StudentRegistration.objects.filter(bd_no=new_destination).exists():
                    messages.error(request, "এই নম্বরটি ইতিমধ্যে নিবন্ধিত")
                    context['show_otp_form'] = True
                    context['otp_destination'] = request.session.get('pending_destination', '')
                    context['otp_destination_type'] = 'ফোন নম্বর'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
                
                # Update session
                request.session['pending_destination'] = new_destination
                if 'pending_student' in request.session:
                    pending = request.session['pending_student']
                    pending['bd_no'] = new_destination
                    request.session['pending_student'] = pending
                
                # Send new OTP
                success, msg = send_otp(new_destination)
                if success:
                    messages.success(request, f"নম্বর পরিবর্তন করে {new_destination} নম্বরে OTP পাঠানো হয়েছে।")
                else:
                    messages.error(request, msg)
                
            else:
                # Validate email
                if not re.match(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', new_destination):
                    messages.error(request, "সঠিক ইমেইল ঠিকানা দিন")
                    context['show_otp_form'] = True
                    context['otp_destination'] = request.session.get('pending_destination', '')
                    context['otp_destination_type'] = 'ইমেইল'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
                
                # Check if email already registered
                if StudentRegistration.objects.filter(email=new_destination).exists():
                    messages.error(request, "এই ইমেইলটি ইতিমধ্যে নিবন্ধিত")
                    context['show_otp_form'] = True
                    context['otp_destination'] = request.session.get('pending_destination', '')
                    context['otp_destination_type'] = 'ইমেইল'
                    context['otp_type'] = otp_type
                    return render(request, 'student_registration.html', context)
                
                # Update session
                request.session['pending_destination'] = new_destination
                if 'pending_student' in request.session:
                    pending = request.session['pending_student']
                    pending['email'] = new_destination
                    request.session['pending_student'] = pending
                
                # Generate and send new OTP
                new_otp = str(random.randint(100000, 999999))
                request.session['pending_otp_code'] = new_otp
                request.session['pending_otp_time'] = datetime.datetime.now().isoformat()
                
                student_name = request.session.get('pending_student', {}).get('student_name', 'বন্ধু')
                
                try:
                    send_mail(
                        'আপনার নতুন OTP কোড - প্রাক্তন শিক্ষার্থী নিবন্ধন',
                        f'প্রিয় {student_name},\n\nআপনার নতুন OTP কোড: {new_otp}\n\nএই কোডটি ৫ মিনিটের জন্য বৈধ।\n\nধন্যবাদ।',
                        settings.DEFAULT_FROM_EMAIL,
                        [new_destination],
                        fail_silently=False,
                    )
                    messages.success(request, f"ইমেইল পরিবর্তন করে {new_destination} ঠিকানায় OTP পাঠানো হয়েছে।")
                except Exception as e:
                    messages.error(request, f'ইমেইল পাঠাতে ব্যর্থ: {str(e)}')
            
            context['show_otp_form'] = True
            context['otp_destination'] = new_destination
            context['otp_destination_type'] = 'ইমেইল' if otp_type == 'email' else 'ফোন নম্বর'
            context['otp_type'] = otp_type
            return render(request, 'student_registration.html', context)
    
    # GET request - show registration form
    context['form_data'] = {}
    context['show_otp_form'] = False
    return render(request, 'student_registration.html', context)




def registration_students_list(request):
    students = StudentRegistration.objects.filter().order_by('batch', 'student_name')
    
    selected_batch = request.GET.get('batch', '')
    selected_gender = request.GET.get('gender', '')
    selected_occupation = request.GET.get('occupation', '')
    selected_name = request.GET.get('student_name', '').strip()
    
    if selected_batch and selected_batch.isdigit():
        students = students.filter(batch=int(selected_batch))
    if selected_gender and selected_gender.isdigit():
        students = students.filter(gender=int(selected_gender))
    if selected_occupation and selected_occupation.isdigit():
        students = students.filter(occupation=int(selected_occupation))
    if selected_name:
        students = students.filter(student_name__icontains=selected_name)
    
    batch_choices = StudentRegistration.objects.filter().values_list('batch', flat=True).distinct().order_by('-batch')
    
    context = {
        'students': students,
        'batch_choices': batch_choices,
        'gender_choices': StudentRegistration.GENDER_CHOICES,
        'occupation_choices': StudentRegistration.OCCUPATION_CHOICES,
        'selected_batch': selected_batch,
        'selected_gender': selected_gender,
        'selected_occupation': selected_occupation,
        'selected_name': selected_name,
        'total_students': students.count(),
    }
    return render(request, 'registration_students_list.html', context)


def registration_student_detail(request, slug):
    from django_countries import countries as country_list

    student = get_object_or_404(StudentRegistration, slug=slug)
    context = get_common_data()

    previous_student = StudentRegistration.objects.filter(id__lt=student.id).order_by('-id').first()
    next_student = StudentRegistration.objects.filter(id__gt=student.id).order_by('id').first()

    default_image = request.build_absolute_uri(static('home/images/default-meeting-og.jpg'))
    if student.student_photo and hasattr(student.student_photo, 'url'):
        meta_image = request.build_absolute_uri(student.student_photo.url)
    else:
        meta_image = default_image

    current_location_name = student.current_location.name if student.current_location else ""
    current_location_code = student.current_location.code if student.current_location else ""
    is_bangladesh = (current_location_code == 'BD')

    seos = [{
        'meta_title': f"{student.student_name} - Alumni Association Member of Felna High School",
        'meta_description': student.student_bio[:160] if student.student_bio else "",
        'meta_keywords': "alumni, registration, felna high school",
        'meta_url': request.build_absolute_uri(),
        'meta_image': meta_image,
    }]

    bd_no_display = "নাই"
    if student.bd_no:
        clean_number = ''.join(filter(str.isdigit, student.bd_no))
        if len(clean_number) == 11 and clean_number.startswith('01'):
            if student.is_no_hide == 2:
                bd_no_display = f"+880-{clean_number[1:3]}**-****{clean_number[-2:]}"
            else:
                bd_no_display = f"+880-{clean_number[1:5]}-{clean_number[5:]}"
        elif len(clean_number) == 10 and clean_number.startswith('1'):
            if student.is_no_hide == 2:
                bd_no_display = f"+880-{clean_number[:2]}**-****{clean_number[-2:]}"
            else:
                bd_no_display = f"+880-{clean_number[:4]}-{clean_number[4:]}"
        else:
            bd_no_display = student.bd_no

    education_choices = StudentRegistration.EDUCATION_CHOICES
    occupation_choices = StudentRegistration.OCCUPATION_CHOICES
    maritalstatus_choices = StudentRegistration.MARITAL_STATUS_CHOICES
    villages = Village.objects.all().order_by('name')

    context.update({
        'student': student,
        'bd_no_display': bd_no_display,
        'seos': seos,
        'previous_student': previous_student,
        'next_student': next_student,
        'current_location_name': current_location_name,
        'current_location_code': current_location_code,
        'is_bangladesh': is_bangladesh,
        'education_choices': education_choices,
        'occupation_choices': occupation_choices,
        'maritalstatus_choices': maritalstatus_choices,
        'villages': villages,
        # ✅ FIX: Pass countries list so template can use code as option value
        'countries': list(country_list),
    })

    return render(request, 'registration_students_details.html', context)


# ============================================================
# 2. update_student_profile  —  FIXED: accepts country CODE
# ============================================================
@require_http_methods(["POST"])
def update_student_profile(request):
    try:
        from django_countries import countries as country_list

        student_id = request.POST.get('student_id')
        student = get_object_or_404(StudentRegistration, id=student_id)

        # Build a name→code lookup as fallback
        name_to_code = {v: k for k, v in list(country_list)}
        all_codes = dict(country_list)  # code→name

        def resolve_country(value):
            """Accept either a 2-letter code (BD) or a full name (Bangladesh)."""
            if not value:
                return None
            value = value.strip()
            if len(value) == 2 and value.upper() in all_codes:
                return value.upper()
            if value in name_to_code:
                return name_to_code[value]
            # last resort: pass as-is (django-countries will validate)
            return value

        # Student name
        if 'student_name' in request.POST:
            name = request.POST.get('student_name', '').strip()
            if name:
                student.student_name = name

        # Marital status
        if 'marital_status' in request.POST:
            val = request.POST.get('marital_status', '').strip()
            if val:
                student.marrital_status = int(val)

        # Village
        if 'village' in request.POST:
            village_name = request.POST.get('village', '').strip()
            if village_name:
                village_obj, _ = Village.objects.get_or_create(name=village_name)
                student.village = village_obj

        # ✅ Current location — now receives code e.g. "BD"
        if 'current_location' in request.POST:
            code = resolve_country(request.POST.get('current_location', ''))
            if code:
                student.current_location = code

        # ✅ Job location — now receives code e.g. "US"
        if 'job_location' in request.POST:
            code = resolve_country(request.POST.get('job_location', ''))
            if code:
                student.job_location = code

        # Education
        if 'last_edu' in request.POST:
            val = request.POST.get('last_edu', '').strip()
            if val:
                student.last_edu = int(val)

        # Occupation
        if 'occupation' in request.POST:
            val = request.POST.get('occupation', '').strip()
            if val:
                student.occupation = int(val)

        # Text fields (allow empty string to clear)
        if 'job_description' in request.POST:
            student.job_description = request.POST.get('job_description', '')

        if 'facebook_profile' in request.POST:
            student.facebook_profile = request.POST.get('facebook_profile', '')

        if 'student_bio' in request.POST:
            student.student_bio = request.POST.get('student_bio', '')

        # Photo
        if 'student_photo' in request.FILES:
            student.student_photo = request.FILES['student_photo']

        student.save()

        return JsonResponse({'success': True, 'message': 'Profile updated successfully'})

    except Exception as e:
        import traceback
        print("update_student_profile error:", traceback.format_exc())
        return JsonResponse({'success': False, 'message': str(e)})


# ============================================================
# 3. send_otp_1  (no changes needed — kept for completeness)
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def send_otp_1(request):
    phone = request.POST.get("destination") or request.POST.get("phone")
    if not phone:
        return JsonResponse({"success": False, "message": "ফোন নম্বর দিন"})
    success, message = send_otp(phone)
    return JsonResponse({"success": success, "message": message})


# ============================================================
# 4. verify_otp_1  (no changes needed — kept for completeness)
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def verify_otp_1(request):
    phone = request.POST.get("destination") or request.POST.get("phone")
    otp = request.POST.get("otp")
    if not phone or not otp:
        return JsonResponse({"success": False, "message": "Phone and OTP are required"})
    success, message = verify_otp(phone, otp)
    return JsonResponse({"success": success, "message": message})


# ============================================================
# 5. send_otp_email  (no changes needed — kept for completeness)
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def send_otp_email(request):
    import time, secrets
    from django.core.mail import EmailMultiAlternatives
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    email = request.POST.get('destination')
    student_name = request.POST.get('student_name', 'Alumni')

    if not email:
        return JsonResponse({'success': False, 'message': 'ইমেইল ঠিকানা দিন'})

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'success': False, 'message': 'সঠিক ইমেইল ঠিকানা দিন'})

    otp = ''.join(secrets.choice('0123456789') for _ in range(6))

    request.session['email_otp'] = otp
    request.session['email_otp_time'] = time.time()
    request.session['email_address'] = email
    request.session.set_expiry(300)

    subject = "Your OTP Code - Felna High School Alumni"
    from_email = settings.DEFAULT_FROM_EMAIL
    text_content = (
        f"Your OTP Is: {otp}, Exp for 5 Min, Don't Share With Any One.\n"
        f"Alumni Association of Felna High School\nfelnahs.edu.bd\nFelnaTech.com"
    )
    html_content = f"""
    <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
    <div style="max-width:600px;margin:auto;background:#fff;padding:20px;border-radius:10px;">
        <h2 style="color:#2E86C1;text-align:center;">Felna High School Alumni Association</h2>
        <hr>
        <p>Dear {student_name},</p>
        <p>Your OTP verification code is:</p>
        <h1 style="color:#2E86C1;text-align:center;letter-spacing:3px;">{otp}</h1>
        <p style="text-align:center;color:red;">This OTP is valid for <b>5 minutes</b> only.</p>
        <p style="text-align:center;">Do not share this code with anyone.</p>
        <hr>
        <p style="text-align:center;">
            <b>Felna High School Alumni Association</b><br>
            <a href="https://felnahs.edu.bd">felnahs.edu.bd</a> |
            <a href="https://felnatech.com">FelnaTech.com</a>
        </p>
    </div></body></html>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({'success': True, 'message': 'OTP sent to your email'})
    except Exception as e:
        print("Email error:", e)
        return JsonResponse({'success': False, 'message': 'Email sending failed'})


# ============================================================
# 6. verify_otp_email  (no changes needed — kept for completeness)
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def verify_otp_email(request):
    import time

    entered_otp = request.POST.get('otp')
    stored_otp = request.session.get('email_otp')
    otp_time = request.session.get('email_otp_time', 0)
    email = request.session.get('email_address')

    if not stored_otp:
        return JsonResponse({'success': False, 'message': 'No OTP requested'})

    if time.time() - otp_time > 300:
        request.session.flush()
        return JsonResponse({'success': False, 'message': 'OTP expired'})

    if entered_otp == stored_otp:
        request.session.pop('email_otp', None)
        request.session.pop('email_otp_time', None)
        return JsonResponse({'success': True, 'message': 'OTP verified successfully', 'email': email})

    return JsonResponse({'success': False, 'message': 'Invalid OTP'})


# ============================================================
# 7. switch_language  (unchanged)
# ============================================================
@require_http_methods(["POST"])
def switch_language(request):
    next_url = request.POST.get('next', '/')
    language = request.POST.get('language', 'bn')
    if language in ['bn', 'en']:
        request.session['language'] = language
    return redirect(next_url)