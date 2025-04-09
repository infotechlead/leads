from django.urls import path
from .views import  user_login, user_logout, dashboard,create_entry,create_subuser
from . import views

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

]

