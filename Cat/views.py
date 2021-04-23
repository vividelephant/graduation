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
from .models import client_0
from .models import client_1
# from pycaret.classification import *


import numpy as np
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None


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
    datas = User.objects.all()
    user = request.user
    context = {
        'datas': datas,
        'user': user
    }
    return render(request, 'user_manage.html', context=context)


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
    if id != '':
        client.objects.filter(customer_id=id).delete()
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
    messages.error(request, '用户增加失败')
    # 重载账号展示页面
    return redirect('')


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


# #处理
# def DfPrepPipeline(df_predict, df_train_Cols, minVec, maxVec):
#     df_predict['BalanceSalaryRatio'] = df_predict.Balance / df_predict.EstimatedSalary
#     df_predict['TenureByAge'] = df_predict.Tenure / (df_predict.Age - 18)
#     df_predict['CreditScoreGivenAge'] = df_predict.CreditScore / (df_predict.Age - 18)
#     continuous_vars = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary',
#                        'BalanceSalaryRatio',
#                        'TenureByAge', 'CreditScoreGivenAge']
#     cat_vars = ['HasCrCard', 'IsActiveMember', "Geography", "Gender"]
#     df_predict = df_predict[['Exited'] + continuous_vars + cat_vars]
#     df_predict.loc[df_predict.HasCrCard == 0, 'HasCrCard'] = -1
#     df_predict.loc[df_predict.IsActiveMember == 0, 'IsActiveMember'] = -1
#     lst = ["Geography", "Gender"]
#     remove = list()
#     for i in lst:
#         for j in df_predict[i].unique():
#             df_predict[i + '_' + j] = np.where(df_predict[i] == j, 1, -1)
#         remove.append(i)
#     df_predict = df_predict.drop(remove, axis=1)
#     L = list(set(df_train_Cols) - set(df_predict.columns))
#     for l in L:
#         df_predict[str(l)] = -1
#     df_predict[continuous_vars] = (df_predict[continuous_vars] - minVec) / (maxVec - minVec)
#     df_predict = df_predict[df_train_Cols]
#     return df_predict


# def maxclass(request):
#     df = pd.read_csv('/Users/mac/Desktop/graduation/Churn_Modelling.csv', delimiter=',')
#     df = df.drop(["RowNumber", "CustomerId", "Surname"], axis = 1)
#     #分为%80训练集
#     df_train = df.sample(frac=0.8,random_state=200)
#     df_test = df.drop(df_train.index)
#     #添加之前可视化不相关变量的比值。
#     df_train['BalanceSalaryRatio'] = df_train.Balance/df_train.EstimatedSalary
#     df_train['TenureByAge'] = df_train.Tenure/(df_train.Age)
#     df_train['CreditScoreGivenAge'] = df_train.CreditScore/(df_train.Age)
#     #用之前分的训练集和测试集取得maxVec和minVec
#     continuous_vars = ['CreditScore',  'Age', 'Tenure', 'Balance','NumOfProducts', 'EstimatedSalary', 'BalanceSalaryRatio',
#                     'TenureByAge','CreditScoreGivenAge']
#     cat_vars = ['HasCrCard', 'IsActiveMember','Geography', 'Gender']
#     df_train = df_train[['Exited'] + continuous_vars + cat_vars]
#     df_train.loc[df_train.HasCrCard == 0, 'HasCrCard'] = -1
#     df_train.loc[df_train.IsActiveMember == 0, 'IsActiveMember'] = -1
#     lst = ['Geography', 'Gender']
#     remove = list()
#     for i in lst:
#         if (df_train[i].dtype == np.str or df_train[i].dtype == np.object):
#             for j in df_train[i].unique():
#                 df_train[i+'_'+j] = np.where(df_train[i] == j,1,-1)
#             remove.append(i)
#     df_train = df_train.drop(remove, axis=1)
#     minVec = df_train[continuous_vars].min().copy()
#     maxVec = df_train[continuous_vars].max().copy()
#     df_train[continuous_vars] = (df_train[continuous_vars]-minVec)/(maxVec-minVec)
#     ##main
#     test= pd.read_csv('/Users/mac/Desktop/graduation/test.csv')
#     ##测试df
#     df1 = {'CreditScore':[1],'Geography':['France'],'Gender':['Female'],'Age':[50],'Tenure':[1],'Balance':[1],'NumOfProducts':[1]
#                 ,'HasCrCard':[1],'IsActiveMember':[1],'EstimatedSalary':[1],'Exited':[1]}
#     df1_df = pd.DataFrame(df1)
#     a = DfPrepPipeline(df1_df,df_train.columns,minVec,maxVec)#原始函数特征工程
#     aa = test.append(a)
#     #读取模型pkl
#     # setup(data = test, target = 'Exited')
#     # setup(data=test,target='Exited')
#     # df_predict = load_model('Final Xgboost Model 20200723')
#
#     df_predict = load_model('/Users/mac/Desktop/graduation/gbc,rf,lightgbm_meta=ada.pkl')
#     deploy_model(df_predict,)
#     pre = predict_model(df_predict,data=aa)
#     print(pre.iloc[-1,-2])
#     if pre.iloc[-1,-2] == 0:
#         # return '客户对我们很满意'
#         print('客户对我们很满意')
#     else:
#         # return '客户对我们有些失望，要想办法挽留客户'
#         print('客户对我们有些失望，要想办法挽留客户')
#
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


