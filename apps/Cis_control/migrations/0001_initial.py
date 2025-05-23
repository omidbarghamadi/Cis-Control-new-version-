# Generated by Django 5.2.1 on 2025-05-14 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CisControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='نام شرکت')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
            ],
            options={
                'db_table': 'CIS Control',
            },
        ),
    ]
