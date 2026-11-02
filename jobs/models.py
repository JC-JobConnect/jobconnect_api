from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name



class Job(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    def __str__(self): return f"{self.title} @ {self.company}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Information
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    headline = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = 'app_profile'

    def __str__(self):
        return self.user.username

class Education(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="educations"
    )
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=150)
    result = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.degree

    

class Experience(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="experiences"
    )
    job_title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    currently_working = models.BooleanField(default=False)
    responsibilities = models.TextField(blank=True)

    def __str__(self):
        return self.job_title

class Skill(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="skills"
    )
    skill_name = models.CharField(max_length=100)
    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL_CHOICES,
        default='Beginner'
    )

    def __str__(self):
        return self.skill_name


    
class Application(models.Model):
    STATUS = [('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'job')   


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name