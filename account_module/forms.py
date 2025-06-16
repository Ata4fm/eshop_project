from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ],
        error_messages={
            'required':'لطفا ایمیل را وارد نمایید'
        }
    )

    password = forms.CharField(
        label='رمز',
        widget=forms.PasswordInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),

        ],
        error_messages={
            'required': 'لطفا رمز عبور را وارد نمایید'
        }

    )

    confirm_password = forms.CharField(
        label='تایید رمز',
        widget= forms.PasswordInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),
        ],
        error_messages={
            'required': 'لطفا فیلد تایید رمز عبور را وارد نمایید'
        }
    )


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')








class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,

        ],
        error_messages={
            'required':'لطفا ایمیل را وارد نمایید'
        }
    )

    password = forms.CharField(
        label='رمز',
        widget=forms.PasswordInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.MinLengthValidator(8),
        ],
        error_messages={
            'required': 'لطفا رمز را وارد نمایید'
        }

    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ],
        error_messages={
            'required':'لطفا ایمیل را وارد نمایید'
        }
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='رمز',
        widget=forms.PasswordInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MinLengthValidator(6),
        ],
        error_messages={
            'required': 'لطفا رمز عبور را بیشتر از 6 عبارت بنویسید'
        }

    )

    confirm_password = forms.CharField(
        label='تایید رمز',
        widget=forms.PasswordInput(attrs={'class':'input_second input_all'}),
        validators=[
            validators.MinLengthValidator(6),
        ],
        error_messages={
            'required': 'لطفا دوباره رمز عبور را وارد نمایید'
        }
    )