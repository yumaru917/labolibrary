import logging
import urllib

from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from search.models import LaboratoryInfo, SearchText, ResearchPaper
from mypage.models import Laboratory
from search.forms import SearchForm, TagSearchForm, SendContactForLaboratory

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
logger = logging.getLogger(__name__)


# Create your views here.


def search_view(request):
    model = LaboratoryInfo.objects.values()
    form = SearchForm(request.POST)
    lab_list = []
    table = None

    context = {'model': model,
               'form': form,
               'table': table,
               'lab_list': lab_list,
               'list_json': None}

    if request.method == 'POST':
        # 入力されたらモデルに格納してloadingに遷移
        if context['form'].is_valid():
            context['form'].save()
            logger.info(request.POST)

            # データベースに保存されたデータのうち、最新のものを取得。（入力された検索語句を取得。）
            search_text = SearchText.objects.latest("id")
            str_search_text = str(search_text)

            if str_search_text:
                laboratory_query_list = LaboratoryInfo.objects.filter(
                    Q(research_keywords__icontains=str_search_text) | Q(research_info__icontains=str_search_text))
            else:
                laboratory_query_list = LaboratoryInfo.objects.all()

            for laboratory_query in laboratory_query_list:
                laboratory = laboratory_query.laboratory
                keywords = laboratory_query.research_keywords
                university = laboratory_query.laboratory.belong_university
                create_date = laboratory_query.page_create_date
                lab_url = laboratory_query.laboratory_website
                pk = laboratory_query.pk
                lab_dict = {
                    'laboratory': laboratory,
                    'research_keywords': keywords,
                    'university': university,
                    'create_date': create_date,
                    'lab_url': lab_url,
                    'pk': pk,
                }
                lab_list.append(lab_dict)

            context = {'model': model,
                       'form': form,
                       'table': table,
                       'search_text': str_search_text,
                       'lab_query_list': laboratory_query_list,
                       'lab_list': lab_list}

            # return HttpResponse(table)
            return render(request, "search/search_form.html", context)
        # されてなければ戻る
        else:
            return redirect('search:search')
    else:
        context['form'] = SearchForm()

    return render(request, "search/search_form.html", context)


def tag_search_view(request):
    model = LaboratoryInfo.objects.values()
    form = TagSearchForm(request.POST)
    lab_list = []
    table = None

    context = {'model': model,
               'form': form,
               'table': table,
               'lab_list': lab_list,
               'list_json': None}

    if request.method == 'POST':
        # 入力されたらモデルに格納してloadingに遷移
        if context['form'].is_valid():
            print(request.POST['university_area'])
            print(request.POST['university'])
            print(request.POST['faculty'])
            print(request.POST['department'])
            logger.info(request.POST)

            input_university_area = request.POST['university_area']
            input_university = request.POST['university']
            input_faculty = request.POST['faculty']
            input_department = request.POST['department']

            filtering = {
                'university_area': input_university_area,
                'university': input_university,
                'faculty': input_faculty,
                'department': input_department
            }

            laboratory_query_list = LaboratoryInfo.objects.all()

            if request.POST:
                if request.POST['university_area']:
                    laboratory_query_list = laboratory_query_list.filter(
                        laboratory__belong_university__university_area=input_university_area,
                    )
                    print(laboratory_query_list)
                if request.POST['university']:
                    laboratory_query_list = laboratory_query_list.filter(
                        laboratory__belong_university=input_university,
                    )
                    print(laboratory_query_list)
                if request.POST['faculty']:
                    laboratory_query_list = laboratory_query_list.filter(
                        laboratory__belong_faculty=input_faculty,
                    )
                    print(laboratory_query_list)
                if request.POST['department']:
                    laboratory_query_list = laboratory_query_list.filter(
                        laboratory__belong_department=input_department
                    )
                    print(laboratory_query_list)
            else:
                laboratory_query_list = LaboratoryInfo.objects.all()

            for laboratory_query in laboratory_query_list:
                laboratory = laboratory_query.laboratory
                keywords = laboratory_query.research_keywords
                university = laboratory_query.laboratory.belong_university
                create_date = laboratory_query.page_create_date
                lab_url = laboratory_query.laboratory_website
                pk = laboratory_query.pk
                lab_dict = {
                    'laboratory': laboratory,
                    'research_keywords': keywords,
                    'university': university,
                    'create_date': create_date,
                    'lab_url': lab_url,
                    'pk': pk,
                }
                lab_list.append(lab_dict)

            context = {'model': model,
                       'form': form,
                       'table': table,
                       'filtering': filtering,
                       'lab_query_list': laboratory_query_list,
                       'lab_list': lab_list}

            # return HttpResponse(table)
            return render(request, "search/tag_search_form.html", context)
        # されてなければ戻る
        else:
            return redirect('search:tag_search')
    else:
        context['form'] = TagSearchForm()

    return render(request, "search/tag_search_form.html", context)


