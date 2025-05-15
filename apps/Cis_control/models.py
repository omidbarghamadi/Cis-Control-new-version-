from django.db import models


class CisControl(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False, verbose_name="نام شرکت")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    created_at = models.DateField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return str(self.id) + "- " + self.title

    class Meta:
        db_table = 'CIS Control'
        # verbose_name = "کاربر"
        # verbose_name_plural = "کاربران"
