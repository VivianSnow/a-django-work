from django.db import models
from django.contrib import admin
class Users(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username','password')

admin.site.register(Users, UsersAdmin)

TOPIC_CHOICES = (
    ('leve1', u'student'),
    ('leve2', u'teacher'),
)

