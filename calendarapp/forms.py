from django.forms import ModelForm, DateInput

from accounts.models import Account
from cabinet_tutors.models import MyStudent
from calendarapp.models import Event, EventMember
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        labels = {'title': 'Название', 'description': 'Описание', 'start_time': 'Начало',

                  'end_time': 'Конец'}

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название события"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Описание события",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = self.fields['user'].queryset.filter(tutor=current_user)
    user = forms.ModelChoiceField(
        label='Необходимо выбрать ученика',
        queryset=MyStudent.objects.all(),
    )
    class Meta:
        model = EventMember
        fields = ["user"]
