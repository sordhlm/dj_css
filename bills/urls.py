from django.urls import path
from bills.views import (
    BillsListView, CreateBillView, BillDeleteView, BillUpdateView
)

app_name = 'bills'

urlpatterns = [
    path('', BillsListView.as_view(), name='list'),
    path('create/', CreateBillView.as_view(), name='new_bill'),
    path('<int:pk>/edit/', BillUpdateView.as_view(), name="edit_bill"),
    path('<int:pk>/delete/', BillDeleteView.as_view(),
         name="remove_bill"),
]
