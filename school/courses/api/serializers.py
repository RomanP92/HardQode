import datetime
from rest_framework import serializers
from courses.models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'start_date', 'creator', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_start_date(self, obj):
        return obj.start_datetime.strftime('%d-%m-%Y')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'link']
