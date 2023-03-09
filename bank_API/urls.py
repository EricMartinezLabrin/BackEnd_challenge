# django
from django.urls import path

# Local
from . import views

app_name = "api"

urlpatterns = [
    path('account_create_view', views.AccountCreateView.as_view(),
         name='account_create_view'),
    path('account_update_view/<int:pk>', views.AccountUpdateView.as_view(),
         name='account_update_view'),
    path('account_delete_view/<str:account_number>', views.AccountDeleteView.as_view(),
         name='account_delete_view'),
    path('account_detail_view/<str:account_number>', views.AccountDetailView.as_view(),
         name='account_detail_view'),
    path('transaction_create_view', views.TransactionCreateView.as_view(),
         name='transaction_create_view'),
    path('transaction_update_view/<int:pk>', views.TransactionUpdateView.as_view(),
         name='transaction_update_view'),
    path('transaction_delete_view/<str:transaction_id>', views.TransactionDeleteView.as_view(),
         name='transaction_delete_view'),
    path('transaction_detail_view/<str:transaction_id>', views.TransactionDetailView.as_view(),
         name='transaction_detail_view'),
]
