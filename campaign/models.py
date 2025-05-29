from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    STATUS_CHOICES = [
        ('pending', 'لم يتم الإرسال'),
        ('sent', 'تم الإرسال'),
        ('rejected', 'مرفوض'),
    ]

    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='contacts')

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
