from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.home, name='bloghome'), 
    path('create', views.create, name='create'),
     path('update/<id>', views.update_blog, name='update'),
    path('delete/<id>', views.delete, name='delete'),
    path('blog_content/<id>',views.content,name='content'),
    path("signup", SignUpView.as_view(), name="signup"),
    # path('config/', views.stripe_config),
    # path('create-checkout-session/', views.create_checkout_session),
    
   
]