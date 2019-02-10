from django import forms

from .models import Request
from django.utils import timezone

class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ('roll','parent_email','venue','date','end_date','time','end_time','subject', 'description',)
        widgets = {'date': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
                   'time': forms.TimeInput(attrs={'type': 'text', 'class': 'timepicker'})}
    def clean_date(self):
        """Check if the date is less than the current date. If so, raise an error."""
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("Date should not be before today's date.",
                                        code="date_in_past")
        return date

    def clean_time(self):
        """Check that if the date is the current date, the time is not the current time. If so,
            raise an error."""
        time = self.cleaned_data.get('time')
        date = self.cleaned_data.get('date')
        if time:
            if date < timezone.now().date():
                raise forms.ValidationError("Time should not be a time that has already passed.",
                                                code="time_in_past")
        return time
