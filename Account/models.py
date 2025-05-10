from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام شرکت")
    email = models.EmailField(unique=True, verbose_name="ایمیل شرکت")
    password = models.CharField(max_length=128, verbose_name="رمز عبور")
    responsible_person = models.CharField(max_length=255, verbose_name="نام مسئول")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="موبایل")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="لوگو")
    website = models.URLField(blank=True, null=True, verbose_name="وب سایت")
    Province = models.TextField(max_length=100, verbose_name="استان")
    city = models.TextField(max_length=100, verbose_name="شهر")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")
    status = models.BooleanField(default=False,  verbose_name="وضعیت")
    created_at = models.DateField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'Company'
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت ها"
