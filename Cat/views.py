from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
# from .models import cal
# Create your views here.
# def index(request):
#     return render(request,'index.html')
# def calpage(request):
#     return render(request,'cal.html')
# def calculate(request):
#     value_a = request.POST['valueA']
#     value_b = request.POST['valueB']
#     result = int(value_b)+int(value_a)
#     cal.objects.create(value_a=value_a,value_b=value_b,result=result)
#     return render(request,'result.html',context={'data':result})
#     # return HttpResponse(result)
# def callist(request):
#     data = cal.objects.all()
#     return render(request,'list.html',context={'data':data})
#     # for i in data:
# # print(i.value_a,i.value_b,i.result)
# def deldata(request):
#     cal.objects.all().delete()
#     return HttpResponse('Data Deleted')
#公告页面
def index(request):
    return render(request,'index.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        #验证登录
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误')
            return redirect('login')


    return render(request,'login.html')
def forgot_password(request):
    return render(request, 'forgot_password.html')
def register(request):
    return render(request, 'register.html')
