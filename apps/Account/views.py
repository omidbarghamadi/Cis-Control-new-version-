from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import EmailVerificationForm
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Company, User
from django import forms
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
import requests, re
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required


class SendVerificationCodeView(FormView):
    template_name = "email_input.html"
    form_class = EmailVerificationForm
    success_url = reverse_lazy("verify_code")  # مسیر مرحله بعد

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        # بررسی وجود ایمیل
        if User.objects.filter(email=email).exists():
            messages.warning(
                self.request,
                "این ایمیل قبلاً ثبت‌نام شده است. لطفاً وارد شوید."
            )
            return redirect("login")

        code = str(random.randint(100000, 999999))

        # قالب HTML ایمیل را بارگیری و مقداردهی کن
        html_message = render_to_string("email_template.html", {"code": code})

        # ارسال ایمیل
        send_mail(
            subject="کد تأیید ایمیل در سامانه CIS Control",
            message="",
            from_email="noreply@yourdomain.com",
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        # ذخیره در session
        self.request.session["email"] = email
        self.request.session["verification_code"] = code
        self.request.session["code_sent_time"] = timezone.now().isoformat()  # ذخیره زمان برای بررسی انقضا

        messages.success(
            self.request,
            "کد تأیید به ایمیل شما ارسال شد. (اگر ایمیل را دریافت نکردید، پوشه Spam یا هرزنامه را بررسی کنید.)"
        )

        return super().form_valid(form)


def verify_code_view(request):
    if request.method == 'POST':
        # استخراج کد وارد شده
        input_code = ''.join([
            request.POST.get(f'code_{i}', '') for i in range(1, 7)
        ])

        # گرفتن اطلاعات از سشن
        email = request.session.get('email')
        real_code = request.session.get('verification_code')
        code_sent_time_str = request.session.get('code_sent_time')

        # بررسی وجود زمان ارسال
        if code_sent_time_str:
            code_sent_time = timezone.datetime.fromisoformat(code_sent_time_str)

            # بررسی انقضای دو دقیقه
            if timezone.now() - code_sent_time > timedelta(minutes=2):
                messages.error(request, "کد منقضی شده است. لطفاً دوباره تلاش کنید.")
                return render(request, 'verify_code.html')

        # بررسی تطابق کد
        if input_code == real_code:
            messages.success(request, "کد با موفقیت تأیید شد.")
            return redirect("complete_profile")
        else:
            messages.error(request, "کد وارد شده نادرست است.")

    return render(request, 'verify_code.html')


class ResendVerificationCodeView(View):
    def post(self, request, *args, **kwargs):
        email = request.session.get("email")
        if not email:
            return JsonResponse({"message": "ایمیل یافت نشد. لطفاً دوباره تلاش کنید."}, status=400)

        code = str(random.randint(100000, 999999))
        html_message = render_to_string("email_template.html", {"code": code})

        try:
            send_mail(
                subject="کد تأیید ایمیل در سامانه CIS Control",
                message="",
                from_email="noreply@yourdomain.com",
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            # ذخیره کد جدید در session
            request.session["verification_code"] = code
            request.session["code_sent_time"] = timezone.now().isoformat()
            return JsonResponse({"message": "کد تأیید با موفقیت ارسال شد!"})
        except Exception as e:
            return JsonResponse({"message": "ارسال ایمیل با خطا مواجه شد."}, status=500)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'responsible_person', 'phone_number', 'logo', 'website', 'province', 'city', 'address']


def is_strong_password(password):
    # پسورد قوی: حداقل ۸ کاراکتر، حروف بزرگ، کوچک، عدد و نماد
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[@$!%*?&#^()_\-+=]', password):
        return False
    return True


def complete_profile(request):
    if not request.session.get("email"):
        return redirect("email_input")

    error_message = None

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not password1 or not password2:
            error_message = "رمز عبور و تکرار آن را وارد کنید."
        elif password1 != password2:
            error_message = "رمز عبور و تکرار آن یکسان نیستند."
        elif not is_strong_password(password1):
            error_message = "رمز عبور باید حداقل ۸ کاراکتر، شامل عدد، حروف بزرگ، حروف کوچک و نماد باشد."
        elif form.is_valid():
            email = request.session.get("email")
            if User.objects.filter(email=email).exists():
                error_message = "برای این ایمیل قبلاً حساب کاربری ایجاد شده است."
            else:
                user = User.objects.create_user(username=email, email=email)
                user.is_company = True
                user.set_password(password1)  # ست کردن پسورد قوی کاربر
                user.save()

                company = form.save(commit=False)
                company.user = user
                company.save()

                login(request, user)
                return redirect("dashboard")
        # اگر form نامعتبر بود، خطاهای فرم نشان داده می‌شود

    else:
        form = CompanyForm()
        error_message = None

    return render(
        request,
        "complete_profile.html",
        {"form": form, "error_message": error_message}
    )


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "ایمیل یا رمز عبور اشتباه است.")
    return render(request, "login.html")


@login_required
def dashboard_view(request):
    company = getattr(request.user, "company_profile", None)
    return render(request, "dashboard.html", {
        "user": request.user,
        "company": company,
    })


def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت از حساب کاربری خارج شدید.")
    return redirect("login")


def get_provinces(request):
    response = requests.get("https://iran-locations-api.ir/api/v1/fa/states")
    return JsonResponse(response.json(), safe=False)


def get_cities(request):
    state_id = request.GET.get("state_id")
    if not state_id:
        return JsonResponse({"error": "state_id parameter is required."}, status=400)
    response = requests.get(f"https://iran-locations-api.ir/api/v1/fa/cities?state_id={state_id}")
    return JsonResponse(response.json(), safe=False)