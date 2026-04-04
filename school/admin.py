from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from django.utils.html import strip_tags
from unfold.admin import ModelAdmin as UnfoldAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import *

# --- কাস্টম রিচ টেক্সট ফরম (সব টেক্সট ফিল্ডের জন্য) ---
class ProfessionalForm(forms.ModelForm):
    class Meta:
        widgets = {
            'message': WysiwygWidget(), 'content': WysiwygWidget(),
            'bio': WysiwygWidget(), 'description': WysiwygWidget(),
            'mission': WysiwygWidget(), 'vision': WysiwygWidget(),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

from django.urls import reverse # ফাইলের শুরুতে এটি ইম্পোর্ট করুন

@admin.register(Teacher)
class TeacherAdmin(UnfoldAdmin):
    form = ProfessionalForm
    # ১. লিস্ট ভিউ সেটিংস (অ্যাকশন বাটন যোগ করা হয়েছে)
    list_display = (
        'display_photo', 
        'display_teacher', 
        'subject', 
        'phone', 
        'display_status', 
        'action_buttons' # মডার্ন অ্যাকশন বাটন
    )
    
    list_filter = ('designation', 'subject', 'is_active')
    list_filter_sheet = True # সাইড স্লাইডিং ফিল্টার
    search_fields = ('name', 'subject', 'phone')
    ordering = ('name',)

    # ২. নামের নিচে ডেজিগনেশন (Modern Typography)
    @display(description="Teacher Info", header=True)
    def display_teacher(self, obj):
        return obj.name, obj.designation

    # ৩. গোল অবতার ছবি (Avatar)
    @display(description="Photo")
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid #6366f1;" />')
        return "—"

    # ৪. রঙিন স্ট্যাটাস ব্যাজ (Badge)
    @display(description="Status", label={True: "success", False: "danger"})
    def display_status(self, obj):
        return obj.is_active

    # ৫. মডার্ন অ্যাকশন বাটনস (Edit & Delete পাশাপাশি)
    @display(description="Actions")
    def action_buttons(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])
        
        return mark_safe(f"""
            <div style="display: flex; gap: 8px; align-items: center;">
                <!-- Manage Button (Indigo) -->
                <a href="{change_url}" title="Edit Info" style="background: #4f46e5; color: white; padding: 6px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);">
                    <span class="material-symbols-outlined" style="font-size: 16px;">edit_note</span>
                </a>
                
                <!-- Delete Icon (Red) -->
                <a href="{delete_url}" title="Delete Teacher" style="background: #ef4444; color: white; padding: 6px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2);">
                    <span class="material-symbols-outlined" style="font-size: 16px;">delete</span>
                </a>
            </div>
        """)

    # ৬. এডিট পেজ ক্লিন রাখার জন্য বাড়তি বাটন হাইড করা
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_delete': False,               # এডিট পেজে ডিলিট বাটন হাইড হবে
            'show_save_and_add_another': False, 
            'show_save_and_continue': False,    
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # ৭. আপনার আগের সেই সুন্দর ট্যাব লেআউট (Tabbed Layout)
    fieldsets = (
        ("Personal info", {
            "fields": (("name", "gender"), "photo", "bio", "join_date"),
            "classes": ["tab"]
        }),
        ("Professional info", {
            "fields": (("designation", "subject"), ("phone", "email")),
            "classes": ["tab"]
        }),
        ("Status", {
            "fields": ("is_active",),
            "classes": ["tab"]
        }),
    )

@admin.register(Student)
class StudentAdmin(UnfoldAdmin):
    list_display = ('display_photo', 'display_student', 'class_name', 'roll_number', 'display_status')
    list_filter = ('class_name', 'gender', 'is_active')
    list_filter_sheet = True
    
    @display(description="Student", header=True)
    def display_student(self, obj):
        return obj.name, f"Roll: {obj.roll_number}"

    @display(description="Photo")
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="width:40px; height:40px; border-radius:8px; object-fit:cover;" />')
        return "—"

    @display(description="Status", label={True: "success", False: "danger"})
    def display_status(self, obj):
        return obj.is_active

from django.urls import reverse # ফাইলের শুরুতে এটি নিশ্চিত করুন

