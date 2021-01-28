import csv
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_stub.settings")
django.setup()

from test_app.models import Homework, HomeworkResult, Student, Teacher  # noqa

# this script gets only the first element from the QuerySet
if __name__ == "__main__":
    model_list = [Student, Teacher, Homework, HomeworkResult]
    for model in model_list:

        model = model.objects.all()[0]
        model_fields = model._meta.fields + model._meta.many_to_many
        field_names = [field.name for field in model_fields]

        with open(f"test{str(model)}.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            csv_writer.writerow(field_names)
            row = []
            for field in field_names:
                value = getattr(model, field)
                row.append(value)
            csv_writer.writerow(row)
