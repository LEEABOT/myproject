import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render
from .models import Food
from .models import userInfo
from .forms import FoodForm
# Create your views here.

def toLogin_view(request):
    return render(request,'login.html')

def Login_view(request):
    u = request.POST.get("user", '')
    p = request.POST.get("password", '')
    if u and p:
        user = userInfo.objects.filter(user_name=u, user_password=p).first()
        if user:
            request.session['user_id'] = user.user_id
            return redirect(home_view)
        else:
            return HttpResponse("账号或密码错误！！")

def toregister_view(request):
    return render(request,'register.html')

def register_view(request):
    u=request.POST.get("user",'')
    p=request.POST.get("password", '')
    if u and p:
        user=userInfo(user_id=str(random.randrange(000000,999999)),user_name=u,user_password=p)
        user.save()
        return HttpResponse('注册成功')

def home_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = userInfo.objects.get(user_id=user_id)
        user_name = user.user_name
    else:
        user_name = 'Guest'
    return render(request, 'home.html', {'user_name': user_name})
def search(request):
    query = request.GET.get('q')
    if query:
        foods_list = Food.objects.filter(foodname__icontains=query)
    else:
        foods_list = Food.objects.all()

    paginator = Paginator(foods_list, 10)  # 每页显示10个菜谱
    page = request.GET.get('page')

    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)

    return render(request, 'search_results.html', {'foods': foods, 'query': query})

def upload_food_view(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'complete.html')
    else:
        form = FoodForm()
    return render(request, 'upmanu.html', {'form': form})