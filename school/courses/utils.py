from datetime import datetime
from django.db import models
from .models import Student, Product, Group


def base_distribution(student: Student, product: Product) -> models.Model:
    max = product.max_users
    groups = Group.objects.filter(product=product).annotate(cnt=models.Count('students')).order_by("-cnt")
    print(groups, student)
    if groups:
        for group in groups:
            if group.cnt < max:
                group.students.add(student)
                group.save()
                return group
    new_group = Group.objects.create(name=f'Group {groups.count() + 1} for product {product.name}', product=product)
    new_group.students.add(student)
    new_group.save()
    return new_group


def redistribution(product: Product):
    if datetime.now(product.start_datetime.tzinfo) < product.start_datetime:
        all_students = list(Student.objects.filter(stud_groups__product=product))
        total_students = len(all_students)
        groups = list(Group.objects.filter(product=product))
        for group in groups:
            group.students.clear()
        total_groups = len(groups)
        min = product.min_users
        if total_students // min > total_groups:
            maximum_number_groups = total_groups
        else:
            maximum_number_groups = total_students // min
            print(maximum_number_groups)
        for i, student in enumerate(all_students):
            group = groups[i % maximum_number_groups]
            group.students.add(student)
        for group in groups:
            group.save()
