from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:product_id>/lessons/', views.LessonsListView.as_view(), name='lessons-list'),
]
