from django.urls import path
from website.views import TransactionListView, DepositView, BalanceView, MyBalanceView

urlpatterns = [
    path('transactions', TransactionListView.as_view(), name='transactions'),
    path('deposit', DepositView.as_view(), name='deposit'),
    path('balance', BalanceView.as_view(), name='balance'),
    path('mybalance', MyBalanceView.as_view(), name='mybalance'),
]
