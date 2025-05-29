from django.shortcuts import render
from django.utils.translation import gettext as _

def home(request):
    greeting = _("Welcome to the WhatsApp Campaign System")
    return render(request, 'campaign/home.html', {'greeting': greeting})
