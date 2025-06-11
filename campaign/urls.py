from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('import_contacts/', views.import_contacts, name='import_contacts'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('campaigns/new/', views.create_campaign, name='create_campaign'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('reports/', views.campaign_reports, name='reports'),
    path('campaign/<int:campaign_id>/report/', views.campaign_detail_report, name='campaign_detail_report'),
    path('top-campaign/', views.top_engaged_campaign, name='top_campaign'),

]
