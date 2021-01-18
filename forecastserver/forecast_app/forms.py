from django import forms


class DateRangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        years = kwargs.pop("years", None)
        super(DateRangeForm, self).__init__(*args, **kwargs)
        if years:
            # calculate the list of years based on user's information and the rules you have
            # e.g. years = range(2010, 2016)
            self.fields["min_date"] = forms.DateField(
                label="Min date", widget=forms.SelectDateWidget(years=years)
            )
            self.fields["max_date"] = forms.DateField(
                label="Min date", widget=forms.SelectDateWidget(years=years)
            )
