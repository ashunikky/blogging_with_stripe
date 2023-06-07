from django.db import models
from django.core import validators
from blog.models import User
from datetime import datetime
# Create your models here.


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=70, verbose_name='Product Name')
    price = models.FloatField(verbose_name='Price', validators=[validators.MinValueValidator(299),
                                                                validators.MaxValueValidator(499)])
    description= models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name 

class OrderDetail(models.Model):

    customer = models.OneToOneField(User, related_name='order_user', on_delete=models.CASCADE,primary_key=True)

    customer_email = models.EmailField(verbose_name='Customer Email',null=True)

    product = models.ForeignKey(to=Product,verbose_name='Product',on_delete=models.PROTECT)

    amount = models.IntegerField(verbose_name='Amount')

    # stripe_payment_intent = models.CharField(max_length=200,null=True)

    session_id= models.CharField(max_length=200, null=True)

    has_paid = models.BooleanField(default=False,verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.customer_email 