import logging
import urllib

from django.shortcuts import render, redirect
from django.db.models import Q
from search.models import Laboratory, SearchText, ResearchPaper
from search.forms import SearchForm

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
logger = logging.getLogger(__name__)


# Create your views here.


def search_view(request):
    model = Laboratory.objects.values()
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
                laboratory_query_list = Laboratory.objects.filter(
                    Q(research_keywords__icontains=str_search_text) | Q(research_info__icontains=str_search_text))
            else:
                laboratory_query_list = Laboratory.objects.all()

            for laboratory_query in laboratory_query_list:
                lab_name = laboratory_query.laboratory_name
                keywords = laboratory_query.research_keywords
                university = laboratory_query.university
                create_date = laboratory_query.create_date
                lab_url = laboratory_query.laboratory_website
                pk = laboratory_query.pk
                lab_dict = {
                    'lab_name': lab_name,
                    'research_keywords': keywords,
                    'university': university,
                    'create_date': create_date,
                    'lab_url': lab_url,
                    'pk': pk,
                    'laboratory': laboratory_query
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
            return redirect('search:search_form')
    else:
        context['form'] = SearchForm()

    return render(request, "search/search_form.html", context)


def detail_view(request, lab_pk):
    laboratory = Laboratory.objects.get(pk=lab_pk)
    paper = ResearchPaper.objects.filter(laboratory_id=laboratory.id)
    context = {'laboratory': laboratory, 'paper_list': paper}

    # return HttpResponse(table)

    return render(request, "search/detail.html", context)
