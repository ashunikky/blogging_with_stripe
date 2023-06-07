from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from blog.forms import BlogUpdateForm
from payments.models import OrderDetail,Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from datetime import datetime, timedelta


# from django.conf import settings # new
# from django.http.response import JsonResponse # new
# from django.views.decorators.csrf import csrf_exempt # new
# import stripe


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("bloghome")
    template_name = "registration/signup.html"

@login_required
def home(request):
    user_id= request.user.id
    
    order = OrderDetail.objects.all()
    
    product=Product.objects.all()
    try:
        payment_customer=order.get(customer=user_id)
        c_product = payment_customer.product
        premium=product[1]
        order_date= payment_customer.created_on.date()
        current_date = datetime.now().date()
        expiry_date= order_date+timedelta(days=366)
        blogs=Blog.objects.all().order_by('-last_modified')
        user_blogs= Blog.objects.filter(user=payment_customer.customer)
        ub_count= user_blogs.count()
        return render(request, 'home.html',{'blogs':blogs,'c_product':c_product,'premium':premium,'order_date':order_date,'expiry_date':expiry_date,'current_date':current_date,'user_blogs':user_blogs,'ub_count':ub_count})     
    except Exception as e:
        print(e)
        return render(request,'home2.html')

    
@login_required
def create(request):
    try:    
        user_id= request.user.id   
        order = OrderDetail.objects.all()
        payment_customer=order.get(customer=user_id)
        product=Product.objects.all()
        c_product = payment_customer.product
        premium=product[1]
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')  
            user = request.user
            b1= Blog(title=title,content=content,user=user) 
            b1.save()
            return render(request,"action_complete.html")
        return render(request,'blog_form.html',{'c_product':c_product,'premium':premium})
    except: 
        return HttpResponse("action not allowed !")

@login_required
def content(request,id):
    try:
        user_id= request.user.id
        order = OrderDetail.objects.all()
        payment_customer=order.get(customer=user_id)
        c_paid = payment_customer.has_paid
        content=Blog.objects.get(id=id)
        auth_customer=payment_customer.customer.id==content.user.id
        content_id=content.id
        return render (request,'content.html',{'content':content,'c_paid':c_paid,'auth_customer':auth_customer,'content_id':content_id})
    except Exception as e:
        print (e)
        return render(request,'content.html')

@login_required
def update_blog(request,id):
    context={}
    blog = get_object_or_404(Blog, id=id)
    form = BlogUpdateForm(instance=blog)
    if request.method == "POST":
        form = BlogUpdateForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
        return render(request,'action_complete.html')

    context["form"] = form
    return render(request, "blog_update.html", context)

@login_required
def delete (request,id):
    try:
        userid=request.user.id
        content_id=Blog.objects.get(id=id)
        content_userid=content_id.user.id

        print (content_userid)
        print (userid)
        if userid ==content_userid:
            content_id.delete()
            return HttpResponse('blog deleted')

    except:
        return HttpResponse('action not allowed!')


