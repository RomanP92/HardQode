from django.db import models
from django.contrib.auth.models import User


class SchoolAbstract(models.Model):
    class Meta:
        abstract = True

    date_creation = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Изменен", auto_now=True)


class SchoolProfileAbstract(SchoolAbstract):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=20, verbose_name="Фамилия")


class Product(SchoolAbstract):
    name = models.CharField(max_length=50, verbose_name="Название")
    start_datetime = models.DateTimeField(verbose_name="Дата и время старта")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    min_users = models.IntegerField(verbose_name="Минимум пользователей в группе")
    max_users = models.IntegerField(verbose_name="Максимум пользователей в группе")
    creator = models.ForeignKey("Creator", on_delete=models.PROTECT, related_name='products')

    class Meta:
        verbose_name_plural = 'Продукты'
        verbose_name = 'Продукт'

    def __str__(self):
        return self.name


class Lesson(SchoolAbstract):
    name = models.CharField(max_length=50, verbose_name="Название")
    link = models.URLField(verbose_name="Ссылка")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'

    def __str__(self):
        return self.name


class Group(SchoolAbstract):
    name = models.CharField(max_length=50, verbose_name="Название")
    students = models.ManyToManyField('Student', related_name='stud_groups', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_groups')

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'

    def __str__(self):
        return self.name


class Student(User):
    class Meta:
        verbose_name_plural = 'Студенты'
        verbose_name = 'Студент'

    def __str__(self):
        return self.username


class Creator(SchoolProfileAbstract):
    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Access(SchoolAbstract):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='prod_accesses')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accesses')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'product')
        verbose_name_plural = 'Доступы'
        verbose_name = 'Доступ'

    def __str__(self):
        return f"{self.student.first_name} - {self.product.name}"
