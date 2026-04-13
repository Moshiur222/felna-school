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

# Create your views here.



def home(request):
    # Active sliders
    sliders = Slider.objects.filter(is_active=True).order_by('order')
    
    # Welcome message (optional)
    welcome_message = WelcomeMessage.objects.first()

    # Teacher list
    teachers = Teacher.objects.all().order_by('-id')  # or any ordering you prefer

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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from school.models import StudentRegistration, Village
from django_countries import countries
from .utils import *

def get_common_data():
    return {
        'villages': Village.objects.all(),
        'batch_years': [(year) for year in range(2000, datetime.datetime.now().year + 1)],
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
        
        if not step or step == "":
            bd_no = request.POST.get("bangladesh_number", "").strip()
            
            if StudentRegistration.objects.filter(bd_no=bd_no).exists():
                messages.error(request, 'এই নম্বরটি ইতিমধ্যে নিবন্ধিত।')
                context['form_data'] = request.POST
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)

            try:
                # ... existing code for getting values ...
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
                    messages.error(request, 'শিক্ষার্থীর নাম শুধুমাত্র ইংরেজি অক্ষরে হতে হবে (Only English letters allowed)')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
                
                gender = request.POST.get("gender")
                marital_status = request.POST.get("marital_status")
                batch = request.POST.get("batch", "").strip()
                village_id = request.POST.get("village", "").strip()
                current_location = request.POST.get("current_location", "").strip()
                job_location = request.POST.get("job_location", "").strip()
                job_description = request.POST.get("job_description", "").strip()  # নতুন ফিল্ড
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
                # job_description is optional, no validation needed
                if not occupation:
                    errors.append("পেশা নির্বাচন করুন")
                if not last_edu:
                    errors.append("শিক্ষাগত যোগ্যতা নির্বাচন করুন")
                if not bd_no:
                    errors.append("বাংলাদেশ নম্বর দিন")
                elif not bd_no.startswith('01') or len(bd_no) < 10 or len(bd_no) > 11 or not bd_no.isdigit():
                    errors.append("সঠিক বাংলাদেশি নম্বর দিন (যেমন: 01712345678)")
                if not request.POST.get("is_whatsapp_bd"):
                    errors.append("হোয়াটসঅ্যাপ নম্বর কিনা নির্বাচন করুন")
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
                    'job_description': job_description,  # নতুন ফিল্ড
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

            temp_path = None
            if photo:
                temp_path = default_storage.save(f"temp/{bd_no}_{photo.name}", ContentFile(photo.read()))

            request.session['pending_student'] = student_data
            request.session['pending_student']['temp_photo_path'] = temp_path
            request.session['pending_phone'] = bd_no
            
            # Check if current location is Bangladesh
            current_location_code = student_data.get('current_location', '')
            
            # Only send OTP if current location is Bangladesh (code 'BD')
            if current_location_code == 'BD':
                success, result = send_otp(bd_no)
                if success:
                    context['show_otp_form'] = True
                    context['phone_number'] = bd_no
                    messages.info(request, f'{bd_no} নম্বরে OTP পাঠানো হয়েছে।')
                    return render(request, 'student_registration.html', context)
                else:
                    messages.error(request, f'OTP পাঠাতে ব্যর্থ: {result}')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
            else:
                # If current location is not Bangladesh, save directly without OTP
                try:
                    village = None
                    if student_data.get('village_id'):
                        village = Village.objects.get(id=student_data['village_id'])
                    
                    student = StudentRegistration.objects.create(
                        student_name=student_data['student_name'],
                        student_bio=student_data.get('student_bio'),
                        facebook_profile=student_data.get('facebook_profile'),
                        gender=student_data.get('gender'),
                        marrital_status=student_data.get('marrital_status'),
                        is_whatsapp_bd=student_data.get('is_whatsapp_bd'),
                        is_whatsapp_abroad=student_data.get('is_whatsapp_abroad'),
                        is_no_hide=student_data.get('is_no_hide'),
                        batch=student_data.get('batch'),
                        village=village,
                        current_location=student_data.get('current_location'),
                        job_location=student_data.get('job_location'),
                        job_description=student_data.get('job_description'),  # নতুন ফিল্ড
                        bd_no=student_data['bd_no'],
                        abroad_no=student_data.get('abroad_no'),
                        occupation=student_data.get('occupation'),
                        last_edu=student_data.get('last_edu'),
                        is_verified=False
                    )
                    
                    if temp_path:
                        if default_storage.exists(temp_path):
                            with default_storage.open(temp_path, 'rb') as f:
                                student.student_photo.save(
                                    os.path.basename(temp_path), 
                                    ContentFile(f.read())
                                )
                            default_storage.delete(temp_path)
                    
                    request.session.flush()
                    messages.success(request, '🎉 আপনার নিবন্ধন সফল হয়েছে! ধন্যবাদ।')
                    return redirect('student_registration')
                    
                except Village.DoesNotExist:
                    messages.error(request, 'গ্রামটি পাওয়া যায়নি।')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)
                except Exception as e:
                    messages.error(request, f'নিবন্ধন সংরক্ষণে সমস্যা: {str(e)}')
                    context['form_data'] = request.POST
                    context['show_otp_form'] = False
                    return render(request, 'student_registration.html', context)

        elif step == "verify_otp":
            phone = request.session.get('pending_phone')
            data = request.session.get('pending_student')
            
            if not phone or not data:
                messages.error(request, 'সেশন এক্সপায়ার্ড হয়েছে। আবার চেষ্টা করুন।')
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)
                
            success, msg = verify_otp(phone, request.POST.get("otp_code"))
            
            if success:
                try:
                    village = None
                    if data.get('village_id'):
                        village = Village.objects.get(id=data['village_id'])
                    
                    student = StudentRegistration.objects.create(
                        student_name=data['student_name'],
                        student_bio=data.get('student_bio'),
                        facebook_profile=data.get('facebook_profile'),
                        gender=data.get('gender'),
                        marrital_status=data.get('marrital_status'),
                        is_whatsapp_bd=data.get('is_whatsapp_bd'),
                        is_whatsapp_abroad=data.get('is_whatsapp_abroad'),
                        is_no_hide=data.get('is_no_hide'),
                        batch=data.get('batch'),
                        village=village,
                        current_location=data.get('current_location'),
                        job_location=data.get('job_location'),
                        job_description=data.get('job_description'),  # নতুন ফিল্ড
                        bd_no=data['bd_no'],
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
                    
                    request.session.flush()
                    messages.success(request, '🎉 আপনার নিবন্ধন সফল হয়েছে! ধন্যবাদ।')
                    return redirect('student_registration')
                    
                except Village.DoesNotExist:
                    messages.error(request, 'গ্রামটি পাওয়া যায়নি।')
                    context['show_otp_form'] = True
                    context['phone_number'] = phone
                    return render(request, 'student_registration.html', context)
                except Exception as e:
                    messages.error(request, f'নিবন্ধন সংরক্ষণে সমস্যা: {str(e)}')
                    context['show_otp_form'] = True
                    context['phone_number'] = phone
                    return render(request, 'student_registration.html', context)
            else:
                messages.error(request, msg)
                context['show_otp_form'] = True
                context['phone_number'] = phone
                return render(request, 'student_registration.html', context)
        
        # ... rest of the code remains same for resend_otp and change_number ...
        
        elif step == "resend_otp":
            # ... existing resend_otp code ...
            phone = request.session.get('pending_phone')
            if not phone:
                messages.error(request, 'সেশন এক্সপায়ার্ড হয়েছে।')
                context['show_otp_form'] = False
                return render(request, 'student_registration.html', context)
                
            success, msg = send_otp(phone)
            if success:
                messages.success(request, "নতুন OTP পাঠানো হয়েছে।")
            else:
                messages.error(request, msg)
                
            context['show_otp_form'] = True
            context['phone_number'] = phone
            return render(request, 'student_registration.html', context)
        
        elif step == 'change_number':
            # ... existing change_number code ...
            new_phone = request.POST.get('new_phone_number', '').strip()
            
            if not new_phone:
                messages.error(request, "নম্বর দিন")
                context['show_otp_form'] = True
                context['phone_number'] = request.session.get('pending_phone', '')
                return render(request, 'student_registration.html', context)
            
            if len(new_phone) < 10 or len(new_phone) > 11:
                messages.error(request, "সঠিক ১০-১১ অঙ্কের নম্বর দিন")
                context['show_otp_form'] = True
                context['phone_number'] = request.session.get('pending_phone', '')
                return render(request, 'student_registration.html', context)
            
            if not new_phone.startswith('01') or not new_phone.isdigit():
                messages.error(request, "সঠিক বাংলাদেশি নম্বর দিন (যেমন: 01xxxxxxxxx)")
                context['show_otp_form'] = True
                context['phone_number'] = request.session.get('pending_phone', '')
                return render(request, 'student_registration.html', context)
            
            pending_phone = request.session.get('pending_phone', '')
            if new_phone != pending_phone and StudentRegistration.objects.filter(bd_no=new_phone).exists():
                messages.error(request, "এই নম্বরটি ইতিমধ্যে নিবন্ধিত")
                context['show_otp_form'] = True
                context['phone_number'] = pending_phone
                return render(request, 'student_registration.html', context)
            
            request.session['pending_phone'] = new_phone
            request.session.modified = True
            
            if 'pending_student' in request.session:
                pending = request.session['pending_student']
                pending['bd_no'] = new_phone
                request.session['pending_student'] = pending
            
            success, msg = send_otp(new_phone)
            
            if success:
                messages.success(request, f"নম্বর পরিবর্তন করে {new_phone} নম্বরে OTP পাঠানো হয়েছে।")
            else:
                messages.error(request, msg)
            
            context = get_common_data()
            context['show_otp_form'] = True
            context['phone_number'] = new_phone
            return render(request, 'student_registration.html', context)
    
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


from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static

def registration_student_detail(request, slug):
    student = get_object_or_404(StudentRegistration, slug=slug)
    context = get_common_data()
    # Previous student
    previous_student = StudentRegistration.objects.filter( id__lt=student.id ).order_by('-id').first()

    # Next student
    next_student = StudentRegistration.objects.filter( id__gt=student.id ).order_by('id').first()

    # -----------------------------
    # SAFE OG IMAGE HANDLING
    # -----------------------------
    default_image = request.build_absolute_uri(
        static('home/images/default-meeting-og.jpg')
    )

    if student.student_photo and hasattr(student.student_photo, 'url'):
        meta_image = request.build_absolute_uri(student.student_photo.url)
    else:
        meta_image = default_image

    # -----------------------------
    # SEO DATA
    # -----------------------------
    seos = [{
        'meta_title': f"{student.student_name} - Alumni Association Member of Felna High School",
        'meta_description': (
            student.student_bio[:160]
            if student.student_bio
            else ""
        ),
        'meta_keywords': "alumni, registration, felna high school", 
        'meta_url': request.build_absolute_uri(),
        'meta_image': meta_image,
    }]

    # -----------------------------
    # PHONE FORMAT
    # -----------------------------
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

    context.update({
        'student': student,
        'bd_no_display': bd_no_display,
        'seos': seos,
        'previous_student': previous_student,
        'next_student': next_student,
    })

    return render(request, 'registration_students_details.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_countries import countries
import json

@require_http_methods(["POST"])
def update_student_profile(request):
    try:
        student_id = request.POST.get('student_id')
        student = get_object_or_404(StudentRegistration, id=student_id)
        
        # Update student name
        if 'student_name' in request.POST:
            student.student_name = request.POST.get('student_name')
        
        # Update marital status (using integer values from model)
        if 'marital_status' in request.POST:
            marital_status_value = request.POST.get('marital_status')
            if marital_status_value and marital_status_value != '':
                student.marrital_status = int(marital_status_value)
        
        # Update village
        if 'village' in request.POST:
            village_name = request.POST.get('village')
            if village_name and village_name != '':
                village, created = Village.objects.get_or_create(name=village_name)
                student.village = village
            else:
                student.village = None
        
        # Update current location (country)
        if 'current_location' in request.POST:
            location_name = request.POST.get('current_location')
            if location_name and location_name != '':
                for code, name in countries:
                    if name == location_name:
                        student.current_location = code
                        break
            else:
                student.current_location = None
        
        # Update job location (country)
        if 'job_location' in request.POST:
            job_loc_name = request.POST.get('job_location')
            if job_loc_name and job_loc_name != '':
                for code, name in countries:
                    if name == job_loc_name:
                        student.job_location = code
                        break
            else:
                student.job_location = None
        
        # Update education
        if 'last_edu' in request.POST:
            last_edu_value = request.POST.get('last_edu')
            if last_edu_value and last_edu_value != '':
                student.last_edu = int(last_edu_value)
            else:
                student.last_edu = None
        
        # Update occupation
        if 'occupation' in request.POST:
            occupation_value = request.POST.get('occupation')
            if occupation_value and occupation_value != '':
                student.occupation = int(occupation_value)
            else:
                student.occupation = None
        
        # Update job description
        if 'job_description' in request.POST:
            student.job_description = request.POST.get('job_description')
        
        # Update Facebook profile
        if 'facebook_profile' in request.POST:
            student.facebook_profile = request.POST.get('facebook_profile')
        
        # Update student bio
        if 'student_bio' in request.POST:
            student.student_bio = request.POST.get('student_bio')
        
        # Update photo if provided
        if 'student_photo' in request.FILES:
            student.student_photo = request.FILES['student_photo']
        
        student.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Profile updated successfully'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        })
    
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def switch_language(request):
    next_url = request.POST.get('next', '/')
    language = request.POST.get('language', 'bn')
    
    if language in ['bn', 'en']:
        request.session['language'] = language
    
    return redirect(next_url)

from django.http import JsonResponse


def send_otp_1(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"})

    phone = request.POST.get("phone")

    success, message = send_otp(phone)

    return JsonResponse({
        "success": success,
        "message": message
    })


def verify_otp_1(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"})

    phone = request.POST.get("phone")
    otp = request.POST.get("otp")

    success, message = verify_otp(phone, otp)

    return JsonResponse({
        "success": success,
        "message": message
    })