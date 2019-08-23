from django import forms
from collections import OrderedDict
from .models import userdata,Profile
import re

class LoginForm(forms.Form):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
                                                 attrs={
                                                       'class': 'form-control', 'placeholder': 'Password',
                                                 }),
    help_text='Password should be atleast 8 characters,'
                 'one lower,upper and special character.')

class UserregisterForm(forms.Form):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={ 'class':'form-control','placeholder':'Email'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(
                                              attrs={
                                                  'class':'form-control','placeholder':'Password',
                                              }),
    help_text='Password should be atleast 8 characters,'
              'one lower,upper and special character.')
    password2 = forms.CharField(label='Password Conformation',widget=forms.PasswordInput(
                                                  attrs={
                                                       'class': 'form-control','placeholder':'Confirm Password'
                                                  }),
    help_text='Enter the same password as before, for verification.')

    def clean_email(self):
        email2=self.cleaned_data.get('email')
        email=userdata.objects.filter(email=email2)
        if email.exists():
            raise forms.ValidationError('This Email is already taken')
        return email

    def clean_username(self):
        username=self.cleaned_data.get('username')
        name=userdata.objects.filter(username=username)
        if name.exists():
            raise forms.ValidationError('This Username name is already taken,try different name')
        if username.isdigit():
            raise forms.ValidationError('username should not all numeric')
        return username

    def clean_password2(self):
        # MIN_LENGTH=8
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,50}$"
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('Password didnt match')
        # elif  len(password)<=MIN_LENGTH:
        #     raise forms.ValidationError('Password should have atleast %d characters'%MIN_LENGTH)
        # elif not any(char.isdigit() for char in password):
        #     raise forms.ValidationError('Password should have at least one numeral ')
        # elif not any(char.isupper() for char in password):
        #     raise forms.ValidationError('Password should have at least one uppercase letter ')
        # elif not any(char.islower() for char in password):
        #     raise forms.ValidationError('Password should have at least one lower letter ')
        # elif not any(char==reg for char in password):
        #     raise forms.ValidationError('Password should have at least one lower letter,upper,special ')
        # return password
        pat = re.compile(reg)
        match = re.search(pat, password)
        if not match:
            raise forms.ValidationError('Password should be atleast 8 characters length and one lower letter,upper,special character')
        return password


class PasswordResetForm(forms.Form):
      new_password=forms.CharField(label='New Password',widget=forms.PasswordInput(
                                                      attrs={ 'class':'form-control',
                                                              'placeholder':'New Password',
                                                      }
      ))
      new_password2 = forms.CharField(label='New Password Conformation', widget=forms.PasswordInput(
          attrs={'class': 'form-control',
                 'placeholder': 'Confirm New Password',
                 }
      ))

      def clean_new_password(self):
          reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,50}$"
          new_password = self.cleaned_data.get("new_password")
          new_password2 = self.cleaned_data.get("new_password2")
          if new_password and new_password2 and new_password != new_password2:
              raise forms.ValidationError('Password didnt match')
          pat = re.compile(reg)
          match = re.search(pat, new_password)
          if not match:
              raise forms.ValidationError(
                  'Password should be atleast 8 characters length and one lower letter,upper,special character')
          return new_password


class PasswordChangeForm(PasswordResetForm):
      old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(
                                                          attrs={'class': 'form-control',
                                                                  'placeholder': 'Old Password',
                                                          }
      ))

      def clean_old_password(self):
          old_password=self.cleaned_data.get('old_password')
          match=userdata.objects.filter(password=old_password)
          if not match:
              raise forms.ValidationError('your old password is incorrect')
          return old_password

PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password', 'new_password2']
)


class UserUpdateForm(forms.ModelForm):
       class Meta:
           model=userdata
           fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
       class Meta:
           model=Profile
           fields = ['profile']

