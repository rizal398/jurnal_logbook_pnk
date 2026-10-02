from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('semua/', views.semua_jurnal, name='semua_jurnal'),
    path('edit/<int:pk>/', views.edit_jurnal, name='edit_jurnal'),
    path('hapus/<int:pk>/', views.hapus_jurnal, name='hapus_jurnal'),
    path('export-pdf/', views.export_logbook_pdf, name='export_logbook_pdf'),
]