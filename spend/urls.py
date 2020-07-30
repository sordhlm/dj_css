from django.urls import path
from spend.views import (
    SpendListView, CreateSpendView, SpendDeleteView, SpendUpdateView
)

app_name = 'bills'

urlpatterns = [
    path('', SpendListView.as_view(), name='list'),
    path('create/', CreateSpendView.as_view(), name='new_spend'),
    path('<int:pk>/edit/', SpendUpdateView.as_view(), name="edit_spend"),
    path('<int:pk>/delete/', SpendDeleteView.as_view(),
         name="remove_spend"),
]
