from django.contrib import admin
from .models import Product, Student, Lesson, Group, Creator, Access


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'start_datetime', 'creator']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'product']


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ['product', 'student']
