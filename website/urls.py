from django.urls import path
from website.views import TransactionListView, DepositView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('deposit/', DepositView.as_view(), name='deposit'),
]
