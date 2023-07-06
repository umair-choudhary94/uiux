from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class creator_signup_form(UserCreationForm):
	# ID_No = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Student ID No.' }),required=True,max_length=30)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first name'}),required=True,max_length=30)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last name'}),required=True,max_length=30)
	email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email ID'}),required=True,max_length=30)
	# department = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter department'}),required=True,max_length=30)
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),required=True,max_length=30)
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required=True,max_length=30)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}),required=True,max_length=30)

	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

	def clean_confirm_password(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password != confirm_password:
			raise forms.ValidationError("Password Mismatch")
		return confirm_password


class viewer_signup_form(UserCreationForm):
    # ID_No = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Student ID No.' }),required=True,max_length=30)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first name'}),required=True,max_length=30)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last name'}),required=True,max_length=30)
	email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email ID'}),required=True,max_length=30)
	# department = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter department'}),required=True,max_length=30)
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),required=True,max_length=30)
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required=True,max_length=30)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}),required=True,max_length=30)

	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

	def clean_confirm_password(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password != confirm_password:
			raise forms.ValidationError("Password Mismatch")
		return confirm_password


class UserLoginForm(forms.Form):
	username = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),required=True,max_length=30)
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required=True,max_length=30)


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,max_length=30)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'about']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']




