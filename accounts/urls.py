from django.urls import path
from .views import  user_login, user_logout, dashboard,create_entry
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", user_login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", user_logout, name="logout"),
    path('create_entry/', create_entry, name='create_entry'),
    path('edit_entry/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('entries/', views.entry_list, name='entry_list'),
    path('delete-entry/<int:pk>/', views.delete_entry, name='delete_entry'),
    path('create-subuser/',views.create_subuser, name='create_subuser'),
    path('toggle-subuser/<int:user_id>/', views.toggle_subuser_status, name='toggle_subuser_status'),
    path('reports/', views.reports_view, name='reports'),

   
    




path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        email_template_name='auth/password_reset_email.html',
        subject_template_name='auth/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]

