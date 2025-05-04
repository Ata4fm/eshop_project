from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User



class EditUserFavoriteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['favorite']
        widgets = {
            'favorite': forms.CheckboxSelectMultiple()
        }


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address','phone']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'input_second input_all',
                    'placeholder': 'نام'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'input_second input_all',
                    'placeholder': 'نام خانوادگی'
                }
            ),
            'avatar': forms.FileInput(
                attrs={

                }
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'input_second ',
                    'rows':3,
                    'id': 'message',
                    'placeholder': 'آدرس'

                },
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'input_second ',
                    'placeholder': 'تلفن'

                }
            )
        }

        error_messages = {
            'first_name': {
                'required': 'نام و نام خانوادگی الزامی میباشد'
            },
            'last_name': {
                'required': 'لطفا ایمیل را وارد نمایید'
            },
            'avatar': {
                'required': 'لطفا عکس پروفایل خود را بارگذاری نمایید'
            },
            'address': {
                'required': 'آدرس خود را بنویسید'
            },
            'phone': {
                'required': 'تلفن را وارد نمایید'
            }


        }




class ChangePasswordModelForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_second input_all',
                'placeholder':'لطفا رمز عبور فعلی خود را وارد کنید'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ],
        error_messages={
            'required': 'لطفا رمز عبور را وارد نمایید',

        }

    )

    password = forms.CharField(
        label='رمز',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_second input_all',
                'placeholder':'لطفا رمز عبور جدید خود را وارد کنید'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ],
        error_messages={
            'required': 'لطفا رمز عبور را وارد نمایید'
        }

    )

    confirm_password = forms.CharField(
        label='تایید رمز',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_second input_all',
                'placeholder': 'لطفا رمز عبور جدید خود را تکرار کنید'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ],
        error_messages={
            'required': 'لطفا دوباره رمز عبور را وارد نمایید'
        }
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
