from django import forms

from .models import ContactUs





class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'title', 'message']
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'نام و نام خانوادگی'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ایمیل'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'عنوان'
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows':5,
                    'id': 'message',
                    'placeholder': 'پیغام شما'

                }
            )
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی الزامی میباشد'
            },
            'email': {
                'required': 'لطفا ایمیل را وارد نمایید'
            },
            'title': {
                'required': 'لطفا عنوان درخواست را بنویسید'
            },
            'message': {
                'required': 'متن پیغام الزامی میباشد'
            }


        }
