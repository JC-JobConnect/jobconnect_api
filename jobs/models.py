from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name



class Job(models.Model):

    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('remote', 'Remote'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]

   
    WORK_MODES = [
        ('onsite', 'On-site'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]

    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
    ]



    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='jobs')
    title = models.CharField(max_length=200)
    company = models.ForeignKey('Company',on_delete=models.CASCADE,related_name='jobs')
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    job_type = models.CharField(max_length=20,choices=JOB_TYPES,default='full_time')
    responsibilities = models.JSONField(default=list, blank=True)
    requirements = models.JSONField(default=list, blank=True)
    work_mode = models.CharField(max_length=20,choices=WORK_MODES,default='onsite')
    experience_level = models.CharField(max_length=20,choices=EXPERIENCE_LEVELS,default='entry')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.title} @ {self.company}"




class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'app_profile'

    def __str__(self):
        return self.user.username

   


    
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