from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

class ProductListView(ListView):
    model = Product
    template_name = "payments/product_list.html"
    context_object_name = 'product_list'

class ProductDetailView(DetailView):
    model = Product
    template_name = "payments/product_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  
        
@login_required
@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'INR',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price*100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )


    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price )
    order.session_id= checkout_session.id
    order.save()
    print(f'checkoutview:{checkout_session.id}')

    # return JsonResponse({'data': checkout_session})
    
    return JsonResponse({'sessionId': checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        print(f'paymentsuccesssview:{session_id}')

        # order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order = get_object_or_404(OrderDetail, session_id=session.id)
    
        # print(f'paymentsuccesssview:{order.id}')
        
        order.has_paid = True
        order.save()
        
        return render(request, "payments/payment_success.html")

class PaymentFailedView(TemplateView):
    template_name = "payments/payment_failed.html"

class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "payments/order_history.html"
