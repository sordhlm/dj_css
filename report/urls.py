from django.urls import path
from report.views import report

app_name = 'report'


urlpatterns = [
    path('', report, name='overview'),
    path('update_progress_trend/', report, name='report-update_progress_trend'),
]
