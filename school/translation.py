# school/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import (
    Album, Gallery, Notice, OurHistory, Product, AdmissionResult,
    Slider, MissionVision, SchoolProfile, Founder, Donor, Management,
    WelcomeMessage, HeadmasterMessage, AssistantHeadmasterMessage,
    Teacher, Student, ExamResult, ClassRoutine, SchoolAchievement,
    Syllabus, ExamRoutine, AdmissionCircular, Prospectus, Facility
)

# Album Translation
@register(Album)
class AlbumTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

# Gallery Translation (image only, no text fields to translate)

# Notice Translation
@register(Notice)
class NoticeTranslationOptions(TranslationOptions):
    fields = ('title',)

# OurHistory Translation
@register(OurHistory)
class OurHistoryTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

# Product Translation
@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# AdmissionResult Translation
@register(AdmissionResult)
class AdmissionResultTranslationOptions(TranslationOptions):
    fields = ('student_name', 'status')

# Slider Translation
@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('headline', 'caption')

# MissionVision Translation
@register(MissionVision)
class MissionVisionTranslationOptions(TranslationOptions):
    fields = ('mission', 'vision')

# SchoolProfile Translation
@register(SchoolProfile)
class SchoolProfileTranslationOptions(TranslationOptions):
    fields = ('school_name', 'principal_name', 'address', 'contact_number', 'email', 'web_address', 'class_room_info')

# Founder Translation
@register(Founder)
class FounderTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# Donor Translation
@register(Donor)
class DonorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# Management Translation
@register(Management)
class ManagementTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# WelcomeMessage Translation
@register(WelcomeMessage)
class WelcomeMessageTranslationOptions(TranslationOptions):
    fields = ('title', 'message')

# HeadmasterMessage Translation
@register(HeadmasterMessage)
class HeadmasterMessageTranslationOptions(TranslationOptions):
    fields = ('title', 'message')

# AssistantHeadmasterMessage Translation
@register(AssistantHeadmasterMessage)
class AssistantHeadmasterMessageTranslationOptions(TranslationOptions):
    fields = ('title', 'message')

# Teacher Translation
@register(Teacher)
class TeacherTranslationOptions(TranslationOptions):
    fields = ('name', 'designation', 'subject', 'bio')

# Student Translation
@register(Student)
class StudentTranslationOptions(TranslationOptions):
    fields = ('name', 'guardian_name', 'address')

# ExamResult Translation
@register(ExamResult)
class ExamResultTranslationOptions(TranslationOptions):
    fields = ('subject',)

# ClassRoutine Translation
@register(ClassRoutine)
class ClassRoutineTranslationOptions(TranslationOptions):
    fields = ('subject',)

# SchoolAchievement Translation
@register(SchoolAchievement)
class SchoolAchievementTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'awarded_by')

# Syllabus Translation (image only)
@register(Syllabus)
class SyllabusTranslationOptions(TranslationOptions):
    fields = ()  # No text fields to translate

# ExamRoutine Translation (image only)
@register(ExamRoutine)
class ExamRoutineTranslationOptions(TranslationOptions):
    fields = ()  # No text fields to translate

# AdmissionCircular Translation
@register(AdmissionCircular)
class AdmissionCircularTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

# Prospectus Translation
@register(Prospectus)
class ProspectusTranslationOptions(TranslationOptions):
    fields = ('title',)

# Facility Translation
@register(Facility)
class FacilityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'category', 'location')