from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Job(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"{self.title} @ {self.company}"

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