from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import generic
from .forms import (
    LoginForm, LabUserCreateForm, StudentUserCreateForm,
    NewUniversityForm, NewDepartmentForm, NewLaboratoryForm, NewFacultyForm, NewUniversityAreaForm
)

from mypage.models import (Laboratory, Faculty, Department, University)

import os


User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'index.html'


class UserCreateHome(generic.TemplateView):
    template_name = 'register/user_create_home.html'


class LabUserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/lab_user_create.html'
    form_class = LabUserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_lab_member = True
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('mail_template/create/subject.txt', context)
        message = render_to_string('mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('accounts:user_create_done')


class StudentUserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/student_user_create.html'
    form_class = StudentUserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('mail_template/create/subject.txt', context)
        message = render_to_string('mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('accounts:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


def user_delete_confirm(request):
    user = request.user
    return render(request, 'accounts/user_delete_confirm.html', {'user': user})


class UserDeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        return render(self.request, 'accounts/user_delete.html')


def register_university(request):
    form = NewUniversityForm()
    # formのインスタンス作成

    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = NewUniversityForm(request.POST)
        # 画面からPOSTした値を取得

        if form.is_valid():
            lab = form.save(commit=False)
            lab.uploader_id = request.user.id
            lab.save()
            # form.saveとするとデータが登録される

            return redirect('accounts:lab_user_create')
        else:
            print('ERROR FORM INVALID')
    return render(request, 'register/university_create.html', {'form': form})


def register_department(request):
    form = NewDepartmentForm()
    # formのインスタンス作成

    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = NewDepartmentForm(request.POST)
        # 画面からPOSTした値を取得

        if form.is_valid():
            lab = form.save(commit=False)
            lab.uploader_id = request.user.id
            lab.save()
            # form.saveとするとデータが登録される

            return redirect('accounts:lab_user_create')
        else:
            print('ERROR FORM INVALID')
    return render(request, 'register/department_create.html', {'form': form})


def register_laboratory(request):
    form = NewLaboratoryForm()
    # formのインスタンス作成

    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = NewLaboratoryForm(request.POST)
        # 画面からPOSTした値を取得

        if form.is_valid():
            lab = form.save(commit=False)
            lab.uploader_id = request.user.id
            lab.save()
            # form.saveとするとデータが登録される

            return redirect('accounts:lab_user_create')
        else:
            print('ERROR FORM INVALID')
    return render(request, 'register/laboratory_create.html', {'form': form})


def register_faculty(request):
    form = NewFacultyForm()
    # formのインスタンス作成

    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = NewFacultyForm(request.POST)
        # 画面からPOSTした値を取得

        if form.is_valid():
            lab = form.save(commit=False)
            lab.uploader_id = request.user.id
            lab.save()
            # form.saveとするとデータが登録される

            return redirect('accounts:lab_user_create')
        else:
            print('ERROR FORM INVALID')
    return render(request, 'register/laboratory_create.html', {'form': form})


# 本番は削除する。（都道府県の登録が終わったら。）
def register_university_area(request):
    form = NewUniversityAreaForm()
    # formのインスタンス作成

    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = NewUniversityAreaForm(request.POST)
        # 画面からPOSTした値を取得

        if form.is_valid():
            lab = form.save(commit=False)
            lab.uploader_id = request.user.id
            lab.save()
            # form.saveとするとデータが登録される

            return redirect('accounts:lab_user_create')
        else:
            print('ERROR FORM INVALID')
    return render(request, 'register/laboratory_create.html', {'form': form})
