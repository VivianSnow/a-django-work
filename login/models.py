# -*- coding: utf8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.hashers import make_password

class StudentInfo(models.Model):
    student_ID = models.IntegerField(primary_key = True, verbose_name = "学号")
    student_name = models.CharField(max_length = 20, verbose_name = "姓名")
    student_birth = models.DateField(verbose_name = "生日")
    student_gender = models.CharField(max_length = 6, choices = ((u'male', '男'), (u'female', '女'),), verbose_name = "性别")
    s_department = models.CharField(max_length = 20, verbose_name = "学院")
    password = models.CharField(max_length = 40)#, default = make_password("0000", None, 'pbkdf2_sha256'))
    class_ID = models.ForeignKey('ClassInfo')
    
    def __unicode__(self):
        return str(self.student_ID)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_ID','student_name', 'student_birth', 'student_gender', 's_department', 'class_ID')


class TeacherInfo(models.Model):
    teacher_ID = models.IntegerField(primary_key = True, verbose_name = "教工号")
    teacher_name = models.CharField(max_length = 20, verbose_name = "姓名")
    t_department = models.CharField(max_length = 20, verbose_name = "学院")
    password = models.CharField(max_length = 40)#, default = make_password("0000", None, 'pbkdf2_sha256'))

    def __unicode__(self):
        return str(self.teacher_ID)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_ID','teacher_name', 't_department')

class ClassInfo(models.Model):
    class_ID = models.CharField(max_length = 10, primary_key = True, verbose_name = "班级号")
    class_name = models.CharField(max_length = 20, verbose_name = "班级名")

    def __unicode__(self):
        return self.class_ID
    
    
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_ID', 'class_name')

class CourseInfo(models.Model):
    course_ID = models.CharField(max_length = 3, primary_key = True, verbose_name = "课程号")
    course_name = models.CharField(max_length = 20, verbose_name = "课程名称")
    semester = models.CharField(max_length = 20, verbose_name = "授课学期")
    teacher_ID = models.ForeignKey('TeacherInfo')

    def __unicode__(self):
        return '%s %s' %(self.course_ID, self.course_name)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_ID', 'course_name', 'semester')

class StudentCourse(models.Model):
    student_ID = models.ForeignKey('StudentInfo')
    course_ID = models.ForeignKey('CourseInfo')
    teacher_ID = models.ForeignKey('TeacherInfo')
    course_grade = models.IntegerField(null = True, blank = True, verbose_name = "成绩")

    def __unicode__(self):
        return str(self.course_grade)

    class Meta:  
        unique_together = ('student_ID', 'course_ID', 'teacher_ID')

class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student_ID', 'course_ID', 'teacher_ID', 'course_grade')
    
admin.site.register(StudentInfo, StudentAdmin)
admin.site.register(TeacherInfo, TeacherAdmin)
admin.site.register(ClassInfo, ClassAdmin)
admin.site.register(CourseInfo, CourseAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
