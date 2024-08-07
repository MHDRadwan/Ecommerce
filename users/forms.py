from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from .models import Profile, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_of_origin = CountryField(blank_label='(select country)').formfield(widget=forms.Select(attrs={'class': 'form-control'}))
    country_of_residence = CountryField(blank_label='(select country)').formfield(widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    phone_number = PhoneNumberField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'gender', 'country_of_origin', 'country_of_residence', 'city', 'address', 'image', 'phone_number']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                address=self.cleaned_data.get('address'),
                country_of_origin=self.cleaned_data.get('country_of_origin'),
                country_of_residence=self.cleaned_data.get('country_of_residence'),
                city=self.cleaned_data.get('city'),
                image=self.cleaned_data.get('image') if self.cleaned_data.get('image') else 'profile_pics/placeholder.png',
                phone_number=self.cleaned_data.get('phone_number')
            )
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']




















