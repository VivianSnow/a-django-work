#coding=utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import Users

from models import TOPIC_CHOICES

#表单
class UserForm(forms.Form): 
    username = forms.CharField(label='学号',max_length=20, error_messages={'required': '请输入学号'})
    password = forms.CharField(label='密码',widget=forms.PasswordInput(), error_messages={'required': '请输入密码'})
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=[('student', '学生'), ('teacher', '教师')], error_messages={'required': '请选择身份'})


#登陆
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            type_ = uf.cleaned_data['choice']
            print type_
            #获取的表单数据与数据库进行比较
            user = Users.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/login/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                response.set_cookie('type_', type_, 3600)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

#登陆成功
def index(req):
    username = req.COOKIES.get('username','')
    return render_to_response('index.html' ,{'username':username})
