from django.contrib import admin
from .models import Category, Job, Application ,Profile, Company,Education,Skill,Experience

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

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    can_delete = False
class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0
    can_delete = False


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    can_delete = False

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'location',
        'view_profile',
    )

    search_fields = ('user__username', 'location')

    inlines = [
    EducationInline,
    ExperienceInline,
    SkillInline,
    ]

    def view_profile(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse

        url = reverse(
            'admin:jobs_profile_change',
            args=[obj.pk]
        )

        return format_html(
            '<a href="{}">View Profile</a>',
            url
        )

    view_profile.short_description = 'Profile Details'

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'created_at')
    list_filter = ('location',)
    search_fields = ('name', 'location')