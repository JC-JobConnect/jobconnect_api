from django.contrib import admin
from .models import Category, Job, Application ,profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','company','category','location','is_active','is_featured','created_at')
    list_filter = ('is_active','is_featured','category','location')
    search_fields = ('title','company','location')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user','job','status','applied_at')
    list_filter = ('status',)
    search_fields = ('user__username','job__title','email')

@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','location','birth_date')
    search_fields = ('user__username','location')