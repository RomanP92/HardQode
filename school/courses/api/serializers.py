"""
    2. Реализовать API на список продуктов, доступных для покупки,
которое бы включало в себя основную информацию о продукте и количество уроков,
которые принадлежат продукту. **(2 балла)**

    3. Реализовать API с выведением списка уроков по конкретному продукту,
к которому пользователь имеет доступ. **(1 балл)**.

        Необходимо отобразить список всех продуктов на платформе,
        к каждому продукту приложить информацию:

    1. Количество учеников занимающихся на продукте.
    2. На сколько % заполнены группы? (среднее значение по количеству участников
        в группах от максимального значения участников в группе).
    3. Процент приобретения продукта 
        (рассчитывается исходя из количества полученных доступов к продукту
        деленное на общее количество пользователей на платформе).

********Доступ пользователя к списку уроков контролируется во views*********

"""

from django.db.models import Count
from rest_framework import serializers
from courses.models import Product, Lesson, Student


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    all_students = serializers.SerializerMethodField()
    avg_filling = serializers.SerializerMethodField()
    popularity_of_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'start_date', 'creator', 'lessons_count', 'all_students', 'avg_filling',
                  'popularity_of_product']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_start_date(self, obj):
        return obj.start_datetime.strftime('%d-%m-%Y')

    def get_all_students(self, obj):
        return obj.prod_groups.filter(product=obj) \
            .annotate(unique_students=Count('students', distinct=True)) \
            .aggregate(total=Count('students', distinct=True))['total']

    def get_avg_filling(self, obj):
        all_students = self.get_all_students(obj)
        max = obj.max_users
        all_group = obj.prod_groups.filter(product=obj).count()
        avg = int(all_students / (max * all_group) * 100)
        return f'{avg} %'

    def get_popularity_of_product(self, obj):
        product_accesses = obj.accesses.filter(product=obj).aggregate(total=Count('student'))['total']
        all_students = Student.objects.count()
        popularity = int(product_accesses / all_students * 100) if all_students > 0 else 0
        return f"{popularity} %"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'link']
