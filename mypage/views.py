from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView

from mypage.models import Laboratory
from search.models import LaboratoryInfo, ResearchPaper
from accounts.models import User, UserProfile

from mypage.forms import UserProfileCreateForm


# Create your views here.

@login_required
def mypage(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    is_lab = request.user.is_lab_member
    if is_lab is True:
        user_laboratory = request.user.laboratory
        user_id = request.user.id
        favorite_laboratory = User.objects.get(id=user_id).favorite_laboratory.all()
        print(user_laboratory)

        context = {
            'user': user,
            'user_profile': user_profile,
            'user_laboratory': user_laboratory,
            'favorite_laboratory': favorite_laboratory,
        }

        return render(request, "mypage/researcher_mypage.html", context)
    else:
        user_id = request.user.id
        favorite_laboratory = User.objects.get(id=user_id).favorite_laboratory.all()

        context = {
            'user': user,
            'user_profile': user_profile,
            'favorite_laboratory': favorite_laboratory,
        }
        return render(request, "mypage/student_mypage.html", context)


def user_profile(request):
    user = request.user
    profile = user.profile
    return render(request, 'mypage/user_profile.html', {'user': user, 'profile': profile})


def create_user_profile(request):
    user = request.user.id
    form = UserProfileCreateForm(
        initial={
            'user': user
        }
    )
    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = UserProfileCreateForm(
            request.POST,
            initial={
                'user': user
            }
        )
        # 画面からPOSTした値を取得

        if form.is_valid():
            paper = form.save(commit=False)
            paper.save()
            # form.saveとするとデータが登録される
            context = {
                'form': form,
                'user': user
            }

            return render(request, 'mypage/create_user_profile_complete.html', context)
        else:
            for ele in form:
                print(ele)
            print('ERROR FORM INVALID')

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'mypage/create_user_profile.html', context)


# 要修正（エラーが出てる。）
class UserProfileUpdate(UpdateView):
    template_name = 'mypage/edit_user_profile.html'
    model = UserProfile
    fields = (
        # user_form
        'user', 'research_detail', 'interested_area', 'future_works', 'free_comment'
    )
    #
    def get_success_url(self):
        return reverse('mypage:mypage')

    def get_form(self):
        form = super(UserProfileUpdate, self).get_form()
        return form

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)  # はじめに継承元のメソッドを呼び出す
        context["user"] = user
        return context
