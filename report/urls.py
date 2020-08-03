from django.urls import path
from report.views import report, get_contact_trend

app_name = 'report'


urlpatterns = [
    path('', report, name='overview'),
    path('update_progress_trend/', report, name='report-update_progress_trend'),
    path('get_contact_trend/', get_contact_trend, name='report-get-contact-trend'),
]
