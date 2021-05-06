from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from search.models import Laboratory, ResearchPaper
from register_lab.forms import NewLaboratoryForm, PaperUploadForm

# Create your views here.


@login_required
def register_lab(request):
    if request.user.is_lab is True:
        # form登録用のビュー

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

                return render(request, 'register/register_complete.html', {})
            else:
                print('ERROR FORM INVALID')
        return render(request, 'register/register.html', {'form': form})
        # POSTしない場合の画面にformを渡す
    else:
        return render(request, 'register/not_lab_user_error.html', {})


class LabInfoUpdate(UpdateView):
    template_name = 'register/lab_info_update.html'
    model = Laboratory
    fields = '__all__'

    def get_success_url(self):
        return reverse('mypage:mypage')

    def get_form(self):
        form = super(LabInfoUpdate, self).get_form()
        form.fields['laboratory_name'].label = '研究室名'
        return form


@login_required
def paper_upload(request):
    if request.user.is_lab is True:
        # form登録用のビュー

        form = PaperUploadForm()
        # formのインスタンス作成

        if request.method == 'POST':
            # 画面からPOSTした場合に、実行される

            form = PaperUploadForm(request.POST, request.FILES)
            # 画面からPOSTした値を取得

            if form.is_valid():
                paper = form.save(commit=False)
                paper.laboratory = Laboratory.objects.filter(uploader_id=request.user.id)[0]
                paper.save()
                # form.saveとするとデータが登録される

                return render(request, 'register/paper_upload_complete.html', {})
            else:
                print('ERROR FORM INVALID')
        return render(request, 'register/paper_upload.html', {'form': form})
        # POSTしない場合の画面にformを渡す
    else:
        return render(request, 'register/not_lab_user_error.html', {})


class PaperDelete(DeleteView):
    template_name = 'register/paper_delete_confirm.html'
    model = ResearchPaper

    success_url = reverse_lazy('mypage:mypage')
