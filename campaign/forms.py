from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Contact, Group, Campaign
import datetime

class ContactImportForm(forms.Form):
    file = forms.FileField(
        label=_('Contact file'),
        help_text=_('Choose a CSV, Excel, or VCF file (.csv, .xlsx, .vcf)'),
        widget=forms.ClearableFileInput(attrs={'accept': '.csv,.xlsx,.vcf'})
    )

    group_name = forms.CharField(
        label=_('Group name'),
        max_length=100,
        initial=lambda: _('Group') + f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        help_text=_('A new group will be created automatically. You can rename it.')
    )


class ContactSearchForm(forms.Form):
    query = forms.CharField(
        label=_('Search by name, phone, or email'),
        required=False
    )

    group = forms.ModelChoiceField(
        label=_('Group'),
        queryset=Group.objects.all(),
        required=False,
        empty_label=_("All groups")
    )

    status = forms.ChoiceField(
        label=_('Status'),
        choices=[('', _('All statuses'))] + [(k, _(v)) for k, v in Contact.STATUS_CHOICES],
        required=False
    )

    gender = forms.ChoiceField(
        label=_('Gender'),
        choices=[
            ('', _('All')),
            ('ذكر', _('Male')),
            ('أنثى', _('Female')),
        ],
        required=False
    )

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'group', 'message_text', 'attachment', 'scheduled_at']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'message_text': forms.Textarea(attrs={'rows': 4, 'class': 'form-textarea'}),
        }
        labels = {
            'name': _("Campaign Name"),
            'group': _("Target Group"),
            'message_text': _("Message Text"),
            'attachment': _("Attachment"),
            'scheduled_at': _("Scheduled Date & Time"),
        }