def all_delete(request):
    a = client_1.objects.values("id")
    for i in a:
        print(i)
    # for i in
    # c = client.objects.get(id=1).Score
    # return HttpResponse(a)


# 整合client三张表的一次性工具方法
# def get_total_client(request):
#     from .models import client, client_1, client_0, total_client
#
#     for temp_id in range(1, 10001):
#         # 取出client中的数据
#         try:
#             client_id = client.objects.get(id=temp_id).id
#             customer_id = client.objects.get(id=temp_id).customer_id
#             surname = client.objects.get(id=temp_id).surname
#             credit_score = client.objects.get(id=temp_id).credit_score
#             geography = client.objects.get(id=temp_id).geography
#             gender = client.objects.get(id=temp_id).gender
#             age = client.objects.get(id=temp_id).age
#             tenure = client.objects.get(id=temp_id).tenure
#             balance = client.objects.get(id=temp_id).balance
#             num_of_products = client.objects.get(id=temp_id).num_of_products
#             has_cr_card = client.objects.get(id=temp_id).has_cr_card
#             is_active_member = client.objects.get(id=temp_id).is_active_member
#             estimated_salary = client.objects.get(id=temp_id).estimated_salary
#             exited = client.objects.get(id=temp_id).exited
#             Label = client.objects.get(id=temp_id).Label
#             Score = client.objects.get(id=temp_id).Score
#         except:
#             client_id = None
#             customer_id = None
#             surname = None
#             credit_score = None
#             geography = None
#             gender = None
#             age = None
#             tenure = None
#             balance = None
#             num_of_products = None
#             has_cr_card = None
#             is_active_member = None
#             estimated_salary = None
#             exited = None
#             Label = None
#             Score = None
#
#         # 取出client_0的数据
#         try:
#             client_0_id = client_0.objects.get(id=temp_id).id
#             client_0_Label = client_0.objects.get(id=temp_id).Label
#             client_0_Score = client_0.objects.get(id=temp_id).Score
#         except:
#             client_0_id = None
#             client_0_Label = None
#             client_0_Score = None
#
#         # 取出client_1的数据
#         try:
#             client_1_id = client_1.objects.get(id=temp_id).id
#             client_1_Label = client_1.objects.get(id=temp_id).Label
#             client_1_Score = client_1.objects.get(id=temp_id).Score
#         except:
#             client_1_id = None
#             client_1_Label = None
#             client_1_Score = None
#
#         total_client.objects.create(
#             client_id=client_id,
#             customer_id=customer_id,
#             surname=surname,
#             credit_score=credit_score,
#             geography=geography,
#             gender=gender,
#             age=age,
#             tenure=tenure,
#             balance=balance,
#             num_of_products=num_of_products,
#             has_cr_card=has_cr_card,
#             is_active_member=is_active_member,
#             estimated_salary=estimated_salary,
#             exited=exited,
#             Label=Label,
#             Score=Score,
#             client_0_id=client_0_id,
#             client_0_Label=client_0_Label,
#             client_0_Score=client_0_Score,
#             client_1_id=client_1_id,
#             client_1_Label=client_1_Label,
#             client_1_Score=client_1_Score,
#         )
#         print(temp_id)
#     return HttpResponse('success')
