from django.contrib import admin
from .models import User, Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_company', 'date_joined')
    search_fields = ('username', 'is_company',)
    list_filter = ('date_joined', )
    ordering = ('id',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'responsible_person', 'city')
    search_fields = ('name', 'city')
    list_filter = ('city', 'province')
    ordering = ('id',)
