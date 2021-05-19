import re

from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import client
from .models import User
from .models import UserExtension
from .models import total_client
# from pycaret.classification import *

from Dog.apps import *
import numpy as np
import pandas as pd

# pd.options.display.max_rows = None
# pd.options.display.max_columns = None


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
# 公告页面
# def page_not_found(request,exception):
#     return render(request, '404.html')


def home(request):
    return render(request, 'home.html')


@login_required
def index(request):
    datas = client.objects.all()[:1000]
    user = request.user
    context = {
        'datas': datas,
        'user': user,
    }

    return render(request, 'index.html', context=context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # 验证登录
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误')
            return redirect('user_login')
    return render(request, 'login.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def register(request):
    return render(request, 'register.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def client_table(request):
    datas = client.objects.all()
    user = request.user
    context = {
        'datas': datas,
        'user': user,

    }
    return render(request, 'table.html', context=context)


# 用户管理
@login_required
def user_manage(request):
    if request.user.is_superuser:
        datas = User.objects.all()
        user = request.user
        context = {
            'datas': datas,
            'user': user
        }
        return render(request, 'user_manage.html', context=context)
    else:
        return render(request,'error.html')


# 新增账号方法
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def add_user(request):
    # 从前端获取填写用户信息
    email = str(request.POST.get('email')).strip()
    job_number = str(request.POST.get('job_number')).strip()
    name = str(request.POST.get('name')).strip()
    department = str(request.POST.get('department')).strip()
    telephone = str(request.POST.get('telephone')).strip()
    user_name = str(request.POST.get('user_name')).strip()
    password = str(request.POST.get('password')).strip()
    is_superuser = str(request.POST.get('is_superuser')).strip()

    # 保存用户
    try:
        user = User.objects.create_user(
            password=password,
            first_name=name,
            username=user_name,
            is_superuser=is_superuser,
            email=email
        )
        user.extension.job_number = job_number
        user.extension.department = department
        user.extension.telephone = telephone
        user.save()
        # 写入成功提示
        messages.success(request, '用户增加成功')
        return redirect('user_manage')
    except:
        # 写入失败提示
        messages.error(request, '用户增加失败')
        # 重载账号展示页面
        return redirect('user_manage')


# 删除账号方法
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def delete_user(request):
    job_number = str(request.POST.get('job_number')).strip()
    # user_name = str(request.POST.get('user_name')).strip()
    # current_user_id = str(User.objects.get(id=request.user.id).id)
    current_user_id = request.user
    # user_is_superuser = str(User.objects.filter(is_superuser=request.user.is_superuser).is_superuser)#修改人的superuser
    # current_is_superuser = str(User.objects.filter(job_number =job_number).is_superuser)

    if current_user_id == job_number:
        messages.error(request, '不可以删除当前登录的账号')
    else:
        user = UserExtension.objects.get(job_number=job_number)
        id = UserExtension.objects.get(job_number=job_number).user_id
        orgin = User.objects.get(id=id)
        #     user = User.objects.get(job_number=job_number)
        user.delete()
        orgin.delete()
        messages.success(request, '用户删除成功')
    return redirect('user_manage')


# 修改账户方法
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def change_user(request):
    # 从前端获取要修改的id
    change_id = request.POST.get('change_id')
    # 获取修改后的信息
    email = request.POST.get('email')
    job_number = request.POST.get('job_number')
    user_name = request.POST.get('user_name')
    name = request.POST.get('name')
    department = request.POST.get('department')
    telephone = request.POST.get('telephone')
    print(job_number, name)
    # 取出此账户并更新信息
    user = User.objects.get(id=change_id)
    if job_number != '':
        user.extension.job_number = job_number
    if user_name != '':
        user.username = user_name
    if name != '':
        user.first_name = name
    if email != '':
        user.email = email
    if department != '':
        user.extension.department = department
    if telephone != '':
        user.extension.telephone = telephone

    user.save()
    # 写入成功提示
    messages.success(request, '用户信息修改成功')
    # 重载账号展示页面
    return redirect('user_manage')

#安全客户界面
@login_required
def safe_clients(request):
    # datas = client.objects.filter(exited=)
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'safe_clients.html', context=context)


# 修改密码
@login_required
def change_passwd(request):
    old_password = request.POST.get('old_password').strip()
    new_password = request.POST.get('new_password').strip()
    new_password_again = request.POST.get('new_password_again').strip()
    user = request.user
    # 验证当前用户密码是否匹配用户输入的旧密码
    if not user.check_password(old_password):
        # 验证失败，写入验证失败提示
        return HttpResponse('旧密码有误，如遗忘请联系管理员修改')
        # messages.error(request, '旧密码有误，如遗忘请联系管理员修改')
        # 重载更改密码页面
        return redirect('change_user')
    if new_password != new_password_again:
        # 写入两次确认密码不同错误
        messages.error(request, '两次确认密码不同，请重新输入')
        # 重载更改密码页面
        return redirect('change_user')
    try:
        # 更新用户密码
        user.set_password(new_password)
        user.save()
    except:
        return HttpResponse('未知错误，请重试或重新登录尝试')
        # messages.error(request, '未知错误，请重试或重新登录尝试')
        return redirect('change_user')
    # 写入成功提示|
    return HttpResponse('''
    <h2>密码修改成功，请重新登录</h2>
    <a href=/user_login/>点击登陆<a>
    ''')
    # messages.success(request, '密码修改成功，请重新登录')
    # 注销该用户
    logout(request)
    # 重载登录界面
    return redirect('user_login')


#   删除客户
# @login_required
# @permission_required('performance.manage_user', raise_exception=True)
# def delete_client(request):
#     job_number = str(request.POST.get('job_number')).strip()
#     current_user_id = str(User.objects.get(id=request.user.id).id)
#
#
#     if current_user_id == job_number:
#         messages.error(request, '不可以删除当前登录的账号')
#         return HttpResponse('error')
#     else:
#         user = UserExtension.objects.get(job_number=job_number)
#         id = UserExtension.objects.get(job_number=job_number).user_id
#         orgin = User.objects.get(id=id)
#         #     user = User.objects.get(job_number=job_number)
#         user.delete()
#         orgin.delete()
#         messages.success(request, '用户删除成功')
#     return redirect('user_manage')
# 修改客户信息页面
@login_required
def clients_manage(request):
    datas = client.objects.all()[:1000]
    user = request.user
    context = {
        'datas': datas,
        'user': user,
    }
    return render(request, 'clients_manage.html', context=context)


# 删除客户信息
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def delete_clients(request):
    row_number = request.POST.get('row_number')
    id = request.POST.get('id')
    if row_number != '':
        client.objects.get(id=row_number).delete()
        messages.success(request, '删除客户信息成功')
    if id != '':
        client.objects.filter(customer_id=id).delete()
        messages.success(request, '删除客户信息成功')
    return redirect('clients_manage')


# 增加客户信息
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def add_clients(request):
    # 从前端获取填写用户信息
    CustomerID = request.POST.get('CustomerID')
    Surname = str(request.POST.get('Surname')).strip()
    CreditScore = request.POST.get('CreditScore')
    Geography = str(request.POST.get('Geography')).strip()
    Gender = str(request.POST.get('Gender')).strip()
    Age = request.POST.get('Age')
    Balance = request.POST.get('Balance')
    Tenure = request.POST.get('Tenure')
    NumOfProducts = request.POST.get('NumOfProducts')
    HasCrCard = request.POST.get('HasCrCard')
    IsActiveMember = request.POST.get('IsActiveMember')
    EstimatedSalary = request.POST.get('EstimatedSalary')
    Exited = request.POST.get('Exited')
    # 保存用户
    client.objects.create(
        customer_id=CustomerID,
        surname=Surname,
        credit_score=CreditScore,
        geography=Geography,
        gender=Gender,
        age=Age,
        balance=Balance,
        tenure=Tenure,
        num_of_products=NumOfProducts,
        has_cr_card=HasCrCard,
        is_active_member=IsActiveMember,
        estimated_salary=EstimatedSalary,
        exited=Exited
    )
    # 写入成功提示
    messages.success(request, '用户增加成功')
    # 写入失败提示
    # 重载账号展示页面
    return redirect('clients_manage')


# 修改客户信息
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def change_clients(request):
    # 从前端获取要修改的id
    RowNumber = request.POST.get('RowNumber')
    # 获取修改后的信息
    CustomerID = request.POST.get('CustomerID')
    Surname = str(request.POST.get('Surname')).strip()
    CreditScore = request.POST.get('CreditScore')
    Geography = str(request.POST.get('Geography')).strip()
    Gender = str(request.POST.get('Gender')).strip()
    Age = request.POST.get('Age')
    Balance = request.POST.get('Balance')
    Tenure = request.POST.get('Tenure')
    NumOfProducts = request.POST.get('NumOfProducts')
    HasCrCard = request.POST.get('HasCrCard')
    IsActiveMember = request.POST.get('IsActiveMember')
    EstimatedSalary = request.POST.get('EstimatedSalary')
    Exited = request.POST.get('Exited')
    # 取出此账户并更新信息
    clients = client.objects.get(id=RowNumber)
    if CustomerID != '':
        clients.customer_id = CustomerID
    if Surname != '':
        clients.surname = Surname
    if CreditScore != '':
        clients.credit_score = CreditScore
    if Geography != '':
        clients.geography = Geography
    if Gender != '':
        clients.gender = Gender
    if Age != '':
        clients.age = Age
    if Balance != '':
        clients.balance = Balance
    if Tenure != '':
        clients.tenure = Tenure
    if NumOfProducts != '':
        clients.num_of_products = NumOfProducts
    if HasCrCard != '':
        clients.has_cr_card = HasCrCard
    if IsActiveMember != '':
        clients.is_active_member = IsActiveMember
    if EstimatedSalary != '':
        clients.estimated_salary = EstimatedSalary
    if Exited != '':
        clients.exited = Exited
    clients.save()
    # 写入成功提示
    messages.success(request, '用户信息修改成功')
    # 重载账号展示页面
    return redirect('clients_manage')

@login_required
def exited_clients(request):
    user = request.user
    clients = client.objects.filter(exited=1)
    context = {
        'user': user,
        'datas': clients
    }
    return render(request, 'exited_clients.html', context=context)


@login_required
def charts(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'charts.html', context=context)

@login_required
def safe_clients(request):
    datas = total_client.objects.filter(client_0_Label=0)
    # clients = total_client.objects.filter(client_0_id=0)
    user = request.user
    context = {
        'user': user,
        'datas': datas
    }
    return render(request, 'safe_clients.html', context=context)
@login_required
def danger_clients(request):
    datas = total_client.objects.filter(client_1_Label=1)
    # clients = total_client.objects.filter(client_0_id=0)
    user = request.user
    context = {
        'user': user,
        'datas': datas
    }
    return render(request, 'danger_clients.html', context=context)

