from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import client
from .models import User
from .models import UserExtension
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
# def page_not_found(request,exception):
#     return render(request, '404.html')
def home(request):
    return render(request,'home.html')
def index(request):
    datas = client.objects.all()[:1000]
    context = {
        'datas':datas
    }

    return render(request,'index.html', context=context)

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
            return redirect('user_login')
    return render(request,'login.html')
def forgot_password(request):
    return render(request, 'forgot_password.html')
def register(request):
    return render(request, 'register.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')
def client_table(request):
    datas = client.objects.all()
    context = {
        'datas':datas
    }
    return render(request,'table.html',context=context)
#用户管理
def user_manage(request):
    datas =User.objects.all()
    context = {
        'datas':datas
    }
    return render(request,'user_manage.html',context)

# 新增账号方法
@login_required
@permission_required('performance.manage_user', raise_exception=True)
def add_user(request):
    # 从前端获取填写用户信息
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
            is_superuser=is_superuser
        )
        user.extension.job_number = job_number
        user.extension.department = department
        user.extension.telephone = telephone
        user.save()
        # 写入成功提示
        messages.success(request, '用户增加成功')
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
    current_user_id = str(User.objects.get(id=request.user.id).id)
    # user_is_superuser = str(User.objects.filter(is_superuser=request.user.is_superuser).is_superuser)#修改人的superuser
    # current_is_superuser = str(User.objects.filter(job_number =job_number).is_superuser)

    if current_user_id == job_number:
        messages.error(request, '不可以删除当前登录的账号')
        return HttpResponse('error')
    else:
        user =UserExtension.objects.get(job_number=job_number)
        id = UserExtension.objects.get(job_number=job_number).user_id
        orgin =User.objects.get(id=id)
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
    job_number = request.POST.get('job_number')
    user_name = request.POST.get('user_name')
    name = request.POST.get('name')
    department = request.POST.get('department')
    telephone = request.POST.get('telephone')
    print(job_number,name)
    # 取出此账户并更新信息
    user = User.objects.get(id=change_id)
    user.extension.job_number = job_number
    user.username = user_name
    user.first_name = name
    user.extension.department = department
    user.extension.telephone = telephone

    user.save()
    # 写入成功提示
    messages.success(request, '用户信息修改成功')
    # 重载账号展示页面
    return redirect('user_manage')

def safe_clients(request):
    # datas = client.objects.filter(exited=)
    return render(request,'safe_clients.html')