# school/context_processors.py
from .models import Notice, Gallery, Founder, HeadmasterMessage, AssistantHeadmasterMessage, Facility, Visitor
from django.utils import timezone
from datetime import timedelta

def notice_board(request):
    notices = Notice.objects.all()[:5]
    return {'notices': notices}

def gallery_images(request):
    gallery_images = Gallery.objects.all().order_by('-created_at')[:7]
    return {'gallery_images': gallery_images}

def school_context(request):
    return {
        "founders": Founder.objects.all(),
        "headmaster_message": HeadmasterMessage.objects.first(),
        "assistant_headmaster_message": AssistantHeadmasterMessage.objects.first(),
    }

def facility_titles(request):
    facilities = Facility.objects.filter(status=True).order_by('title')
    return {'facility_titles': facilities}

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
    return {'active_url': request.resolver_match.url_name}

# school/context_processors.py

def get_translations(request):
    """ইউজারের ভাষা অনুযায়ী ট্রান্সলেশন ডিকশনারি রিটার্ন করে"""
    
    # সেশন থেকে ভাষা নিন, ডিফল্ট বাংলা
    lang = request.session.get('language', 'bn')
    
    # সব ট্রান্সলেশন এখানে রাখুন
    translations = {
        'bn': {
            # Top menu keys
            'home': 'হোম',
            'committee_members': 'কমিটি সদস্যবৃন্দ',
            'teachers': 'শিক্ষকবৃন্দ',
            'result': 'ফলাফল',
            'photo_gallery': 'ফটো গ্যালারি',
            'admission': 'ভর্তি',
            
            # Main menu keys (UPPERCASE as used in template)
            'INTRODUCTION': 'পরিচিতি',
            'HISTORY': 'ইতিহাস',
            'MISSION_AND_VISION': 'মিশন ও ভিশন',
            'ACHIEVEMENT': 'অর্জন',
            'ACADEMIC': 'একাডেমিক',
            'STUDENT_LIST': 'শিক্ষার্থী তালিকা',
            'CLASS_ROUTINE': 'ক্লাস রুটিন',
            'SYLLABUS': 'সিলেবাস',
            'EXAM_ROUTINE': 'পরীক্ষার রুটিন',
            'RESULT': 'ফলাফল',
            'ADMISSION_INFORMATION': 'ভর্তি তথ্য',
            'ADMISSION_CIRCULAR': 'ভর্তি বিজ্ঞপ্তি',
            'PROSPECTUS': 'প্রসপেক্টাস',
            'ADMISSION_RESULT': 'ভর্তি ফলাফল',
            'FACILITIES': 'সুবিধাসমূহ',
            'BOARD_PERMISSION': 'বোর্ড অনুমতি',
            'ALUMNI_ASSOCIATION': 'পুরাতন শিক্ষার্থী সমিতি',
            'REGISTRATION': 'নিবন্ধন',
            'No_Facilities': 'কোন সুবিধা নেই',
            
            # Notice and messages
            'notices': 'নোটিশ',
            'No_notices_found': 'কোন নোটিশ পাওয়া যায়নি।',
            'MESSAGES_OF_HEADMASTER': 'প্রধান শিক্ষকের বার্তা',
            'MESSAGES_OF_ASSISTANT_HEADMASTER': 'সহকারী প্রধান শিক্ষকের বার্তা',
            'read_more': 'বিস্তারিত',
            'Our_Facebook_Page': 'আমাদের ফেসবুক পেজ',
            
            # Footer keys
            'Administration': 'প্রশাসন',
            'alumni': 'পুরাতন শিক্ষার্থী',
            'download': 'ডাউনলোড',
            'magazine': 'ম্যাগাজিন',
            'annual_Report': 'বার্ষিক প্রতিবেদন',
            'class_routine': 'ক্লাস রুটিন',
            'exam_routine': 'পরীক্ষার রুটিন',
            'academic_calendar': 'একাডেমিক ক্যালেন্ডার',
            'payment_portal': 'পেমেন্ট পোর্টাল',
            'job_vacancies': 'চাকরির শূন্যপদ',
            'important_links': 'গুরুত্বপূর্ণ লিংক',
            'CONTACT_WITH_US': 'যোগাযোগ করুন',
            'Phone_No': 'ফোন নম্বর',
            'Email': 'ইমেইল',
            
            # Visitor stats
            'website_visitors': 'ওয়েবসাইট দর্শক',
            'today_visitors': 'আজকের দর্শক',
            'Visitors_in_this_Week': 'এই সপ্তাহের দর্শক',
            'Visitors_in_this_Month': 'এই মাসের দর্শক',
            'Visitors_in_this_Year': 'এই বছরের দর্শক',
            'total_visitors': 'মোট দর্শক',
            'active_visitors': 'সক্রিয় দর্শক',

            'about_institute': 'প্রতিষ্ঠান সম্পর্কে',
            'teachers_staffs': 'শিক্ষক ও কর্মচারীবৃন্দ',
            'meritorious_students': 'মেধাবী শিক্ষার্থীরা',


            'comilla_education_board': 'কুমিল্লা শিক্ষা বোর্ড',
            'dshe': 'মাধ্যমিক ও উচ্চ শিক্ষা অধিদপ্তর (DSHE)',
            'shed': 'মাধ্যমিক ও উচ্চ শিক্ষা বিভাগ',
            'national_university': 'জাতীয় বিশ্ববিদ্যালয়',
            'back_to_achievements': 'অর্জন তালিকায় ফিরে যান',

            'for_more_details': 'আরও বিস্তারিত জানতে, ভিজিট করুন আমাদের',
            'profile': 'প্রোফাইল',


            'our_mission': 'আমাদের মিশন',
            'our_vision': 'আমাদের ভিশন',
            'mission_and_vision_title': 'মিশন ও ভিশন',

            'achievements_title': 'স্কুলের অর্জনসমূহ',
            'our_school_achievements': 'আমাদের স্কুলের অর্জনসমূহ',


            # bn ডিকশনারিতে (বাংলা)
            'student_list_title': 'শিক্ষার্থী তালিকা',
            'student_list': 'শিক্ষার্থী তালিকা',
            'all_classes': 'সব শ্রেণি',
            'all_genders': 'সব লিঙ্গ',
            'filter': 'ফিল্টার',
            'roll_no': 'রোল নং',
            'name': 'নাম',
            'class_label': 'শ্রেণি',
            'gender_label': 'লিঙ্গ',
            'photo_label': 'ছবি',
            'details_label': 'বিস্তারিত',
            'view': 'দেখুন',




            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'academic_report_card': 'একাডেমিক রিপোর্ট কার্ড',
            'name': 'নাম',
            'roll_number': 'রোল নম্বর',
            'class_label': 'শ্রেণি',
            'gender_label': 'লিঙ্গ',
            'guardian': 'অভিভাবক',
            'academic_year': 'একাডেমিক বছর',
            'exam_results': 'পরীক্ষার ফলাফল',
            'subject': 'বিষয়',
            'total_marks': 'মোট নম্বর',
            'marks_obtained': 'প্রাপ্ত নম্বর',
            'status': 'স্থিতি',
            'pass': 'পাস',
            'fail': 'ফেল',
            'class_teacher': 'শ্রেণি শিক্ষক',
            'head_teacher': 'প্রধান শিক্ষক',
            'print_result_card': 'রেজাল্ট কার্ড প্রিন্ট করুন',
            'no_records_found': 'এই একাডেমিক সময়ের জন্য কোনো রেকর্ড পাওয়া যায়নি।',
            'official_student_progress_report': 'অফিসিয়াল শিক্ষার্থী অগ্রগতি প্রতিবেদন',

            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'class_routine_title': 'ক্লাস রুটিন',
            'class_routine': 'ক্লাস রুটিন',
            'all_classes': 'সব শ্রেণি',
            'filter': 'ফিল্টার',
            'class_label': 'শ্রেণি',
            'day': 'দিন',
            'subject': 'বিষয়',
            'time': 'সময়',
            'teacher': 'শিক্ষক',
            'image_label': 'ছবি',
            'routine_image': 'রুটিন ছবি',
            'close': 'বন্ধ করুন',
            'no_class_routines_found': 'কোন ক্লাস রুটিন পাওয়া যায়নি।',


            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'syllabus_title': 'সিলেবাস',
            'syllabus': 'সিলেবাস',
            'all_classes': 'সব শ্রেণি',
            'filter': 'ফিল্টার',
            'syllabus_image': 'সিলেবাস ছবি',
            'no_image': 'কোন ছবি নেই',
            'no_syllabus_found': 'কোন সিলেবাস পাওয়া যায়নি।',

            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'exam_routine_title': 'পরীক্ষার রুটিন',
            'exam_routine': 'পরীক্ষার রুটিন',
            'all_classes': 'সব শ্রেণি',
            'filter': 'ফিল্টার',
            'exam_routine_image': 'পরীক্ষার রুটিন ছবি',
            'no_image': 'কোন ছবি নেই',
            'no_exam_routine_found': 'কোন পরীক্ষার রুটিন পাওয়া যায়নি।',

            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'examination_result_title': 'পরীক্ষার ফলাফল',
            'examination_result': 'পরীক্ষার ফলাফল',
            'class_label': 'শ্রেণি',
            'select_your_class': 'আপনার শ্রেণি নির্বাচন করুন',
            'year_label': 'সাল',
            'select_passing_year': 'পাসের সাল নির্বাচন করুন',
            'class_roll': 'শ্রেণি রোল',
            'enter_class_roll_number': 'আপনার শ্রেণি রোল নম্বর লিখুন',
            'view_result': 'ফলাফল দেখুন',
            'result_for_roll': 'ফলাফল',
            'sl': 'ক্রমিক নং',
            'name': 'নাম',
            'subject': 'বিষয়',
            'marks_obtained': 'প্রাপ্ত নম্বর',
            'total_marks': 'মোট নম্বর',
            'no_results_found': 'আপনার অনুসন্ধানকৃত মানদণ্ডে কোনো ফলাফল পাওয়া যায়নি।',


            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'admission_circulars_title': 'ভর্তি বিজ্ঞপ্তি',
            'admission_circulars': 'ভর্তি বিজ্ঞপ্তি',
            'class_label': 'শ্রেণি',
            'all_classes': 'সব শ্রেণি',
            'filter': 'ফিল্টার',
            'sl': 'ক্রমিক নং',
            'title': 'শিরোনাম',
            'date_label': 'তারিখ',
            'image_label': 'ছবি',
            'document_label': 'ডকুমেন্ট',
            'download': 'ডাউনলোড',
            'no_circulars_found': 'নির্বাচিত শ্রেণির জন্য কোনো বিজ্ঞপ্তি পাওয়া যায়নি।',

            
            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'admission_circulars_registry_title': 'ভর্তি বিজ্ঞপ্তি - অফিসিয়াল রেজিস্ট্রি',
            'class_selection': 'শ্রেণি নির্বাচন',
            'all_academic_classes': 'সব একাডেমিক শ্রেণি',
            'filter_records': 'রেকর্ড ফিল্টার করুন',
            'sl': 'ক্রমিক নং',
            'circular_title_and_date': 'বিজ্ঞপ্তির শিরোনাম ও তারিখ',
            'class_label': 'শ্রেণি',
            'preview': 'প্রিভিউ',
            'document': 'ডকুমেন্ট',
            'published': 'প্রকাশিত',
            'preview_image': 'প্রিভিউ ছবি',
            'not_available': 'N/A',
            'download_pdf': 'পিডিএফ ডাউনলোড করুন',
            'no_file': 'কোন ফাইল নেই',
            'no_circulars_found_official': 'এই নির্বাচনের জন্য কোন অফিসিয়াল বিজ্ঞপ্তি পাওয়া যায়নি।',

            
            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'official_portal': 'অফিসিয়াল পোর্টাল',
            'result_search_criteria': 'ফলাফল অনুসন্ধানের মানদণ্ড',
            'exam_track_number': 'পরীক্ষার ট্র্যাক নম্বর',
            'track_number_placeholder': 'যেমন: ২০২৪৫০০১',
            'select_class': 'শ্রেণি নির্বাচন করুন',
            'select_year': 'সাল নির্বাচন করুন',
            'search_result': 'ফলাফল অনুসন্ধান করুন',
            'result_details_for_track': 'ট্র্যাক আইডির জন্য ফলাফলের বিবরণ:',
            'applicant_name': 'আবেদনকারীর নাম',
            'exam_track': 'পরীক্ষার ট্র্যাক',
            'admission_status': 'ভর্তির অবস্থা',
            'no_results_found_message': 'আপনার মানদণ্ডের সাথে মিলে এমন কোনো ফলাফল পাওয়া যায়নি। অনুগ্রহ করে আপনার ট্র্যাক নম্বর এবং নির্বাচন যাচাই করুন।',

            
            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'no_image_available': 'কোন ছবি উপলব্ধ নেই',
            'title_label': 'শিরোনাম',
            'description_label': 'বিবরণ',
            'category_label': 'বিভাগ',
            'capacity_label': 'ধারণক্ষমতা',
            'location_label': 'অবস্থান',
            'status_label': 'স্থিতি',
            'created_at_label': 'তৈরির তারিখ',
            'updated_at_label': 'হালনাগাদের তারিখ',
            'back_to_facilities': 'সুবিধাসমূহে ফিরে যান',
            
            # bn ডিকশনারিতে যোগ করুন (বাংলা)
            'our_facilities_title': 'আমাদের সুবিধাসমূহ',
            'our_facilities': 'আমাদের সুবিধাসমূহ',
            'category_label': 'বিভাগ',
            'all_categories': 'সব বিভাগ',
            'filter': 'ফিল্টার',
            'sl': 'ক্রমিক নং',
            'title_label': 'শিরোনাম',
            'description_label': 'বিবরণ',
            'capacity_label': 'ধারণক্ষমতা',
            'location_label': 'অবস্থান',
            'status_label': 'স্থিতি',
            'image_label': 'ছবি',
            'action_label': 'অ্যাকশন',
            'view_details': 'বিস্তারিত দেখুন',
            'no_facilities_found': 'নির্বাচিত বিভাগের জন্য কোনো সুবিধা পাওয়া যায়নি।',
            
            # bn ডিকশনারিতে (বাংলা)
            'board_permission_title': 'বোর্ড অনুমতি',
            'board_permission': 'বোর্ড অনুমতি',
            'board_permission_description': 'এই পৃষ্ঠাটি সমস্ত বোর্ড সদস্য এবং তাদের অনুমতি প্রদর্শন করে।',
            'no_data_available': 'বর্তমানে কোনো তথ্য উপলব্ধ নেই।',

            # bn ডিকশনারিতে (বাংলা)
            'sl': 'ক্রমিক নং',
            'batch': 'ব্যাচ',
            'student_name': 'শিক্ষার্থীর নাম',
            'location': 'অবস্থান',
            'occupation': 'পেশা',
            'education': 'শিক্ষাগত যোগ্যতা',
            'actions': 'অ্যাকশন',

            # bn ডিকশনারিতে (বাংলা)
            'search_placeholder': '🔍 খুঁজুন...',

            
            # bn ডিকশনারিতে (বাংলা)
            'all_occupations': 'সব পেশা',
            'all_batches': 'সব ব্যাচ',
            'all_genders': 'সব লিঙ্গ',

            # bn ডিকশনারিতে (বাংলা)
            'filter': 'ফিল্টার',
            'reset': 'রিসেট',

            # bn ডিকশনারিতে (বাংলা)
            'top_news': 'শীর্ষ সংবাদ!',

            # bn ডিকশনারিতে (বাংলা)
            'faculty_profile': 'শিক্ষক প্রোফাইল',
            'directory': 'তালিকা',
            'faculty_portrait': 'শিক্ষকের প্রতিকৃতি',
            'department': 'বিভাগ',
            'education': 'শিক্ষাগত যোগ্যতা',
            'email_label': 'ইমেইল',
            'direct_line': 'সরাসরি ফোন',
            'default_department': 'বিজ্ঞান অনুষদ',
            'advanced_degree': 'উচ্চতর ডিগ্রি',
        },
        'en': {
            # Top menu keys
            'top_news': 'Top News!',
            'home': 'Home',
            'committee_members': 'Committee Members',
            'teachers': 'Teachers',
            'result': 'Result',
            'photo_gallery': 'Photo Gallery',
            'admission': 'Admission',
            
            # Main menu keys (UPPERCASE as used in template)
            'INTRODUCTION': 'INTRODUCTION',
            'HISTORY': 'HISTORY',
            'MISSION_AND_VISION': 'MISSION AND VISION',
            'ACHIEVEMENT': 'ACHIEVEMENT',
            'ACADEMIC': 'ACADEMIC',
            'STUDENT_LIST': 'STUDENT LIST',
            'CLASS_ROUTINE': 'CLASS ROUTINE',
            'SYLLABUS': 'SYLLABUS',
            'EXAM_ROUTINE': 'EXAM ROUTINE',
            'RESULT': 'RESULT',
            'ADMISSION_INFORMATION': 'ADMISSION INFORMATION',
            'ADMISSION_CIRCULAR': 'ADMISSION CIRCULAR',
            'PROSPECTUS': 'PROSPECTUS',
            'ADMISSION_RESULT': 'ADMISSION RESULT',
            'FACILITIES': 'FACILITIES',
            'BOARD_PERMISSION': 'BOARD PERMISSION',
            'ALUMNI_ASSOCIATION': 'ALUMNI ASSOCIATION',
            'REGISTRATION': 'REGISTRATION',
            'No_Facilities': 'No Facilities',
            
            # Notice and messages
            'notices': 'Notices',
            'No_notices_found': 'No notices found.',
            'MESSAGES_OF_HEADMASTER': 'MESSAGES OF HEADMASTER',
            'MESSAGES_OF_ASSISTANT_HEADMASTER': 'MESSAGES OF ASSISTANT HEADMASTER',
            'read_more': 'Read more',
            'Our_Facebook_Page': 'Our Facebook Page',
            
            # Footer keys
            'Administration': 'Administration',
            'alumni': 'Alumni',
            'download': 'Download',
            'magazine': 'Magazine',
            'annual_Report': 'Annual Report',
            'class_routine': 'Class Routine',
            'exam_routine': 'Exam Routine',
            'academic_calendar': 'Academic Calendar',
            'payment_portal': 'Payment Portal',
            'job_vacancies': 'Job Vacancies',
            'important_links': 'Important Links',
            'CONTACT_WITH_US': 'CONTACT WITH US',
            'Phone_No': 'Phone No',
            'Email': 'Email',
            
            # Visitor stats
            'website_visitors': 'Website Visitors',
            'today_visitors': 'Today Visitors',
            'Visitors_in_this_Week': 'Visitors in this Week',
            'Visitors_in_this_Month': 'Visitors in this Month',
            'Visitors_in_this_Year': 'Visitors in this Year',
            'total_visitors': 'Total Visitors',
            'active_visitors': 'Active Visitors',


            'about_institute': 'About Institute',
            'teachers_staffs': 'Teachers & Staffs',
            'meritorious_students': 'Meritorious Students',
            
            'comilla_education_board': 'Comilla Education Board',
            'dshe': 'Directorate of Secondary and Higher Education (DSHE)',
            'shed': 'Secondary and Higher Education Division',
            'national_university': 'National University',

            'back_to_achievements': 'Back to Achievements',
            'for_more_details': 'For more details, please visit our',
            'profile': 'Profile',

            'our_mission': 'Our Mission',
            'our_vision': 'Our Vision',
            'mission_and_vision_title': 'Mission & Vision',

            'achievements_title': 'School Achievements',
            'our_school_achievements': 'Our School Achievements',


            'student_list_title': 'Student List',
            'student_list': 'Student List',
            'all_classes': 'All Classes',
            'all_genders': 'All Genders',
            'filter': 'Filter',
            'roll_no': 'Roll No',
            'name': 'Name',
            'class_label': 'Class',
            'gender_label': 'Gender',
            'photo_label': 'Photo',
            'details_label': 'Details',
            'view': 'View',


            # en ডিকশনারিতে (ইংরেজি)
            'student_list_title': 'Student List',
            'student_list': 'Student List',
            'all_classes': 'All Classes',
            'all_genders': 'All Genders',
            'filter': 'Filter',
            'roll_no': 'Roll No',
            'name': 'Name',
            'class_label': 'Class',
            'gender_label': 'Gender',
            'photo_label': 'Photo',
            'details_label': 'Details',
            'view': 'View',




            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'academic_report_card': 'Academic Report Card',
            'name': 'Name',
            'roll_number': 'Roll Number',
            'class_label': 'Class',
            'gender_label': 'Gender',
            'guardian': 'Guardian',
            'academic_year': 'Academic Year',
            'exam_results': 'Exam Results',
            'subject': 'Subject',
            'total_marks': 'Total Marks',
            'marks_obtained': 'Marks Obtained',
            'status': 'Status',
            'pass': 'Pass',
            'fail': 'Fail',
            'class_teacher': 'Class Teacher',
            'head_teacher': 'Head Teacher',
            'print_result_card': 'Print Result Card',
            'no_records_found': 'No records found for this academic period.',
            'official_student_progress_report': 'Official Student Progress Report',


            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'class_routine_title': 'Class Routine',
            'class_routine': 'Class Routine',
            'all_classes': 'All Classes',
            'filter': 'Filter',
            'class_label': 'Class',
            'day': 'Day',
            'subject': 'Subject',
            'time': 'Time',
            'teacher': 'Teacher',
            'image_label': 'Image',
            'routine_image': 'Routine Image',
            'close': 'Close',
            'no_class_routines_found': 'No class routines found.',

            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'syllabus_title': 'Syllabus',
            'syllabus': 'Syllabus',
            'all_classes': 'All Classes',
            'filter': 'Filter',
            'syllabus_image': 'Syllabus Image',
            'no_image': 'No Image',
            'no_syllabus_found': 'No syllabus found.',

            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'exam_routine_title': 'Exam Routine',
            'exam_routine': 'Exam Routine',
            'all_classes': 'All Classes',
            'filter': 'Filter',
            'exam_routine_image': 'Exam Routine Image',
            'no_image': 'No Image',
            'no_exam_routine_found': 'No exam routine found.',


            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'examination_result_title': 'Examination Result',
            'examination_result': 'Examination Result',
            'class_label': 'Class',
            'select_your_class': 'Select Your Class',
            'year_label': 'Year',
            'select_passing_year': 'Select Passing Year',
            'class_roll': 'Class Roll',
            'enter_class_roll_number': 'Enter Your class roll number',
            'view_result': 'View Result',
            'result_for_roll': 'Result for Roll',
            'sl': 'SL',
            'name': 'Name',
            'subject': 'Subject',
            'marks_obtained': 'Marks Obtained',
            'total_marks': 'Total Marks',
            'no_results_found': 'No results found for the given criteria.',

            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'admission_circulars_title': 'Admission Circulars',
            'admission_circulars': 'Admission Circulars',
            'class_label': 'Class',
            'all_classes': 'All Classes',
            'filter': 'Filter',
            'sl': 'SL',
            'title': 'Title',
            'date_label': 'Date',
            'image_label': 'Image',
            'document_label': 'Document',
            'download': 'Download',
            'no_circulars_found': 'No circulars found for the selected class.',


            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'admission_circulars_registry_title': 'Admission Circulars - Official Registry',
            'class_selection': 'Class Selection',
            'all_academic_classes': 'All Academic Classes',
            'filter_records': 'Filter Records',
            'sl': 'SL',
            'circular_title_and_date': 'Circular Title & Date',
            'class_label': 'Class',
            'preview': 'Preview',
            'document': 'Document',
            'published': 'Published',
            'preview_image': 'Preview Image',
            'not_available': 'N/A',
            'download_pdf': 'Download PDF',
            'no_file': 'No File',
            'no_circulars_found_official': 'No official circulars found for this selection.',


            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'official_portal': 'Official Portal',
            'result_search_criteria': 'Result Search Criteria',
            'exam_track_number': 'Exam Track Number',
            'track_number_placeholder': 'e.g. 20245001',
            'select_class': 'Select Class',
            'select_year': 'Select Year',
            'search_result': 'Search Result',
            'result_details_for_track': 'Result details for Track ID:',
            'applicant_name': 'Applicant Name',
            'exam_track': 'Exam Track',
            'admission_status': 'Admission Status',
            'no_results_found_message': 'No results were found matching your criteria. Please double-check your track number and selection.',

            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'no_image_available': 'No image available',
            'title_label': 'Title',
            'description_label': 'Description',
            'category_label': 'Category',
            'capacity_label': 'Capacity',
            'location_label': 'Location',
            'status_label': 'Status',
            'created_at_label': 'Created At',
            'updated_at_label': 'Updated At',
            'back_to_facilities': 'Back to Facilities',
            

            # en ডিকশনারিতে যোগ করুন (ইংরেজি)
            'our_facilities_title': 'Our Facilities',
            'our_facilities': 'Our Facilities',
            'category_label': 'Category',
            'all_categories': 'All Categories',
            'filter': 'Filter',
            'sl': 'SL',
            'title_label': 'Title',
            'description_label': 'Description',
            'capacity_label': 'Capacity',
            'location_label': 'Location',
            'status_label': 'Status',
            'image_label': 'Image',
            'action_label': 'Action',
            'view_details': 'View Details',
            'no_facilities_found': 'No facilities found for the selected category.',
            
            # en ডিকশনারিতে (ইংরেজি)
            'board_permission_title': 'Board Permission',
            'board_permission': 'Board Permission',
            'board_permission_description': 'This page displays all board members and their permissions.',
            'no_data_available': 'No data available at the moment.',

            # en ডিকশনারিতে (ইংরেজি)
            'sl': 'SL',
            'batch': 'Batch',
            'student_name': 'Student Name',
            'location': 'Location',
            'occupation': 'Occupation',
            'education': 'Education',
            'actions': 'Actions',

            # en ডিকশনারিতে (ইংরেজি)
            'search_placeholder': '🔍 Search...',

            # en ডিকশনারিতে (ইংরেজি)
            'all_occupations': 'All Occupations',
            'all_batches': 'All Batches',
            'all_genders': 'All Genders',

            # en ডিকশনারিতে (ইংরেজি)
            'filter': 'Filter',
            'reset': 'Reset',

            
            # en ডিকশনারিতে (ইংরেজি)
            'faculty_profile': 'Faculty Profile',
            'directory': 'Directory',
            'faculty_portrait': 'Faculty portrait',
            'department': 'Department',
            'education': 'Education',
            'email_label': 'Email',
            'direct_line': 'Direct Line',
            'default_department': 'Faculty of Science',
            'advanced_degree': 'Advanced Degree',
        }
    }
    
    current_trans = translations.get(lang, translations['bn'])
    
    return {
        't': current_trans,
        'current_language': lang,
    }