@admin.register(AdmissionResult)
class AdmissionResultAdmin(UnfoldAdmin):
    # ১. লিস্ট ভিউ সেটিংস (Professional & Modern)
    list_display = (
        'exam_track_number', 
        'display_student_info', 
        'class_name', 
        'year', 
        'display_status', 
        'update_action' # শুধুমাত্র ম্যানেজ বাটন
    )
    
    list_filter = ('status', 'class_name', 'year')
    list_filter_sheet = True # সাইড ড্রয়ার ফিল্টার
    search_fields = ('exam_track_number', 'student_name')
    ordering = ('-year', 'class_name')
    compressed_fields = True # ফিল্ডগুলোর মাঝের গ্যাপ কমিয়ে স্ট্যান্ডার্ড লুক দেয়

    # ২. স্টুডেন্টের নামের নিচে আইডি (Modern Typography)
    @display(description="Applicant Details", header=True)
    def display_student_info(self, obj):
        return obj.student_name, f"Track ID: #{obj.exam_track_number}"

    # ৩. কালারফুল স্ট্যাটাস ব্যাজ (Passed, Failed, Waiting)
    @display(description="Result Status", label={
        "Passed": "success", 
        "Failed": "danger", 
        "Waiting": "warning"
    })
    def display_status(self, obj):
        return obj.status

    # ৪. শুধুমাত্র আপডেট বাটন (No Delete Action)
    @display(description="Action")
    def update_action(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        
        return mark_safe(f"""
            <a href="{url}" style="
                background: #4f46e5; 
                color: white; 
                padding: 6px 14px; 
                border-radius: 8px; 
                font-size: 11px; 
                font-weight: 700; 
                text-decoration: none; 
                display: inline-flex; 
                align-items: center; 
                gap: 6px;
                box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);
            ">
                <span class="material-symbols-outlined" style="font-size: 16px;">edit_note</span>
            </a>
        """)

    # ৫. আপডেট পেজের ফুটার বাটন হাইড করা (No Delete/Extra Buttons)
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_delete': False, 
            'show_save_and_add_another': False, 
            'show_save_and_continue': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # ডিলিট পারমিশন হার্ড-স্টপ (নিরাপত্তার জন্য)
    def has_delete_permission(self, request, obj=None):
        return False

    # ৬. সিঙ্গেল পেজ লেআউট (সব তথ্য এক সেকশনে)
    fieldsets = (
        ("Admission Record Details", {
            "fields": (
                ("student_name", "exam_track_number"), # এক লাইনে নাম ও আইডি
                ("class_name", "year"),                # এক লাইনে ক্লাস ও বছর
                "status",                             # নিচে রেজাল্ট স্ট্যাটাস
            ),
        }),
    )

@admin.register(ExamResult)
class ExamResultAdmin(UnfoldAdmin):
    list_display = ('student', 'year', 'subject', 'marks_obtained', 'total_marks')
    list_filter = ('year', 'subject')

# --- ৩. মিডিয়া ও স্লাইডার ---
from django.urls import reverse # ফাইলের শুরুতে এটি নিশ্চিত করুন

@admin.register(Slider)
class SliderAdmin(UnfoldAdmin):
    # ১. লিস্ট ভিউ সেটিংস (Modern & Professional)
    list_display = (
        'display_preview', 
        'display_headline', 
        'order', 
        'is_active', 
        'action_buttons' # এখানে এডিট এবং ডিলিট বাটন থাকবে
    )
    
    list_editable = ('order', 'is_active') 
    list_filter = ('is_active',)
    list_filter_sheet = True 
    search_fields = ('headline',)
    ordering = ('order',)

    # ২. ছবির মডার্ন প্রিভিউ (লিস্টের জন্য)
    @display(description="Slide View")
    def display_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width:110px; height:55px; border-radius:10px; object-fit:cover; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 2px solid #f3f4f6;" />')
        return "—"

    # ৩. হেডলাইন Typography
    @display(description="Slider Info", header=True)
    def display_headline(self, obj):
        return obj.headline, f""

    # ৪. মডার্ন অ্যাকশন বাটনস (Edit & Delete পাশাপাশি)
    @display(description="Actions")
    def action_buttons(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])
        
        return mark_safe(f"""
            <div style="display: flex; gap: 10px; align-items: center;">
                <!-- Edit Button (Indigo) -->
                <a href="{change_url}" title="Edit Slide" style="background: #4f46e5; color: white; padding: 6px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);">
                    <span class="material-symbols-outlined" style="font-size: 16px;">edit_note</span>
                </a>
                
                <!-- Delete Button (Red) -->
                <a href="{delete_url}" title="Delete Slide" style="background: #ef4444; color: white; padding: 6px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2);">
                    <span class="material-symbols-outlined" style="font-size: 16px;">delete</span> 
                </a>
            </div>
        """)

    # ৫. ফুটার বাটন কন্ট্রোল (এডিট পেজ ক্লিন রাখার জন্য)
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_delete': False, # এডিট পেজের নিচের ডিলিট বাটন হাইড থাকবে
            'show_save_and_add_another': False, 
            'show_save_and_continue': False,    
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # ৬. ডিলিট পারমিশন ট্রু (যাতে লিস্টের ডিলিট বাটন কাজ করে)
    def has_delete_permission(self, request, obj=None):
        return True

    # ৭. এডিট পেজ লেআউট (সবকিছু এক সেকশনে)
    fieldsets = (
        ("Main Content", {
            "fields": (
                ("headline", "order"), 
                "caption", 
                "image",
                "is_active",
                "active_slide_preview",
            ),
        }),
    )

    readonly_fields = ('active_slide_preview',)
    @display(description="Preview Now")
    def active_slide_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width: 100%; border-radius: 16px; box-shadow: 0 15px 25px rgba(0,0,0,0.1);" />')
        return "No image uploaded"



