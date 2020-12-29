from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Homework(models.Model):
    text = models.CharField(max_length=200)
    deadline = models.DateTimeField("hw deadline")
    created = models.DateTimeField("hw created")
    teacher = models.ForeignKey("test_app.Teacher", on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Student(Person):
    ...


class HomeworkResult(models.Model):
    solution = models.CharField(max_length=200)
    homework = models.ForeignKey("test_app.Homework", on_delete=models.CASCADE)
    completed_by = models.ForeignKey("test_app.Student", on_delete=models.CASCADE)
    checked_by = models.ForeignKey("test_app.Teacher", on_delete=models.CASCADE)

    def __str__(self):
        return self.solution


class Teacher(Person):
    ...
