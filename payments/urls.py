from django.urls import path
from .views import *

urlpatterns = [
    path('', login_required(ProductListView.as_view()), name='paymenthome'),
    # path('create/', ProductCreateView.as_view(), name='create'),
    path('detail/<id>/', login_required(ProductDetailView.as_view()), name='detail'),
    path('success/', login_required(PaymentSuccessView.as_view()), name='success'),
    path('failed/', login_required(PaymentFailedView.as_view()), name='failed'),
    path('history/', login_required(OrderHistoryListView.as_view()), name='history'),

    path('api/checkout-session/<id>/',create_checkout_session, name='api_checkout_session'),
]