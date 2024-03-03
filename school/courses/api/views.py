from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Product, Lesson, Access
from courses.api.serializers import ProductSerializer, LessonSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        access = Access.objects.filter(product_id=product_id, student_id=request.user.id).exists()
        if not product or not access:
            return Response({'detail': 'Access denied or product not found.'}, status=status.HTTP_403_FORBIDDEN)
        lessons = Lesson.objects.filter(product=product)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
