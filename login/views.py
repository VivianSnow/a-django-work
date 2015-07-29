#coding=utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.forms import ModelForm 
from models import StudentInfo
from models import TeacherInfo
from models import StudentCourse
import django_tables2 as tables
from django_tables2 import RequestConfig
import csv
from captcha.fields import CaptchaField


class UserForm(forms.Form): 
    username = forms.CharField(label='学号',max_length=20, error_messages={'required': '请输入学号'},
                               widget=forms.TextInput(attrs={'class' : 'span12', 'placeholder' : '请输入学号'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class' : 'span12', 'placeholder' : '请输入密码'}), error_messages={'required': '请输入密码'})
    choice = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('student', '学生'), ('teacher', '教师')], error_messages={'required': '请选择身份'})
    captcha = CaptchaField(error_messages = {'required': '请输入验证码'})
    
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            human = True
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            type_ = uf.cleaned_data['choice']
            print type_
            if type_ == 'student':
                user = StudentInfo.objects.filter(student_ID__exact = username,password__exact = password)
            elif type_ == 'teacher':
                user = TeacherInfo.objects.filter(teacher_ID__exact = username,password__exact = password)
            if user:
                if type_ == 'student':
                    response = HttpResponseRedirect('/login/s-index/')
                elif type_ == 'teacher':
                    response = HttpResponseRedirect('/login/t-index/')
                response.set_cookie('username',username,3600)
                response.set_cookie('type_', type_, 3600)
                return response
            else:
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
            if user:
                for i in user: ans = i
                ans.password = newpassword
                ans.save()
                return render_to_response('s-change-password.html',{'form':form, 'change_success' : True},context_instance=RequestContext(req))
            else:
                return render_to_response('s-change-password.html',{'form':form, 'oldpassword_is_wrong' : True},context_instance=RequestContext(req))
            print oldpassword
    return render_to_response('s-change-password.html',{'form':form},context_instance=RequestContext(req))

def t_change_password(req):
    form = change_pwd_form(req.POST)
    if req.method == 'POST':
        if form.is_valid():
            username = req.COOKIES.get('username','')
            oldpassword = req.POST.get('oldpassword', '')
            newpassword = req.POST.get('newpassword1', '')
            user = TeacherInfo.objects.filter(teacher_ID = username,password__exact = oldpassword)
            if user:
                for i in user: ans = i
                ans.password = newpassword
                ans.save()
                return render_to_response('t-change-password.html',{'form':form, 'change_success' : True},context_instance=RequestContext(req))
            else:
                return render_to_response('t-change-password.html',{'form':form, 'oldpassword_is_wrong' : True},context_instance=RequestContext(req))
            print oldpassword
    return render_to_response('t-change-password.html',{'form':form},context_instance=RequestContext(req))

class s_grade_table(tables.Table):
    course_ID = tables.Column(verbose_name = u"课程名")
    course_grade = tables.Column()
    teacher_name = tables.Column(verbose_name = "授课教师", accessor='teacher_ID.teacher_name')
    class Meta:
        attrs = {"class": "table table-hover", 
                 "th" : "span3"}
        #model = StudentCourse
        #sequence = ("course_ID", "course_grade")
        
 
def s_grade_list(req):
    username = req.COOKIES.get('username','')
    t = s_grade_table(StudentCourse.objects.filter(student_ID__exact = username))
    RequestConfig(req).configure(t)
    #RequestConfig(req, paginate={"per_page": 1}).configure(t)
    return render(req, "s-grade-list.html", {'StudentInfo': t})

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

class update_grade_form(ModelForm):
    #course_ID = forms.CharField()
    class Meta:
        model = StudentCourse
        fields = ('course_ID', 'student_ID', 'course_grade')

class upload_grade_form(forms.Form):
    csv = forms.FileField(label = "请上传更改后的成绩文件")

def handle_uploaded_file(f, username):
    import os
    import time
    file_name = ""
    path = "media/"+ time.strftime('%Y%m%d/%H%M%S/')
    os.makedirs(path)
    file_name = file_name = path + f.name
    destination = open(file_name, 'w')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    reader = csv.reader(open(file_name))
    for i in reader:
        courseID =  i[0].split(' ')[0]
        user = StudentCourse.objects.filter(teacher_ID__exact = username, course_ID__exact = courseID, student_ID__exact = i[1])
        print user
        for j in list(user):
            ans = j
        ans.course_grade = i[2]
        ans.save()    
    
def t_grade_list(req):
    username = req.COOKIES.get('username','')
    #search = StudentCourse.objects.filter(teacher_ID__exact = username).get(course_ID__exact = 231)
    #print search
    form = update_grade_form(req.POST)#, instance = search)
    if req.method == 'POST':
        upload_form =upload_grade_form(req.POST, req.FILES)
        if req.POST.has_key('submit'):
            if form.is_valid():
                courseID = req.POST.get('course_ID', '')
                studentID = req.POST.get('student_ID', '')
                coursegrade = req.POST.get('course_grade', '')
                user = StudentCourse.objects.filter(teacher_ID__exact = username, course_ID__exact = courseID, student_ID__exact = studentID)
                ans = None
                for i in list(user): ans = i
                if ans:
                    ans.course_grade = coursegrade
                    ans.save()
                    return render_to_response('t-grade-list.html',{'form':form, 'change_success' : True,  "upload_form": upload_form},context_instance=RequestContext(req))
                else:
                    return render_to_response('t-grade-list.html',{'form':form, "upload_form": upload_form, 'not_exist' : True},context_instance=RequestContext(req))
            else:
                return render_to_response('t-grade-list.html',{'form':form, "upload_form": upload_form, 'not_finish': True},context_instance=RequestContext(req))
        elif req.POST.has_key('download'):
            response = HttpResponse(content_type='text/csv')
            #response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename="teacher.csv"'
            writer = csv.writer(response)
            search = StudentCourse.objects.filter(teacher_ID__exact = username).order_by("course_ID", "student_ID")
            for i in list(search):
                writer.writerow([i.course_ID, i.student_ID, i.course_grade])
            return response
        elif req.POST.has_key('upload'):
            if upload_form.is_valid():
                handle_uploaded_file(req.FILES.get('csv'), username)
    else:
        upload_form =upload_grade_form()
            
    return render_to_response('t-grade-list.html',{'form':form, "upload_form": upload_form},context_instance=RequestContext(req))

class choose_course_form(ModelForm):
    class Meta:
        model = StudentCourse
        fields = ('course_ID', )

class t_grade_table(tables.Table):
    course_ID = tables.Column(verbose_name = u"课程名")
    studentname = tables.Column(accessor='student_ID.student_name') 
    student_ID = tables.Column(verbose_name = "学号")
    classname = tables.Column(accessor='student_ID.class_ID.class_name') 
    #studentname = tables.Column(accessor='student_ID.student_name')
    # = tables.Column(verbose_name = "授课教师", accessor='teacher_ID.class_ID.class_name')
    course_grade = tables.Column()
    class Meta:
        attrs = {"class": "table table-hover"}
        #model = StudentCourse
        

def t_course_list(req):
    count = {}
    count['stat9'] = 0
    count['stat8'] = 0
    count['stat7'] = 0
    count['stat6'] = 0
    count['stat5'] = 0
    count['is_success'] = False
    form = choose_course_form(req.POST)
    if req.method == 'POST':
        if form.is_valid():
            username = req.COOKIES.get('username','')
            courseID = req.POST.get('course_ID', '')
            user = StudentCourse.objects.filter(teacher_ID__exact = username, course_ID__exact = courseID)
            table = t_grade_table(StudentCourse.objects.filter(teacher_ID__exact = username, course_ID__exact = courseID))
            RequestConfig(req).configure(table)
            print table
            for i in list(user):
                if i.course_grade >= 90: count['stat9'] += 1
                elif i.course_grade >= 80: count['stat8'] += 1
                elif i.course_grade >= 70: count['stat7'] += 1
                elif i.course_grade >= 60: count['stat6'] += 1
                else : count['stat5'] += 1
            count['form'] = form
            count['is_success'] = True
            count['table'] = table
            return render(req, 't-course-list.html', count)
        else:
            return render_to_response('t-course-list.html',{'form':form, 'not_exist' : True, 'table' : table, 'is_success' : True},context_instance=RequestContext(req))
    return render(req, 't-course-list.html', {'form':form})

def logout(req):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('password')
    response.delete_cookie('choice')
    return response
