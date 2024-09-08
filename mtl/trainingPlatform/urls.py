from django.urls import path
from .views import home, logout_view, register, save_answers, view_answers, view_detailed_answers, reset_answers, delete_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('save-answers/', save_answers, name='save_answers'),
    path('view-answers/', view_answers, name='view_answers'),
    path('answers/<int:result_id>/', view_detailed_answers, name='view_detailed_answers'),
    path('reset_answers/<int:result_id>/', reset_answers, name='reset_answers'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
]