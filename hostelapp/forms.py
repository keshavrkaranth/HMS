from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import *
from django import forms
from django.core import validators
import datetime

YEARS = [x for x in range(1990, 3000)]


class registrationForm(forms.Form):
    BRANCHES = [('CS', 'Computer Science'), ('IS', 'Information Science'), ('EC', 'Electronics And Communication'),
                ('EEE', 'Electrical And Electronics'), ('ME', 'Mecanical')]
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    Name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Branch = forms.ChoiceField(choices=BRANCHES)
    USN = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Phone_no = forms.CharField(
        max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Gender = forms.ChoiceField(choices=gender_choices)
    DOB = forms.DateField(widget=forms.SelectDateWidget(
        years=YEARS, attrs={'class': 'form-control'}))
    Father_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Father_mbl_no = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Username = forms.CharField(max_length=20, help_text=USN, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Confirm_Password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(registrationForm, self).clean()
        password = cleaned_data.get("password")
        phone = cleaned_data.get('Phone_no')
        fphone = cleaned_data.get('Father_mbl_no')
        confirm_password = cleaned_data.get("Confirm_Password")

        if len(phone)<10 or len(fphone) <10 or len(phone)>10 or len(fphone)>10:
            raise forms.ValidationError("Phone number should be 10 character long")

        if len(password) < 8:
            raise forms.ValidationError('Password must be 8 character long')

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Student.objects.all().filter(no_dues=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Student.objects.all().filter(no_dues=False))


class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(
        initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(
        initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    reason = forms.CharField(max_length=100, help_text='100 characters max.',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter Reason here'}))

    class Meta:
        model = Leave
        fields = [
            'start_date',
            'end_date',
            'reason']


class RepairForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['repair']


class RoomForm(forms.Form):
    choices = [('S', 'Single_Room'), ('D', 'Double_Room')]
    Room_No = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'placeholder': 'ex D1,S1'}))
    Room_Type = forms.ChoiceField(choices=choices)


class FeedbackForm(forms.Form):
    choice = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    Review = forms.CharField(max_length=255)
    rating = forms.ChoiceField(choices=choice)


class updateprofile(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['student_name', 'student_mbl_no', 'adress',
                  'father_name', 'father_mbl_no', 'USN', 'Branch', 'dob']

        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_mbl_no': forms.TextInput(attrs={'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_mbl_no': forms.TextInput(attrs={'class': 'form-control'}),
            'USN': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.TextInput(attrs={'class': 'form-control'}),
        }
