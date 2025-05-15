from django.db import models
from django.conf import settings

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_company = models.BooleanField(default=False)


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_profile")
    name = models.CharField(max_length=255, verbose_name="نام شرکت")
    responsible_person = models.CharField(max_length=255, verbose_name="نام مسئول")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="موبایل")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="لوگو")
    website = models.URLField(blank=True, null=True, verbose_name="وب سایت")
    province = models.TextField(max_length=100, verbose_name="استان")
    city = models.TextField(max_length=100, verbose_name="شهر")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")
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
