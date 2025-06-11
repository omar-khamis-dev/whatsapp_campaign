from django.db import models
from django.utils.translation import gettext_lazy as _

class   Group(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Not sent')),
        ('sent', _('Sent')),
        ('rejected', _('Rejected')),
    ]

    full_name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10, blank=True)  # رمز الدولة
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='contacts')

    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=255, blank=True)
    residence = models.CharField(max_length=255, blank=True)
    qualification = models.CharField(max_length=255, blank=True)
    specialty = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
class Campaign(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENDING = 'sending', _('Sending')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')

    name = models.CharField(_("Campaign Name"), max_length=200)
    group = models.ForeignKey("Group", verbose_name=_("Target Group"), on_delete=models.CASCADE)
    message_text = models.TextField(_("Message Text"))
    attachment = models.FileField(_("Attachment (optional)"), upload_to='attachments/', blank=True, null=True)
    scheduled_at = models.DateTimeField(_("Scheduled Date & Time"))
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.name
    

class MessageLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    REACTION_CHOICES = [
        ('not_delivered', 'Sent but not delivered'),
        ('delivered_unread', 'Delivered, unread'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('reacted', 'Reacted'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='messages')
    recipient = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reaction_status = models.CharField(max_length=20, choices=REACTION_CHOICES, blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.status} - {self.reaction_status}"