# --- ৪. অ্যাডমিনিস্ট্রেশন ও স্কুল প্রোফাইল ---
@admin.register(SchoolProfile)
class SchoolProfileAdmin(UnfoldAdmin):
    list_display = ('school_name', 'principal_name', 'eiin', 'contact_number')
    fieldsets = (
        ("Basic Info", {"fields": (("school_name", "eiin"), ("principal_name", "established_date")), "classes": ["tab"]}),
        ("Contact Details", {"fields": (("contact_number", "email"), ("address", "web_address")), "classes": ["tab"]}),
        ("Facilities", {"fields": ("class_room_info", "probable_admission_date"), "classes": ["tab"]}),
    )

@admin.register(Notice)
class NoticeAdmin(UnfoldAdmin):
    list_display = ('title', 'date', 'display_file')
    
    def display_file(self, obj):
        if obj.file:
            return mark_safe(f'<a href="{obj.file.url}" target="_blank">📄 View File</a>')
        return "No File"

# --- ৫. মেসেজ ও বার্তা (Headmaster/Asst. HM) ---
@admin.register(WelcomeMessage, HeadmasterMessage, AssistantHeadmasterMessage)
class MessageAdmin(UnfoldAdmin):
    form = ProfessionalForm
    list_display = ('title', 'display_photo', 'display_snippet')
    
    @display(description="Photo")
    def display_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" />') if obj.image else "—"

    def display_snippet(self, obj):
        return strip_tags(obj.message)[:50] + "..."

