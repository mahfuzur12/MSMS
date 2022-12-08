from django.urls import path
from lessons import views


urlpatterns = [
    path('availability/', views.availability, name='availability'),
    path('request/', views.request_lesson, name='request_lesson'),
    path('request/student/', views.StudentRequestLesson.as_view(), name='student_request_lesson'),
    path('request/teacher/', views.TeacherRequestLesson.as_view(), name='teacher_request_lesson'),
    path('request/admin/', views.AdminRequestLesson.as_view(), name='admin_request_lesson'),
    path('edit/<pk>', views.edit_lesson, name='edit_lesson'),
    path('edit/student/<pk>/', views.StudentEditLesson.as_view(), name='student_edit_lesson'),
    path('edit/teacher/<pk>/', views.TeacherEditLesson.as_view(), name='teacher_edit_lesson'),
    path('edit/admin/<pk>/', views.AdminEditLesson.as_view(), name='admin_edit_lesson'),
    path('view/', views.ViewLessons.as_view(), name='view_lessons'),
    path('options/', views.options, name="lesson_options"),
    path('cancel/<pk>/', views.cancel_lesson, name="cancel_lesson"),
    path('book/<pk>/', views.book_lesson, name="book_lesson"),
    path('save/<pk>/', views.save_lesson, name="save_lesson"),
    path('finances/', views.Finances.as_view(), name="finances"),
    path('confirmTransfer/', views.confirmTransfer, name='confirmTransfer'),
    path('invoice/<pk>/', views.view_invoice, name='view_invoice')
]