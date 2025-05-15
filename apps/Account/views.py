from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import EmailVerificationForm
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string


class SendVerificationCodeView(FormView):
    template_name = "email_input.html"
    form_class = EmailVerificationForm
    success_url = reverse_lazy("verify_code")  # مسیر مرحله بعد

    def form_valid(self, form):
        email = form.cleaned_data["email"]
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
        self.request.session["verification_email"] = email
        self.request.session["verification_code"] = code
        self.request.session["code_sent_time"] = timezone.now().isoformat()  # ذخیره زمان برای بررسی انقضا

        messages.success(
            self.request,
            "کد تأیید به ایمیل شما ارسال شد. (اگر ایمیل را دریافت نکردید، پوشه Spam یا هرزنامه را بررسی کنید.)"
        )

        return super().form_valid(form)


def verify_code_view(request):
    if request.method == 'POST':
        # استخراج مقادیر 6 اینپوت و ترکیب آن‌ها به یک رشته
        input_code = ''.join([
            request.POST.get(f'code_{i}', '') for i in range(1, 7)  # انتظار می‌رود نام اینپوت‌ها به صورت code_1, code_2, ... باشد
        ])
        email = request.session.get('email')  # ایمیل قبلاً باید در سشن ذخیره شده باشد
        real_code = request.session.get('verification_code')  # کد ذخیره شده در سشن

        if input_code == real_code:
            messages.success(request, "کد با موفقیت تأیید شد.")
            # return redirect('register_company')  # به فرم بعدی ثبت شرکت منتقل می‌شود
        else:
            messages.error(request, "کد وارد شده نادرست است.")

    return render(request, 'verify_code.html')


class CompleteProfileView:
    pass


class LoginView:
    pass


class DashboardView:
    pass


class Logout:
    pass
