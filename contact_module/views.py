from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from site_module.models import SiteSetting
from .forms import ContactUsModelForm
from django.views.generic.edit import CreateView
from .models import UserProfile


class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context

class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact/create-profile'


class ProfileView(ListView):
    model = UserProfile
    template_name = 'contact_module/profile_list_page.html'
    context_object_name = 'profiles'