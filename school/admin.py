from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import strip_tags
from django import forms
from unfold.admin import ModelAdmin as UnfoldAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import *

# --- ১. কাস্টম রিচ টেক্সট ফরম ---
class ProfessionalForm(forms.ModelForm):
    class Meta:
        widgets = {
            'message': WysiwygWidget(), 'content': WysiwygWidget(),
            'bio': WysiwygWidget(), 'description': WysiwygWidget(),
            'mission': WysiwygWidget(), 'vision': WysiwygWidget(),
            'caption': WysiwygWidget(),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

# --- ২. বেস অ্যাডমিন ক্লাস (Single Page & Full Width Logic) ---
class BaseDescriptionAdmin(UnfoldAdmin):
    """
    ট্যাব ছাড়া সিঙ্গেল পেজ লেআউট এবং ফুল-উইডথ টেক্সট এরিয়া নিশ্চিত করে।
    """
    def render_change_form(self, request, context, **kwargs):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False,
        })
        return super().render_change_form(request, context, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # সব ধরনের টেক্সট ফিল্ড যা ১০০% চওড়া হওয়া প্রয়োজন
        full_fields = ['message', 'content', 'description', 'bio', 'mission', 'vision', 'caption', 'address', 'class_room_info', 'probable_admission_date']
        for field in full_fields:
            if field in form.base_fields:
                form.base_fields[field].widget.attrs.update({
                    'style': 'width: 100% !important; min-width: 100% !important; max-width: 100% !important;',
                    'rows': 5,
                })
        return form

    @display(description="Actions")
    def action_buttons(self, obj):
        app, model = obj._meta.app_label, obj._meta.model_name
        change_url = reverse(f"admin:{app}_{model}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{app}_{model}_delete", args=[obj.pk])
        btn = "display:inline-flex;align-items:center;gap:4px;padding:6px 12px;border-radius:8px;font-size:11px;font-weight:700;text-decoration:none;color:#fff;"
        return mark_safe(f"""
            <div style="display:flex;gap:8px;">
                <a href="{change_url}" style="{btn} background:#4f46e5;">Edit</a>
                <a href="{delete_url}" onclick="return confirm('Are you sure?')" style="{btn} background:#ef4444;">Delete</a>
            </div>
        """)

# --- ৩. স্লাইডার অ্যাডমিন ---
@admin.register(Slider)
class SliderAdmin(BaseDescriptionAdmin):
    list_display = ('display_preview', 'headline', 'order', 'is_active', 'action_buttons')
    list_editable = ('order', 'is_active')
    @display(description="Preview")
    def display_preview(self, obj):
        if obj.image: return mark_safe(f'<img src="{obj.image.url}" style="width:100px;height:50px;border-radius:10px;object-fit:cover;"/>')
        return "—"
    fieldsets = ((None, {"fields": (("headline", "order"), ("caption", "image"), "is_active")}),)

# --- ৪. মেসেজ মডেলসমূহ (Welcome, Headmaster, Asst. Headmaster) ---
@admin.register(WelcomeMessage, HeadmasterMessage, AssistantHeadmasterMessage)
class GlobalMessageAdmin(BaseDescriptionAdmin):
    list_display = ('display_photo', 'title', 'display_snippet', 'action_buttons')
    @display(description="Photo")
    def display_photo(self, obj):
        if obj.image: return mark_safe(f'<img src="{obj.image.url}" style="width:50px;height:50px;border-radius:10px;object-fit:cover;"/>')
        return "—"
    @display(description="Preview")
    def display_snippet(self, obj): return strip_tags(obj.message)[:60] + "..."
    fieldsets = (("Content", {"fields": ("title", "image", "message")}),)

# --- ৫. টিচার ও স্টাফ অ্যাডমিন ---
@admin.register(Teacher)
class TeacherAdmin(BaseDescriptionAdmin):
    form = ProfessionalForm
    list_display = ('display_photo', 'name', 'subject', 'display_status','last_edu',  'action_buttons')
    @display(description="Photo")
    def display_photo(self, obj):
        if obj.photo: return mark_safe(f'<img src="{obj.photo.url}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;"/>')
        return "—"
    @display(description="Status", label={True: "success", False: "danger"})
    def display_status(self, obj): return obj.is_active
    fieldsets = (
        ("Personal Details", {
            "fields": (
                ("name", "gender"), 
                ("photo", "bio"), 
                "join_date"
            )
        }),
        ("Professional Info", {
            "fields": (
                ("designation", "subject"), 
                ("phone", "email"), 
                ("last_edu", "is_active") # এখানে কমা (,) যোগ করা হয়েছে
            )
        }),
    )

# --- ৬. স্টুডেন্ট অ্যাডমিন ---
@admin.register(Student)
class StudentAdmin(BaseDescriptionAdmin):
    list_display = ('display_avatar', 'name', 'class_name', 'roll_number', 'action_buttons')
    @display(description="Student")
    def display_avatar(self, obj):
        photo = obj.photo.url if obj.photo else f"https://ui-avatars.com/api/?name={obj.name}&background=4f46e5&color=fff"
        return mark_safe(f'<img src="{photo}" style="width:40px;height:40px;border-radius:10px;object-fit:cover;"/>')
    fieldsets = (
        ("Academic info", {"fields": (("name", "roll_number"), ("class_name", "is_active"))}),
        ("Personal info", {"fields": (("gender", "date_of_birth"), "photo", ("guardian_name", "phone"))}),
        ("Address", {"fields": ("address",)}),
    )

# --- ৭. স্কুল প্রোফাইল ---
@admin.register(SchoolProfile)
class SchoolProfileAdmin(BaseDescriptionAdmin):
    list_display = ('school_name', 'principal_name', 'contact_number', 'action_buttons')
    fieldsets = (
        ("Identity", {"fields": (("school_name", "eiin"), ("principal_name", "established_date"))}),
        ("Contact", {"fields": (("contact_number", "email"), "web_address")}),
        ("Location & Details", {"fields": ("address", "class_room_info", "probable_admission_date")}),
    )

# --- ৮. স্টুডেন্ট রেজিস্ট্রেশন ---
@admin.register(StudentRegistration)
class StudentRegistrationAdmin(BaseDescriptionAdmin):
    list_display = ('student_name', 'batch', 'village', 'is_verified', 'action_buttons')
    readonly_fields = [f.name for f in StudentRegistration._meta.fields if f.name != 'is_verified']
    def has_add_permission(self, request): return False
    
    # ভেরিফিকেশন করার জন্য এখানে সেভ বাটন সক্রিয় রাখা হয়েছে
    def render_change_form(self, request, context, **kwargs):
        context.update({'show_save': True, 'show_save_and_continue': False, 'show_delete': True})
        return super().render_change_form(request, context, **kwargs)

    fieldsets = (
        ("Registration Data", {"fields": ("student_photo", "student_name", ("gender", "marrital_status"), "batch")}),
        ("Contact Info", {"fields": (("bd_no", "is_whatsapp_bd"), ("abroad_no", "is_whatsapp_abroad"), "village")}),
        ("Other Info", {"fields": ("current_location", ("occupation", "last_edu"), "is_no_hide", "is_verified")}),
    )

# --- ৯. রেজাল্ট ও একাডেমিক ---
@admin.register(AdmissionResult)
class AdmissionResultAdmin(BaseDescriptionAdmin):
    list_display = ('exam_track_number', 'student_name', 'class_name', 'display_status', 'action_buttons')
    @display(description="Status", label={"Passed": "success", "Failed": "danger", "Waiting": "warning"})
    def display_status(self, obj): return obj.status
    fieldsets = (("Result Info", {"fields": (("student_name", "exam_track_number"), ("class_name", "year"), "status")}),)

@admin.register(ExamResult)
class ExamResultAdmin(BaseDescriptionAdmin):
    list_display = ('student', 'year', 'subject', 'display_marks', 'action_buttons')
    @display(description="Marks")
    def display_marks(self, obj): return f"{obj.marks_obtained} / {obj.total_marks}"
    fieldsets = (("Score Record", {"fields": (("student", "year"), "subject", ("marks_obtained", "total_marks"))}),)

# --- ১০. অন্যান্য মডিউল (Founder, History, Gallery, etc.) ---
@admin.register(OurHistory, Founder, Donor, Management, SchoolAchievement, Facility, Notice, MissionVision, Album, Gallery, Village)
class SharedContentAdmin(BaseDescriptionAdmin):
    form = ProfessionalForm
    list_display = ('__str__', 'action_buttons')
    def get_fieldsets(self, request, obj=None):
        fields = [f.name for f in self.model._meta.fields if f.name not in ['id', 'created_at', 'updated_at', 'slug']]
        return [(None, {"fields": fields})]

@admin.register(ClassRoutine, Syllabus, ExamRoutine, Prospectus, AdmissionCircular)
class AcademicDocumentAdmin(BaseDescriptionAdmin):
    list_display = ('__str__', 'action_buttons')

@admin.register(Visitor)
class VisitorAdmin(UnfoldAdmin):
    list_display = ('ip_address', 'visited_at', 'user_agent')
    readonly_fields = ('ip_address', 'visited_at', 'user_agent', 'session_key')



from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    # এর ফলে অ্যাডমিনে ইংরেজি এবং বাংলার জন্য আলাদা বক্স আসবে
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }




# সাইট সেটিংস
admin.site.site_header = "Felna High School"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Management Dashboard"