from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldAdmin
from unfold.decorators import display
from django.utils.safestring import mark_safe
from django.urls import reverse

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(UnfoldAdmin):
    # --- ১. লিস্ট ভিউ সেটিংস (Ultra Clean & Minimal) ---
    list_display = ('display_avatar', 'batch', 'display_name_v2', 'gender', 'village', 'action_button')
    list_filter = ('batch', 'village', 'gender', 'last_edu')
    list_filter_sheet = True
    search_fields = ('student_name', 'bd_no')
    compressed_fields = True 
    
    # --- ২. প্রফেশনাল পারমিশন (Read-Only Mode) ---
    def has_delete_permission(self, request, obj=None): return False

    def get_readonly_fields(self, request, obj=None):
        if obj: # এডিট মোডে সব ফিল্ড লক থাকবে
            return [f.name for f in self.model._meta.fields] + ['student_hero_card']
        return self.readonly_fields

    # --- ৩. লিস্ট ভিউ মেথডস ---

    @display(description="Member")
    def display_avatar(self, obj):
        photo = obj.student_photo.url if obj.student_photo else f"https://ui-avatars.com/api/?name={obj.student_name}&background=6366f1&color=fff"
        return mark_safe(f'<img src="{photo}" style="width:42px; height:42px; border-radius:12px; object-fit:cover; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" />')

    @display(description="Student Name", header=True)
    def display_name_v2(self, obj):
        # নামের নিচে ছোট করে আইডি দেখাবে
        return obj.student_name, f""

    @display(description="Action")
    def action_button(self, obj):
        url = reverse('admin:school_studentregistration_change', args=[obj.pk])
        return mark_safe(f'<a href="{url}" style="background: #f3f4f6; color: #4f46e5; padding: 6px 14px; border-radius: 10px; font-size: 12px; font-weight: 800; text-decoration: none; border: 1px solid #e5e7eb;">View</a>')

    # --- ৪. হিরো সেকশন (The Modern Profile Header) ---
    @display(description="")
    def student_hero_card(self, obj):
        if not obj.pk: return "New Student Registration"
        photo = obj.student_photo.url if obj.student_photo else f"https://ui-avatars.com/api/?name={obj.student_name}&background=fff&color=6366f1"
        
        return mark_safe(f"""
            <div style="background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%); padding: 45px; border-radius: 30px; color: white; position: relative; overflow: hidden; display: flex; align-items: center; gap: 35px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
                <!-- Profile Image -->
                <img src="{photo}" style="width: 140px; height: 140px; border-radius: 40px; border: 6px solid rgba(255,255,255,0.1); object-fit: cover; z-index: 2;" />
                
                <div style="z-index: 2;">
                    <h1 style="margin: 0; font-size: 38px; font-weight: 900; letter-spacing: -1.5px; line-height: 1.1;">{obj.student_name}</h1>
                    <p style="margin: 10px 0 20px 0; opacity: 0.8; font-size: 18px; font-weight: 500;">
                        Batch {obj.batch} <span style="margin: 0 10px; opacity: 0.3;">|</span> {obj.village} Resident
                    </p>
                    
                    <div style="display: flex; gap: 12px;">
                        <span style="background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 12px; font-size: 13px; font-weight: 600; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);">
                            {obj.get_last_edu_display()}
                        </span>
                        <span style="background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 12px; font-size: 13px; font-weight: 600; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);">
                            {obj.get_occupation_display()}
                        </span>
                    </div>
                </div>

                <!-- Abstract Decoration -->
                <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.05); border-radius: 50%;"></div>
                <div style="position: absolute; bottom: -20px; left: 40%; width: 100px; height: 100px; background: rgba(99, 102, 241, 0.2); border-radius: 50%; filter: blur(30px);"></div>
            </div>
        """)

    # --- ৫. হাইড ফুটার বার (Save/Delete Buttons) ---
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # --- ৬. মডার্ন ট্যাব লেআউট ---
    fieldsets = (
        (None, {
            "fields": ["student_hero_card"],
        }),
        ("Identity Details", {
            "fields": (
                ("student_name", "gender"), 
                ("batch", "marrital_status"), 
                "student_photo"
            ),
            "classes": ["tab"],
        }),
        ("Contact & Location", {
            "fields": (
                ("bd_no", "abroad_no"), 
                ("is_whatsapp", "village"), 
                "current_location"
            ),
            "classes": ["tab"],
        }),
        ("Career & Background", {
            "fields": (
                "occupation", "last_edu"
            ),
            "classes": ["tab"],
        }),
    )
@admin.register(Visitor)
class VisitorAdmin(UnfoldAdmin):
    list_display = ('ip_address', 'visited_at', 'user_agent')
    readonly_fields = ('ip_address', 'visited_at', 'user_agent', 'session_key')

from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.decorators import display

@admin.register(Gallery, OurHistory, MissionVision, Founder, Donor, Management, ClassRoutine, SchoolAchievement, Syllabus, ExamRoutine, AdmissionCircular, Prospectus, Facility, Village)
class GenericAdmin(UnfoldAdmin):
    form = ProfessionalForm # আপনার তৈরি করা রিচ টেক্সট ফরম
    list_per_page = 20
    list_filter_sheet = True

    # ১. লিস্ট ভিউতে মডার্ন অ্যাকশন বাটনগুলো (Manage ও Delete)
    @display(description="Actions")
    def action_buttons(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])
        
        return mark_safe(f"""
            <div style="display: flex; gap: 8px; align-items: center;">
                <a href="{change_url}" style="background: #4f46e5; color: white; padding: 6px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);">
                    <span class="material-symbols-outlined" style="font-size: 16px;">edit_note</span> 
                </a>
                <a href="{delete_url}" style="background: #ef4444; color: white; padding: 6px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2);">
                    <span class="material-symbols-outlined" style="font-size: 16px;">delete</span>
                </a>
            </div>
        """)

    list_display = ('__str__', 'action_buttons')

    # ২. আপডেট পেজের নিচের (Footer) বাড়তি বাটনগুলো হাইড করা
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_delete': False,               # ডিলিট বাটন হাইড হবে
            'show_save_and_add_another': False,   # সেভ অ্যান্ড অ্যাড অ্যানাদার হাইড হবে
            'show_save_and_continue': False,      # সেভ অ্যান্ড কন্টিনিউ হাইড হবে
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # ৩. নিরাপত্তাজনিত কারণে এডিট পেজের ভেতরে ডিলিট পারমিশন বন্ধ (লিস্টে বাটন কাজ করবে)
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # (নোট: যদি লিস্টের ডিলিট বাটন কাজ না করে, তবে উপরের ২ লাইন কমেন্ট করে রাখুন)

# সাইট হেডার কাস্টমাইজেশন
admin.site.site_header = "Felna High School ERP"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Felna Management System"