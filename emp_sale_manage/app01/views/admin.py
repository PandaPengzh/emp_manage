from django.shortcuts import render,HttpResponse,redirect
from django.utils.safestring import mark_safe  # 标记安全字符串
from app01.utills.pagination import Pagination
from app01.utills.form import AdminModelForm,AdminResetModelForm
from app01 import models

# Create your views here.

# 管理员管理
def admin_list(request):
    """ 管理员列表 """
    queryset = models.Admin.objects.all()

    # ---------分页功能实现-----------
    page_object = Pagination(request,queryset,page_size=2)

    context = {
        'queryset':page_object.queryset,
        'page_string':page_object.html_data()
    }


    return render(request,'admin_list.html',context)


def admin_modelform_add(request):
    """添加管理员(modelform版)"""
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request,"admin_modelform_add.html",{"form":form})
        
    else:
        form = AdminModelForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/admin/list/')
        else:
            return render(request,"admin_modelform_add.html",{"form":form})

def admin_delete(request,nid):
    """ 删除管理员 """
    if request.method == 'GET':
        models.Admin.objects.filter(id=nid).delete()

        # 重定向
        return redirect('http://127.0.0.1:8000/admin/list/')

def admin_edit(request,nid):
    """ 编辑管理员 """
    if request.method == 'GET':
        row_object = models.Admin.objects.filter(id=nid).first()
        return render(request,"admin_edit.html",{'row_object':row_object})

    else:
        new_username = request.POST.get("username")
        new_password = request.POST.get("password")
        models.Admin.objects.filter(id=nid).update(username=new_username,password=new_password)
        
        # page = math.ceil(nid/2)
        # 重定向
        return redirect('http://127.0.0.1:8000/admin/list/')

def admin_reset(request,nid):
    """ 重置密码(modelform版) """
    row_object = models.Admin.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = AdminResetModelForm()  # instance字段可以指定input中,进去的value值 
        return render(request,"admin_modelform_reset.html",{"form":form,"nid":nid})
        
    else:
        form = AdminResetModelForm(data=request.POST,instance=row_object) # 此处添加一个instance就可以覆盖以前的密码

        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/admin/list/')
        else:
            return render(request,"admin_modelform_reset.html",{"form":form,"nid":nid})






















