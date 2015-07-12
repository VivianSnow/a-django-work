#coding=utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import StudentInfo
from models import TeacherInfo

from models import StudentCourse

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
            if type_ == 'student':
                user = StudentInfo.objects.filter(student_ID__exact = username,password__exact = password)
            elif type_ == 'teacher':
                user = TeacherInfo.objects.filter(teacher_ID__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                if type_ == 'student':
                    response = HttpResponseRedirect('/login/s-index/')
                elif type_ == 'teacher':
                    response = HttpResponseRedirect('/login/t-index/')
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
    user = StudentInfo.objects.filter(student_ID__exact = username)
    for i in list(user): ans = i.student_name
    return render_to_response('s-index.html', {'username':ans})

def s_profile(req):
    username = req.COOKIES.get('username','')
    user = StudentInfo.objects.filter(student_ID__exact = username)
    for i in list(user): ans = i
    print type(ans.student_birth)
    t = {'student_ID':ans.student_ID, 'student_name':ans.student_name, 'student_birth':ans.student_birth,
            'student_gender':ans.student_gender, 's_department' : ans.s_department, 'class_ID':ans.class_ID}
    return render_to_response('s-profile.html', t)

class change_pwd_form(forms.Form):
    oldpassword = forms.CharField(label = " 原密码", error_messages={'required': '请输入原密码'},
                                  widget=forms.PasswordInput(attrs={'placeholder' : '原密码'}),)
    newpassword1 = forms.CharField(label = " 新密码", error_messages={'required': '请输入新密码'},
                                  widget=forms.PasswordInput(attrs={'placeholder' : '新密码'}),)
    newpassword2 = forms.CharField(label = "确认密码", error_messages={'required': '请再次输入新密码'},
                                  widget=forms.PasswordInput(attrs={'placeholder' : '确认密码'}),)
    def clean(self):
        if not self.is_valid():
            print 3213213213
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(change_pwd_form, self).clean()
        return cleaned_data

def s_change_password(req):
    form = change_pwd_form(req.POST)
    if req.method == 'POST':
        if form.is_valid():
            username = req.COOKIES.get('username','')
            oldpassword = req.POST.get('oldpassword', '')
            newpassword = req.POST.get('newpassword1', '')
            user = StudentInfo.objects.filter(student_ID__exact = username,password__exact = oldpassword)
            for i in user: ans = i
            ans.password = newpassword
            ans.save()
            if user:
                
                return render_to_response('s-change-password.html',{'form':form, 'change_success' : True},context_instance=RequestContext(req))
            else:
                return render_to_response('s-change-password.html',{'form':form, 'oldpassword_is_wrong' : True},context_instance=RequestContext(req))
            print oldpassword
    return render_to_response('s-change-password.html',{'form':form},context_instance=RequestContext(req))
    
def s_grade_list(req):
    username = req.COOKIES.get('username','')
    return render(req, "s-grade-list.html", {'StudentInfo':StudentCourse.objects.filter(student_ID__exact = username)})


def t_index(req):
    username = req.COOKIES.get('username','')
    user = TeacherInfo.objects.filter(teacher_ID__exact = username)
    for i in list(user): ans = i.teacher_name
    return render_to_response('t-index.html', {'username':ans})

def t_profile(req):
    username = req.COOKIES.get('username','')
    user = TeacherInfo.objects.filter(teacher_ID__exact = username)
    for i in list(user): ans = i
    t = {'teacher_ID':ans.teacher_ID, 'teacher_name':ans.teacher_name, 't_department':ans.t_department}
    return render_to_response('t-profile.html', t)

def logout(req):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('password')
    response.delete_cookie('choice')
    return response