def detail_view(request, lab_pk):
    laboratory_info = LaboratoryInfo.objects.get(pk=lab_pk)
    laboratory = LaboratoryInfo.objects.get(pk=lab_pk).laboratory
    laboratory_member = laboratory.user_belong_to_laboratory.all()
    paper = ResearchPaper.objects.filter(laboratory_id=laboratory_info.id)
    user_favorite_laboratories_id = request.user.favorite_laboratory.all().values_list('id', flat=True)
    print(laboratory_info)
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'laboratory_member': laboratory_member,
        'paper_list': paper,
        'user_favorite_laboratories_id': user_favorite_laboratories_id
    }

    # return HttpResponse(table)

    return render(request, "search/detail.html", context)


def send_message_for_laboratory_view(request, lab_pk):
    laboratory_info = LaboratoryInfo.objects.get(pk=lab_pk)
    laboratory = LaboratoryInfo.objects.get(pk=lab_pk).laboratory
    form = SendContactForLaboratory(
        initial={
            'laboratory': laboratory,
            'send_user': request.user
        }
    )
    if request.method == 'POST':
        form = SendContactForLaboratory(
            request.POST,
            initial={
                'laboratory': laboratory,
                'send_user': request.user
            }
        )
        if form.is_valid():
            send_massage_form = form.save(commit=False)
            send_massage_form.save()
            return render(request, 'search/send_message_complete.html', {})
        else:
            print('ERROR send_massage FORM INVALID')
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'form': form
    }

    # return HttpResponse(table)

    return render(request, "search/send_message.html", context)


def paper_download(request, pk):
    upload_file = get_object_or_404(ResearchPaper, pk=pk)
    file = upload_file.paper_file  # ファイル本体
    return FileResponse(file)


def follow_laboratory(request, pk):
    """場所をお気に入り登録する"""
    laboratory = get_object_or_404(LaboratoryInfo, pk=pk).laboratory
    laboratory_info = get_object_or_404(LaboratoryInfo, pk=pk)
    request.user.favorite_laboratory.add(laboratory_info)
    paper = ResearchPaper.objects.filter(laboratory_id=laboratory.id)
    user_info = request.user
    follow_complete = True
    user_favorite_laboratories_id = request.user.favorite_laboratory.all().values_list('id', flat=True)
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'paper_list': paper,
        'user_info': user_info,
        'follow_complete': follow_complete,
        'user_favorite_laboratories_id': user_favorite_laboratories_id
    }
    return render(request, "search/detail.html", context)


def remove_follow_laboratory(request, pk):
    """場所をお気に入り登録する"""
    laboratory_info = get_object_or_404(LaboratoryInfo, pk=pk)
    laboratory = get_object_or_404(LaboratoryInfo, pk=pk).laboratory
    request.user.favorite_laboratory.remove(laboratory_info)
    laboratory_info = LaboratoryInfo.objects.get(pk=pk)
    paper = ResearchPaper.objects.filter(laboratory_id=laboratory.id)
    user_info = request.user
    remove_follow_complete = True
    user_favorite_laboratories_id = request.user.favorite_laboratory.all().values_list('id', flat=True)
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'paper_list': paper,
        'user_info': user_info,
        'remove_follow_complete': remove_follow_complete,
        'user_favorite_laboratories_id': user_favorite_laboratories_id
    }
    return render(request, "search/detail.html", context)
