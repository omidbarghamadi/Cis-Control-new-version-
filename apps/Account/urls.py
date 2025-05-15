from django.urls import path, include
from . import views
from django.shortcuts import render


def email_template(request):
    return render(request, 'email_template.html')


urlpatterns = [
    path('register/email/', views.SendVerificationCodeView.as_view(), name='email_input'),
    path('register/verify/', views.verify_code_view, name='verify_code'),
    path('register/complete/', views.CompleteProfileView, name='complete_profile'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('dashboard/', views.DashboardView, name='dashboard'),

]