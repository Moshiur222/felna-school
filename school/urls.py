from django.urls import path
from . import views
# from . import views_admin
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('', views.home, name='home'),
    path("contact/", views.contact, name="contact"),
    path('notice/', views.notice_list, name='notice'),
    path('exam-result/', views.exam_result_view, name='exam_result'),
    path('admission-result/', views.admission_result_view, name='admission_result'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/photos/<slug:slug>/', views.album_detail_view, name='photos'),
    path('history/', views.history_view, name='history'),
    path('donors/', views.donor_list, name='donor_list'),
    path('management/', views.management_list, name='management_list'),
    path('management/<int:pk>/', views.management_detail, name='management_detail'),
    path('founder/',views.founder,name='founder'),
    path('mv/',views.mv,name='mv'),
    path('profile',views.profile,name='profile'),
    path('teachers/', views.teacher_list, name='teachers'),
    path("founder/<int:pk>/", views.founder_detail, name="founder_detail"),
    path("headmaster-message/<int:pk>/", views.headmaster_message_detail, name="headmaster_message_detail"),
    path("teacher/<int:pk>/", views.teacher_detail, name="teacher_detail"),
    path("assistant-headmaster-message/<int:pk>/", views.assistant_headmaster_message_detail, name="assistant_headmaster_message_detail"),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),


    # ---------- Class Routine URLs ----------
    path('class-routines/', views.class_routine_list, name='class_routine_list'),
    path('class-routines/<int:pk>/', views.class_routine_detail, name='class_routine_detail'),
    path('achievements/', views.achievements_list, name='achievements_list'),
    path('achievements/<int:pk>/', views.achievement_detail, name='achievement_detail'),

    path('syllabus/', views.syllabus_view, name='syllabus_view'),
    path('exam-routine/', views.exam_routine_view, name='exam_routine_view'),
    path('admission-circulars/', views.admission_circular_list, name='admission_circular_list'),
    path('prospectus/', views.prospectus_list, name='prospectus_list'), 
    path('facilities/', views.facility_list, name='facility_list'),
    path('board_permission/', views.board_permission, name='board_permission'),
    path('facilities/<int:pk>/', views.facility_detail, name='facility_detail'),
    path('student/registration/', views.student_registration, name='student_registration'),
    path('student/registration/list', views.registration_students_list, name='registration_students_list'),
    path('student/registration/details/view/<int:id>/', views.registration_student_detail, name='registration_student_detail'),
    path('switch-language/', views.switch_language, name='switch_language'),
]
