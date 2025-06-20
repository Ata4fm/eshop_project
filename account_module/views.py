from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.http import Http404, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login,logout
from utils.email_service import send_email
from django.utils.decorators import method_decorator


class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-panel-dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                return JsonResponse(
                    {
                        'status': 'error',
                        'title': 'ناموفق',
                        'text': 'کاربر گرامی ایمیل وارد شده تکراری می باشد',
                        'icon': 'error',
                        'confirm_button_text': 'باشه'
                    }
                    ,status=400
                )
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return JsonResponse(
                    {
                        'status': 'success',
                        'title': 'موفق',
                        'text': 'کاربر گرامی لینک فعالسازی حساب برای ایمیل شما ارسال شد',
                        'icon': 'success',
                        'confirm_button_text': 'باشه',
                    },
                    status=200
                )
        else:
            errors = register_form.errors.get_json_data()
            if 'confirm_password' in errors:
                error_message = errors['confirm_password'][0]['message']
            else:
                error_message = 'اطلاعات را وارد نمایید.'
            return JsonResponse(
                {
                    'status': 'error',
                    'title': 'خطا',
                    'text': error_message,
                    'icon': 'error',
                    'confirm_button_text': 'باشه'
                }, status=400
            )

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-panel-dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)

    def post(self,request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    return JsonResponse(
                {
                    'status': 'error',
                    'title': 'اعلان',
                    'text': 'حساب کاربری فعال نشده است برای تایید به ایمیل مراجعه فرمایید',
                    'icon': 'info',
                    'confirm_button_text': 'باشه'

                }, status=400
            )
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request,user)
                        return JsonResponse(
                            {
                                'status': 'success',
                                'title': 'موفق',
                                'text': 'کاربر گرامی احراز هویت با موفقیت انجام شد',
                                'icon': 'success',
                            },
                            status=200
                        )
                    else:
                        return JsonResponse(
                            {
                                'status': 'error',
                                'title': 'خطا',
                                'text': 'کلمه عبور اشتباه است دوباره اقدام نمایید',
                                'icon': 'warning',
                                'confirm_button_text': 'باشه'
                            }, status=400
                        )

            else:
                return JsonResponse(
                    {
                        'status': 'error',
                        'title': 'خطا',
                        'text': 'چنین کاربری با این مشخصات یافت نشد!',
                        'icon': 'error',
                        'confirm_button_text': 'باشه'
                    }, status=400
                )
        else:
            errors = login_form.errors.get_json_data()
            if 'password' in errors:
                error_message = errors['password'][0]['message']
            else:
                error_message = 'اطلاعات را وارد نمایید'
            return JsonResponse(
                {
                    'status': 'error',
                    'title': 'خطا',
                    'text': error_message,
                    'icon': 'error',
                    'confirm_button_text': 'باشه'
                }, status=400
            )


        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login-page'))


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show success message to user
                return redirect(reverse('login-page'))
            else:
                # todo: show your account was activated message to user
                pass

        raise Http404


class ForgetPasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-panel-dashboard')

        return super().dispatch(request, *args, **kwargs)
    def get(self,request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request,'account_module/forgot_password.html',context)

    def post(self,request):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('home-page'))


        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-panel-dashboard')

        return super().dispatch(request, *args, **kwargs)
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login-page'))

        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login-page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login-page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)



