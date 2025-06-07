from django.shortcuts import render
from django.utils.translation import gettext as _

def home(request):
    greeting = _("Welcome to the WhatsApp Campaign System")
    return render(request, 'campaign/home.html', {'greeting': greeting})

def dashboard(request):
    context = {
        'page_title': _("Dashboard"),
        # يمكنك إضافة بيانات ديناميكية هنا مثل الإحصائيات
    }
    return render(request, 'campaign/dashboard.html', context)