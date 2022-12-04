from django.urls import path
from lessons import views


urlpatterns = [
    path('availability/', views.availability, name='availability'),
    path('request/', views.RequestLesson.as_view(), name='request_lesson'),
    path('edit/<pk>', views.EditLesson.as_view(), name='edit_lesson'),
    path('view/', views.ViewLessons.as_view(), name='view_lessons'),
    path('options/', views.options, name="lesson_options")
]