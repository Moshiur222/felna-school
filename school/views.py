from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

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
    teachers = Teacher.objects.all().order_by('name')  # or any ordering you prefer

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


def gallery_view(request):
    gallery_list = Gallery.objects.all()
    paginator = Paginator(gallery_list, 12)  # 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gallery.html', {'page_obj': page_obj})




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
    teachers = Teacher.objects.filter(is_active=True).order_by('name')
    return render(request, 'teacher_list.html', {'teachers': teachers})


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



import os, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django_countries import countries
from .models import StudentRegistration, Village
from .utils import send_otp, verify_otp

def get_common_data():
    return {
        'villages': Village.objects.all(),
        'batch_years': [year for year in range(2000, datetime.datetime.now().year + 1)],
        'occupation_choices': [(1, 'কৃষক'), (2, 'চাকরি'), (3, 'ব্যবসা'), (4, 'ফ্রিল্যান্সার')],
        'education_choices' : [ (1, 'SSC'), (2, 'HSC'), (3, 'BSc'), (4, 'MSc'), (5, 'Phd')],
        'gender_choices': [(1, 'পুরুষ'), (2, 'মহিলা'), (3, 'অন্যান্য')],
        'maritalstatus_choices': [(1, 'অবিবাহিত'), (2, 'বিবাহিত'), (3, 'তালাকপ্রাপ্ত')],
        'is_whatsapp_choices': [(1, 'হ্যাঁ'), (2, 'না')],
        'countries': list(countries),
    }

def student_registration(request):
    context = get_common_data()
    
    if request.method == "POST":
        step = request.POST.get("step")

        # STEP 1: INITIAL SUBMISSION
        if not step:
            bd_no = request.POST.get("bangladesh_number", "").strip()
            if StudentRegistration.objects.filter(bd_no=bd_no).exists():
                messages.error(request, 'এই নম্বরটি ইতিমধ্যে নিবন্ধিত।')
                return redirect('student_registration')

            photo = request.FILES.get('student_photo')
            temp_path = None
            if photo:
                temp_path = default_storage.save(f"temp/{bd_no}_{photo.name}", ContentFile(photo.read()))

            request.session['pending_student'] = {
                'student_name': request.POST.get("student_name"),
                'gender': int(request.POST.get("gender") or 1),
                'marrital_status': int(request.POST.get("marital_status") or 1),
                'is_whatsapp': int(request.POST.get("is_whatsapp_bd") or 1),
                'batch': int(request.POST.get("batch") or 2024),
                'village_id': int(request.POST.get("village")),
                'current_location': request.POST.get("current_location"),
                'bd_no': bd_no,
                'abroad_no': request.POST.get("abroad_number"),
                'occupation': int(request.POST.get("occupation") or 1),
                'last_edu': int(request.POST.get("last_edu") or 1),
                'temp_photo_path': temp_path
            }
            request.session['pending_phone'] = bd_no
            
            success, result = send_otp(bd_no)
            if success:
                context['show_otp_form'] = True
                context['phone_number'] = bd_no
                return render(request, 'student_registration.html', context)
            else:
                messages.error(request, result)
                return redirect('student_registration')

        # STEP 2: VERIFY OTP
        elif step == "verify_otp":
            phone = request.session.get('pending_phone')
            data = request.session.get('pending_student')
            success, msg = verify_otp(phone, request.POST.get("otp_code"))
            
            if success:
                village = Village.objects.get(id=data['village_id'])
                student = StudentRegistration.objects.create(
                    student_name=data['student_name'], gender=data['gender'],
                    marrital_status=data['marrital_status'], is_whatsapp=data['is_whatsapp'],
                    batch=data['batch'], village=village, current_location=data['current_location'],
                    bd_no=data['bd_no'], abroad_no=data['abroad_no'],
                    occupation=data['occupation'], last_edu=data['last_edu'], is_verified=True
                )
                if data.get('temp_photo_path'):
                    with default_storage.open(data['temp_photo_path'], 'rb') as f:
                        student.student_photo.save(os.path.basename(data['temp_photo_path']), ContentFile(f.read()))
                    default_storage.delete(data['temp_photo_path'])
                
                request.session.flush()
                messages.success(request, 'নিবন্ধন সফল হয়েছে!')
                return redirect('student_registration')
            else:
                messages.error(request, msg)
                context['show_otp_form'] = True
                context['phone_number'] = phone
                return render(request, 'student_registration.html', context)
                
        # STEP 3: RESEND
        elif step == "resend_otp":
            phone = request.session.get('pending_phone')
            success, msg = send_otp(phone)
            if success: messages.success(request, "নতুন ওটিপি পাঠানো হয়েছে।")
            else: messages.error(request, msg)
            context['show_otp_form'] = True
            context['phone_number'] = phone
            return render(request, 'student_registration.html', context)
        
        elif step == 'change_number':
            new_phone = request.POST.get('new_phone_number')
            # ফোন নম্বর ক্লিন করা (প্রথম ০ বাদ দেওয়া বা রাখা আপনার সিস্টেম অনুযায়ী)
            if new_phone:
                request.session['student_phone'] = new_phone # সেশনে আপডেট করা
                # এখানে নতুন করে ওটিপি জেনারেট করে এসএমএস পাঠানোর কোড লিখুন
                send_otp(new_phone) 
                messages.success(request, f"নম্বর পরিবর্তন করে {new_phone}-এ ওটিপি পাঠানো হয়েছে।")
                return redirect('student_registration')

    return render(request, 'student_registration.html', context)

from django.shortcuts import render
from .models import StudentRegistration

def registration_students_list(request):
    """Display list of registered students with filters and search"""
    students = StudentRegistration.objects.all().order_by('batch', 'student_name')
    
    # 1. Get filter parameters from the GET request
    selected_batch = request.GET.get('batch', '')
    selected_gender = request.GET.get('gender', '')
    selected_occupation = request.GET.get('occupation', '')
    selected_name = request.GET.get('student_name', '').strip()
    
    # 2. Apply Backend Filters (These happen before the page loads)
    if selected_batch:
        students = students.filter(batch=selected_batch)
    if selected_gender:
        students = students.filter(gender=selected_gender)
    if selected_occupation:
        students = students.filter(occupation=selected_occupation)
  

    # 3. Prepare Dropdown Choices
    batch_choices = StudentRegistration.objects.values_list('batch', flat=True).distinct().order_by('-batch')
    gender_choices = StudentRegistration.GENDER_CHOICES
    occupation_choices = StudentRegistration.OCCUPATION_CHOICES # Ensure this exists in your Model
    
    context = {
        'students': students,
        'batch_choices': batch_choices,
        'gender_choices': gender_choices,
        'occupation_choices': occupation_choices, # Added this
        'selected_batch': selected_batch,
        'selected_gender': selected_gender,
        'selected_occupation': selected_occupation, # Added this
        'selected_name': selected_name,
        'total_students': students.count(),
    }
    return render(request, 'registration_students_list.html', context)

def registration_student_detail(request, id):
    student = get_object_or_404(StudentRegistration, id=id)
    context = {
        'student': student
    }
    return render(request, 'registration_students_details.html', context)