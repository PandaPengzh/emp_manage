from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt  # post表单验证
from django.http import JsonResponse                  # 序列化
from app01.utills.form import OrderModelForm
from app01.models import Order
from app01.utills.pagination import Pagination 
from datetime import datetime
import random


def order_list(request):
    """ 点击弹窗展示 """
    # 数据
    queryset = Order.objects.all()
    # 分页
    page_object = Pagination(request,page_size=8,queryset=queryset)

    form = OrderModelForm()
    context = {
        "form":form,
        "queryset":page_object.queryset,
        "page_string":page_object.html_data()
    }
    

    return render(request=request,template_name='order_list.html',context=context)

@csrf_exempt
def order_add(request):
    """ 添加订单到数据库 """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # oid 字段自动生成
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000,9999))
        form.save()
        return JsonResponse({"status":True})
    else:
        return JsonResponse({"status":False,"error":form.errors})

def order_delete(request):
    """删除订单"""
    # req = request # <WSGIRequest: GET '/order/delete/?uid=1'>
    # get = request.GET  # <QueryDict: {'uid': ['1']}>  querydict字典对象

    # 获取到字段对应的id
    uid = request.GET.get('uid')
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({
            "status":False,
            "error":"删除失败，数据不存在。"
        })
    else:
        Order.objects.filter(id=uid).delete()  # 删除对应的字段
        return JsonResponse({'status':True})

def order_edit(request):
    uid = request.GET.get('uid')
    exists = Order.objects.filter(id=uid).exists()
    if exists:
        dict_data = Order.objects.filter(id=uid).values('title','price','status','emp','category').first()
        data = {
            'status':True,
            'data':dict_data
        }
        return JsonResponse(data)

    else:
        data = {
            'status':False,
            'error':"数据不存在"
        }
        return JsonResponse(data)

@csrf_exempt
def order_editsave(request):
    """ 将编辑的数据提交到数据库 """
    uid = request.GET.get('uid')
    form = OrderModelForm(data=request.POST)
    
    dict_data=request.POST.dict()  # 转为字典形式
    if form.is_valid():
        Order.objects.filter(id=uid).update(**dict_data)  # 更新字段
        data = {
            'status':True,
        }
        return JsonResponse(data)

    else:
        data = {
            'status':False,
            'error':form.errors
        }
        return JsonResponse(data)



    