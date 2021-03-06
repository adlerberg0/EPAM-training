# Generated by Django 3.1.4 on 2020-12-29 18:14

from django.db import migrations
from django.utils import timezone


def add_instances(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Student = apps.get_model("test_app", "Student")
    student = Student(first_name="Roman", last_name="Petrov")

    Teacher = apps.get_model("test_app", "Teacher")
    teacher = Teacher(first_name="Daniil", last_name="Shadrin")

    Homework = apps.get_model("test_app", "Homework")
    hw = Homework(
        text="test homework",
        created=timezone.now(),
        deadline=timezone.now(),
        teacher=teacher,
    )

    HomeworkResult = apps.get_model("test_app", "HomeworkResult")
    hw_result = HomeworkResult(
        solution="test solution for test homework",
        homework=hw,
        completed_by=student,
        checked_by=teacher,
    )
    student.save()
    teacher.save()
    hw.save()
    hw_result.save()


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_instances),
    ]
