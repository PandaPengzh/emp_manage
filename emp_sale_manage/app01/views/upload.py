from django.shortcuts import HttpResponse,render,redirect
from app01.utills.form import uploadModelForm
from app01.utills.pagination import Pagination
from app01.models import Boss
import os

def upload_list(request):
    object_query = Boss.objects.all()

    # 分页功能
    page_ojbect = Pagination(request,object_query,page_size=4)

    context = {
        "queryset":page_ojbect.queryset,
        "page_string":page_ojbect.html_data()
    }
    return render(request=request,template_name='upload_list.html',context=context)


def upload_add(request):
    """ 文件上传 """
    if request.method == 'GET':
        form = uploadModelForm()
        context = {
            "form":form
        }
        return render(request=request,template_name="upload_add.html",context=context)

    else:
        form = uploadModelForm(data=request.POST,files=request.FILES)
        # 数据有效
        if form.is_valid():
            # cleaned_data {'name': '小张', 'age': 88, 'img': <InMemoryUploadedFile: 12家居-可爱小姐姐.jpg (image/jpeg)>}
            img_object = form.cleaned_data.get('img') # 拿到img对象
            media_path = os.path.join('media',img_object.name)

            # 将数据存储到数据库中
            Boss.objects.create(
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                img=media_path,
            )

            # 将上传的图片存储到相应的文件夹
            with open(media_path,mode='wb') as f:
                for chunk in img_object.chunks():
                    f.write(chunk)

            return redirect('http://127.0.0.1:8000/upload/list')

        # 无效
        else:
            context = {
                "form":form
            }
            return render(request=request,template_name="upload_list.html",context=context)


def upload_delete(request,nid):
    if request.method == 'GET':
        Boss.objects.filter(id=nid).delete()
    return redirect('/upload/list/')


def upload_edit(request,nid):
    """ 编辑客户 """
    row_object = Boss.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = uploadModelForm(instance=row_object)
        return render(request,"upload_edit.html",{"form":form})

    else:
        form = uploadModelForm(data=request.POST,files=request.FILES)
        # 数据有效
        if form.is_valid():
            img_object = form.cleaned_data.get('img') # 拿到img对象
            media_path = os.path.join('media',img_object.name)

            # 将数据更新存储到数据库中
            Boss.objects.filter(id=nid).update(
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                img=media_path,
            )

            # 将上传的图片存储到相应的文件夹
            with open(media_path,mode='wb') as f:
                for chunk in img_object.chunks():
                    f.write(chunk)

            return redirect('http://127.0.0.1:8000/upload/list')

        # 无效
        else:
            context = {
                "form":form
            }
            return render(request=request,template_name="upload_edit.html",context=context)