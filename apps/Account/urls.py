from django.urls import path, include
from . import views
from django.shortcuts import render


def email_template(request):
    return render(request, 'email_template.html')


urlpatterns = [
    path('register/email/', views.SendVerificationCodeView.as_view(), name='email_input'),
    path('register/verify/', views.verify_code_view, name='verify_code'),
    path('resend-verification-code/', views.ResendVerificationCodeView.as_view(), name='resend_verification_code'),
    path('register/complete/', views.complete_profile, name='complete_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/provinces/', views.get_provinces, name='get_provinces'),
    path('api/cities/', views.get_cities, name='get_cities'),

]
