import datetime

from django.test import TestCase
from forecast_app.forms import DateRangeForm


class DataRangeFormTest(TestCase):
    def test_date_range_form_fields_label(self):
        form = DateRangeForm(years=list(range(2010, 2022)))

        self.assertTrue(form.fields["min_date"].label == "Min date")
        self.assertTrue(form.fields["max_date"].label == "Max date")

    def test_date_range_form_with_wrong_dates(self):
        min_date = datetime.date.today()
        max_date = datetime.date.today() - datetime.timedelta(days=1)

        form = DateRangeForm(
            data={"min_date": min_date, "max_date": max_date},
            years=list(range(2010, 2022)),
            auto_id=False,
        )
        self.assertFalse(form.is_valid())

    def test_date_range_form_with_correct_dates(self):
        min_date = datetime.date.today() - datetime.timedelta(days=1)
        max_date = datetime.date.today()

        form = DateRangeForm(
            data={"min_date": min_date.isoformat(), "max_date": max_date.isoformat()},
            years=list(range(2010, 2022)),
            auto_id=False,
        )
        self.assertTrue(form.is_valid())

    def test_date_range_form_with_equals_dates(self):
        min_date = datetime.date.today()
        max_date = datetime.date.today()

        form = DateRangeForm(
            data={"min_date": min_date.isoformat(), "max_date": max_date.isoformat()},
            years=list(range(2010, 2022)),
            auto_id=False,
        )
        self.assertTrue(form.is_valid())
