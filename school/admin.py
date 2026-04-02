from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin as UnfoldAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from django import forms

# Custom form for rich text fields
class RichTextModelForm(forms.ModelForm):
    class Meta:
        widgets = {
            'message': WysiwygWidget(),
            'content': WysiwygWidget(),
            'bio': WysiwygWidget(),
            'description': WysiwygWidget(),
            'mission': WysiwygWidget(),
            'vision': WysiwygWidget(),
        }

@admin.register(Gallery)
class GalleryAdmin(UnfoldAdmin):
    list_display = ('title', 'image_preview', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('image_preview',)
    list_filter = ('created_at',)
    
    fieldsets = (
        ('Gallery Item', {
            'fields': ('title', 'image', 'image_preview'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 150px;" />')
        return "No Image"
    image_preview.short_description = "Image Preview"


@admin.register(Notice)
class NoticeAdmin(UnfoldAdmin):
    list_display = ('title', 'date', 'file_preview', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title',)
    ordering = ('-date',)
    readonly_fields = ('file_preview',)
    
    fieldsets = (
        ('Notice Information', {
            'fields': (
                'title',
                'date',
                'file',
                'file_preview',
            )
        }),
    )
    
    def file_preview(self, obj):
        if obj.file:
            return mark_safe(f'<a href="{obj.file.url}" target="_blank">ðŸ“„ View File</a>')
        return "No File"
    file_preview.short_description = "File Preview"


@admin.register(OurHistory)
class OurHistoryAdmin(UnfoldAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    form = RichTextModelForm
    
    fieldsets = (
        ('History Content', {
            'fields': (
                'title',
                'content',
            )
        }),
    )


@admin.register(AdmissionResult)
class AdmissionResultAdmin(UnfoldAdmin):
    list_display = ('exam_track_number', 'student_name', 'class_name', 'year', 'status', 'created_at')
    list_filter = ('class_name', 'year', 'status', 'created_at')
    search_fields = ('exam_track_number', 'student_name')
    ordering = ('-year', 'class_name')
    
    fieldsets = (
        ('Admission Information', {
            'fields': (
                'exam_track_number',
                'student_name',
                'class_name',
                'year',
            )
        }),
        ('Result Details', {
            'fields': (
                'status',
            )
        }),
    )


@admin.register(Slider)
class SliderAdmin(UnfoldAdmin):
    list_display = ('headline', 'order', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('headline', 'caption')
    readonly_fields = ('image_preview',)
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Slider Content', {
            'fields': ('headline', 'caption', 'order', 'is_active'),
        }),
        ('Image Upload', {
            'fields': ('image', 'image_preview'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 150px;" />')
        return "No Image"
    image_preview.short_description = "Image Preview"


@admin.register(MissionVision)
class MissionVisionAdmin(UnfoldAdmin):
    list_display = ('created_at',)
    search_fields = ('mission', 'vision')
    form = RichTextModelForm
    
    fieldsets = (
        ('Mission & Vision', {
            'fields': (
                'mission',
                'vision',
            )
        }),
    )


@admin.register(SchoolProfile)
class SchoolProfileAdmin(UnfoldAdmin):
    list_display = ('school_name', 'principal_name', 'contact_number', 'established_date', 'eiin')
    search_fields = ('school_name', 'principal_name', 'address', 'eiin')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'school_name',
                'principal_name',
                'established_date',
                'eiin',
            )
        }),
        ('Contact Information', {
            'fields': (
                'address',
                'contact_number',
                'fax_number',
                'email',
                'web_address',
            )
        }),
        ('Additional Information', {
            'fields': (
                'class_room_info',
                'probable_admission_date',
            )
        }),
    )


@admin.register(Founder)
class FounderAdmin(UnfoldAdmin):
    list_display = ('name', 'photo_preview', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('id',)
    
    fieldsets = (
        ('Founder Information', {
            'fields': (
                'name',
                'photo',
                'photo_preview',
                'description',
            )
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 100px; max-width: 100px;" />')
        return "No Photo"
    photo_preview.short_description = "Photo Preview"


@admin.register(Donor)
class DonorAdmin(UnfoldAdmin):
    list_display = ('name', 'photo_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('id',)
    
    fieldsets = (
        ('Donor Information', {
            'fields': (
                'name',
                'photo',
                'photo_preview',
                'description',
            )
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 100px; max-width: 100px;" />')
        return "No Photo"
    photo_preview.short_description = "Photo Preview"


@admin.register(Management)
class ManagementAdmin(UnfoldAdmin):
    list_display = ('name', 'photo_preview', 'created_at')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    fieldsets = (
        ('Management Member Information', {
            'fields': (
                'name',
                'photo',
                'photo_preview',
                'description',
            )
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 100px; max-width: 100px;" />')
        return "No Photo"
    photo_preview.short_description = "Photo Preview"


@admin.register(WelcomeMessage)
class WelcomeMessageAdmin(UnfoldAdmin):
    list_display = ('title', 'message_snippet', 'image_preview')
    readonly_fields = ('image_preview',)
    form = RichTextModelForm
    
    fieldsets = (
        ('Welcome Message Content', {
            'fields': ('title', 'message'),
        }),
        ('Image Upload', {
            'fields': ('image', 'image_preview'),
            'description': 'Image will be automatically resized to 350x200 pixels upon upload.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 350px;" />')
        return "No Image"
    image_preview.short_description = "Image Preview"

    def message_snippet(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_snippet.short_description = "Message"


@admin.register(HeadmasterMessage)
class HeadmasterMessageAdmin(UnfoldAdmin):
    list_display = ('title', 'message_snippet', 'image_preview')
    readonly_fields = ('image_preview',)
    form = RichTextModelForm
    
    fieldsets = (
        ('Headmaster Message Content', {
            'fields': ('title', 'message'),
        }),
        ('Image Upload', {
            'fields': ('image', 'image_preview'),
            'description': 'Image will be automatically resized to 200x200 pixels upon upload.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" />')
        return "No Image"
    image_preview.short_description = "Image Preview"

    def message_snippet(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_snippet.short_description = "Message"


@admin.register(AssistantHeadmasterMessage)
class AssistantHeadmasterMessageAdmin(UnfoldAdmin):
    list_display = ('title', 'message_snippet', 'image_preview')
    readonly_fields = ('image_preview',)
    form = RichTextModelForm
    
    fieldsets = (
        ('Assistant Headmaster Message Content', {
            'fields': ('title', 'message'),
        }),
        ('Image Upload', {
            'fields': ('image', 'image_preview'),
            'description': 'Image will be automatically resized to 200x200 pixels upon upload.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" />')
        return "No Image"
    image_preview.short_description = "Image Preview"

    def message_snippet(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_snippet.short_description = "Message"


@admin.register(Teacher)
class TeacherAdmin(UnfoldAdmin):
    list_display = ('name', 'designation', 'subject', 'photo_preview', 'join_date', 'is_active')
    list_filter = ('designation', 'subject', 'gender', 'is_active', 'join_date')
    search_fields = ('name', 'designation', 'subject', 'phone', 'email')
    readonly_fields = ('photo_preview',)
    ordering = ('name',)
    form = RichTextModelForm
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'name', 
                'gender', 
                'photo', 
                'photo_preview',
                'join_date',
            )
        }),
        ('Professional Information', {
            'fields': (
                'designation',
                'subject',
                'phone',
                'email',
            )
        }),
        ('Status & Biography', {
            'fields': (
                'is_active',
                'bio',
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 100px; max-width: 100px;" />')
        return "No Photo"
    photo_preview.short_description = "Photo Preview"


@admin.register(Student)
class StudentAdmin(UnfoldAdmin):
    list_display = (
        'name',
        'class_name',
        'roll_number',
        'gender',
        'guardian_name',
        'phone',
        'is_active',
        'photo_preview',
    )
    list_display_links = ('name',)
    list_filter = ('class_name', 'gender', 'is_active', 'created_at')
    search_fields = ('name', 'roll_number', 'guardian_name', 'phone')
    ordering = ('class_name', 'roll_number')
    readonly_fields = ('photo_preview',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'name',
                'roll_number',
                'class_name',
                'gender',
                'date_of_birth',
                'photo',
                'photo_preview',
            )
        }),
        ('Guardian Information', {
            'fields': (
                'guardian_name',
                'phone',
                'address',
            )
        }),
        ('Status', {
            'fields': (
                'is_active',
            )
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 100px; max-width: 100px;" />')
        return "No Photo"
    photo_preview.short_description = "Photo Preview"


@admin.register(ExamResult)
class ExamResultAdmin(UnfoldAdmin):
    list_display = (
        'student_name',
        'class_name',
        'roll_number',
        'year',
        'subject',
        'marks_obtained',
        'total_marks',
    )
    list_display_links = ('student_name',)
    list_filter = ('year', 'student__class_name', 'subject')
    search_fields = ('student__name', 'student__roll_number', 'subject')
    ordering = ('-year', 'student__class_name', 'student__roll_number')
    
    fieldsets = (
        ('Student Information', {
            'fields': (
                'student',
            )
        }),
        ('Exam Details', {
            'fields': (
                'year',
                'subject',
                'marks_obtained',
                'total_marks',
            )
        }),
    )

    def student_name(self, obj):
        return obj.student.name
    student_name.admin_order_field = 'student__name'
    student_name.short_description = 'Student Name'

    def class_name(self, obj):
        return obj.student.class_name
    class_name.admin_order_field = 'student__class_name'
    class_name.short_description = 'Class'

    def roll_number(self, obj):
        return obj.student.roll_number
    roll_number.admin_order_field = 'student__roll_number'
    roll_number.short_description = 'Roll Number'


@admin.register(ClassRoutine)
class ClassRoutineAdmin(UnfoldAdmin):
    list_display = (
        'day',
        'class_name',
        'subject',
        'teacher_name',
        'start_time',
        'end_time',
        'routine_image_preview',
    )
    list_display_links = ('day',)
    list_filter = ('class_name', 'day', 'teacher')
    search_fields = ('subject', 'teacher__name')
    ordering = ('class_name', 'day', 'start_time')

    fieldsets = (
        ('Routine Information', {
            'fields': (
                'day',
                'class_name',
                'subject',
                'teacher',
            )
        }),
        ('Time Schedule', {
            'fields': (
                'start_time',
                'end_time',
            )
        }),
        ('Routine Image', {
            'fields': ('image',)
        }),
    )

    def teacher_name(self, obj):
        if obj.teacher:
            return obj.teacher.name
        return "No Teacher"
    teacher_name.admin_order_field = 'teacher__name'
    teacher_name.short_description = 'Teacher'

    def routine_image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="50" style="object-fit: cover;" />'
        return "No Image"
    routine_image_preview.allow_tags = True
    routine_image_preview.short_description = 'Image'


@admin.register(SchoolAchievement)
class SchoolAchievementAdmin(UnfoldAdmin):
    list_display = (
        'title',
        'year',
        'date_awarded',
        'awarded_by',
        'achievement_image',
    )
    list_display_links = ('title',)
    list_filter = ('year', 'awarded_by')
    search_fields = ('title', 'description', 'awarded_by')
    ordering = ('-year', '-date_awarded')

    fieldsets = (
        ('Achievement Details', {
            'fields': (
                'title',
                'description',
                'awarded_by',
                'year',
                'date_awarded',
            )
        }),
        ('Media', {
            'fields': (
                'image',
            )
        }),
    )

    def achievement_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit:cover;" />'
        return "No Image"
    achievement_image.allow_tags = True
    achievement_image.short_description = 'Image'


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'image_preview', 'created_at')
    list_filter = ('class_name',)
    search_fields = ('class_name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="60" style="object-fit:cover;"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Image Preview"


@admin.register(ExamRoutine)
class ExamRoutineAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'image_preview', 'created_at')
    list_filter = ('class_name',)
    search_fields = ('class_name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="60" style="object-fit:cover;"/>'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Image Preview"


@admin.register(AdmissionCircular)
class AdmissionCircularAdmin(UnfoldAdmin):
    list_display = (
        'title',
        'class_name',
        'created_at',
        'circular_image',
    )
    list_display_links = ('title',)
    list_filter = ('class_name', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    fieldsets = (
        ('Circular Details', {
            'fields': (
                'title',
                'description',
                'class_name',
                'document',
            )
        }),
        ('Media', {
            'fields': (
                'image',
            )
        }),
    )

    def circular_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit:cover;" />'
        return "No Image"
    circular_image.allow_tags = True
    circular_image.short_description = 'Image'


@admin.register(Prospectus)
class ProspectusAdmin(UnfoldAdmin):
    list_display = (
        'title',
        'class_name',
        'year',
        'prospectus_image',
        'created_at',
    )
    list_display_links = ('title',)
    list_filter = ('class_name', 'year')
    search_fields = ('title',)
    ordering = ('-year', 'class_name', 'title')

    fieldsets = (
        ('Prospectus Details', {
            'fields': (
                'title',
                'class_name',
                'year',
            )
        }),
        ('Media', {
            'fields': (
                'image',
                'document',
            )
        }),
    )

    def prospectus_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit:cover; border-radius: 4px;" />'
        return "No Image"
    prospectus_image.allow_tags = True
    prospectus_image.short_description = 'Image'


@admin.register(Facility)
class FacilityAdmin(UnfoldAdmin):
    list_display = (
        'title',
        'category',
        'capacity',
        'location',
        'status',
        'facility_image',
    )
    list_display_links = ('title',)
    list_filter = ('category', 'status')
    search_fields = ('title', 'description', 'category', 'location')
    ordering = ('title',)

    fieldsets = (
        ('Facility Details', {
            'fields': (
                'title',
                'description',
                'category',
                'capacity',
                'location',
                'status',
            )
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )

    def facility_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit:cover; border-radius:4px;" />'
        return "No Image"
    facility_image.allow_tags = True
    facility_image.short_description = 'Image'
    
# Customize admin site
admin.site.site_header = "School Management System"
admin.site.site_title = "School Admin Portal"
admin.site.index_title = "Welcome to School Management System"


from django.contrib import admin
from .models import StudentRegistration, Village

class StudentRegistrations(admin.ModelAdmin):
    list_display = ('student_name', 'gender','marrital_status','is_whatsapp', 'batch', 'village', 'current_location', 'bd_no', 'abroad_no', 'occupation', 'last_edu')
    ordering = ('batch', 'student_name')

admin.site.register(StudentRegistration, StudentRegistrations)
admin.site.register(Village)