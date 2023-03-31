from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.utills.form import LoginForm
from app01.utills.code import check_code
from io import BytesIO



def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()

        return render(request,"login.html",{"form":form})
    
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid(): # 数据输入有效时
            # 1、拿到用户输入的数据
            # print(form.cleaned_data)  # 能拿到用户输入的用户名和密码和验证码  {'username': 'root', 'password': '1111', 'code':'xxx'}
            user_input_code = form.cleaned_data.pop('code')  # 因为数据库中没有code这个字段，所以需要干掉它,pop删除这个字段，并获取到对应的值

            # 2、验证码的校验
            code = request.session.get('image_code',"")  # 从session中取值
            if code.upper() != user_input_code.upper():  # 转大写
                form.add_error("code","验证码错误")
                return render(request, 'login.html', {"form":form})

            # 3、用户名和密码的校验
            admin_object = models.Admin.objects.filter(**form.cleaned_data).first()   
            if admin_object:  # 用户名和密码正确
                # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
                request.session["info"] = {'id': admin_object.id, 'username': admin_object.username}
                # 设置session可以保存7天
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('http://127.0.0.1:8000/admin/list/')
            else:
                form.add_error("password","用户名或密码错误")
                return render(request,'login.html',{"form":form})

        else:
            return render(request,"login.html",{"form":form})
        

def logout(request):
    """ 注销 """
    request.session.clear()

    return redirect('http://127.0.0.1:8000/login/')  # 回到登录页面


def code(request):
    """ 图片验证码 """
    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时，超时后image_code为空
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')   # 图片以二进制的形式存储在内存中
    # print(code_string)
    return HttpResponse(stream.getvalue())

        
        

