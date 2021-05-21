from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from search.models import LaboratoryInfo, ResearchPaper, Image
from mypage.models import Laboratory, Department, Faculty, University

from register_lab.forms import NewLaboratoryForm, PaperUploadForm, ImageUploadForm

# Create your views here.


@login_required
def register_lab(request):
    if request.user.is_lab_member is True:
        # form登録用のビュー

        laboratory = request.user.laboratory

        form = NewLaboratoryForm()
        # formのインスタンス作成

        if request.method == 'POST':
            # 画面からPOSTした場合に、実行される

            form = NewLaboratoryForm(request.POST)
            # 画面からPOSTした値を取得

            if form.is_valid():
                lab_info = form.save(commit=False)
                lab_info.laboratory_id = laboratory.id
                lab_info.belong_university_id = laboratory.belong_university.id
                lab_info.belong_department_id = laboratory.belong_department.id
                lab_info.belong_faculty_id = laboratory.belong_faculty.id
                print(lab_info.laboratory_id)
                lab_info.save()
                # form.saveとするとデータが登録される

                return render(request, 'register/register_complete.html', {})
            else:
                print('ERROR FORM INVALID')
        # print(form)
        # print(laboratory)
        return render(request, 'register/register.html', {'form': form, 'laboratory': laboratory})
        # POSTしない場合の画面にformを渡す
    else:
        return render(request, 'register/not_lab_user_error.html', {})


class LabInfoUpdate(UpdateView):
    template_name = 'register/lab_info_update.html'
    model = LaboratoryInfo
    fields = (
        # user_form
        'campus',
        'professor_name',
        'all_student_count',
        'master_count',
        'doctor_count',
        'after_graduation',
        'research_keywords',
        'research_info',
        'entrance_examination_date',
        'entrance_examination_info',
        'master_acceptance',
        'doctor_acceptance',
        'adult_graduate_student_acceptance',
        'degree_of_difficulty',
        'students_rate',
        'information_source',
    )

    def get_success_url(self):
        return reverse('mypage:mypage')

    def get_form(self):
        form = super(LabInfoUpdate, self).get_form()
        return form

    def get_context_data(self, **kwargs):
        laboratory = self.request.user.laboratory
        context = super().get_context_data(**kwargs)  # はじめに継承元のメソッドを呼び出す
        context["laboratory"] = laboratory
        return context


@login_required
def paper_upload(request):
    if request.user.is_lab_member is True:
        # form登録用のビュー
        try:
            form = PaperUploadForm(
                initial={
                    'laboratory': LaboratoryInfo.objects.get(laboratory_id=request.user.laboratory.id),
                    'paper_uploader': request.user
                }
            )
        except LaboratoryInfo.DoesNotExist:
            return render(request, 'register/paper_upload_error.html', {})
        # formのインスタンス作成

        if request.method == 'POST':
            # 画面からPOSTした場合に、実行される

            form = PaperUploadForm(
                request.POST,
                request.FILES,
                initial={
                    'laboratory': LaboratoryInfo.objects.get(laboratory_id=request.user.laboratory.id),
                    'paper_uploader': request.user
                }
            )
            print(form['laboratory'])
            # 画面からPOSTした値を取得

            if form.is_valid():
                paper = form.save(commit=False)
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


def image_upload(request):
    if request.user.is_lab_member is True:
        # form登録用のビュー
        try:
            form = ImageUploadForm(
                initial={
                    'laboratory_info': LaboratoryInfo.objects.get(laboratory_id=request.user.laboratory.id),
                }
            )
        except LaboratoryInfo.DoesNotExist:
            return render(request, 'register/image_upload_error.html', {})
        # formのインスタンス作成

        if request.method == 'POST':
            # 画面からPOSTした場合に、実行される

            form = ImageUploadForm(
                request.POST,
                request.FILES,
                initial={
                    'laboratory_info': LaboratoryInfo.objects.get(laboratory_id=request.user.laboratory.id),
                }
            )
            print(form['laboratory_info'])
            # 画面からPOSTした値を取得

            if form.is_valid():
                paper = form.save(commit=False)
                paper.save()
                # form.saveとするとデータが登録される

                return render(request, 'register/image_upload_complete.html', {})
            else:
                print('ERROR FORM INVALID')
        return render(request, 'register/image_upload.html', {'form': form})
        # POSTしない場合の画面にformを渡す
    else:
        return render(request, 'register/not_lab_user_error.html', {})


class ImageDelete(DeleteView):
    template_name = 'register/image_delete_confirm.html'
    model = Image

    success_url = reverse_lazy('mypage:mypage')
