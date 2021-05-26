import logging
import urllib

from django.http import FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from search.models import LaboratoryInfo, SearchText, ResearchPaper, Image
from mypage.models import Laboratory
from search.forms import SearchForm, TagSearchForm, SendContactForLaboratory

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
logger = logging.getLogger(__name__)


# Create your views here.

def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def search_view(request):
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
            print(request.POST['search_text'])
            print(request.POST['university_area'])
            print(request.POST['university'])
            print(request.POST['faculty'])
            print(request.POST['department'])
            logger.info(request.POST)

            input_university_area = request.POST['university_area']
            input_university = request.POST['university']
            input_faculty = request.POST['faculty']
            input_department = request.POST['department']
            input_master_acceptance = request.POST.get('master_acceptance')
            input_doctor_acceptance = request.POST.get('doctor_acceptance')

            if input_master_acceptance == "true":
                input_master_acceptance = True
            elif input_master_acceptance == "false":
                input_master_acceptance = False
            else:
                input_master_acceptance = None

            if input_doctor_acceptance == "true":
                input_doctor_acceptance = True
            elif input_doctor_acceptance == "false":
                input_doctor_acceptance = False
            else:
                input_doctor_acceptance = None

            filtering = {
                'university_area': input_university_area,
                'university': input_university,
                'faculty': input_faculty,
                'department': input_department,
                'master_acceptance': input_master_acceptance,
                'doctor_acceptance': input_doctor_acceptance
            }

            laboratory_query_list = LaboratoryInfo.objects.all()

            if request.POST:
                if request.POST['search_text']:
                    str_search_text = str(request.POST['search_text'])
                    SearchText.objects.create(search_item=str_search_text)
                    if str_search_text:
                        laboratory_query_list = laboratory_query_list.filter(
                            Q(research_keywords__icontains=str_search_text) | Q(
                                research_info__icontains=str_search_text))
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
                if request.POST['professor_name']:
                    str_professor_name = str(request.POST['professor_name'])
                    if str_professor_name:
                        laboratory_query_list = laboratory_query_list.filter(
                            Q(professor_name__contains=str_professor_name)
                        )
                if request.POST.get('master_acceptance'):
                    if input_master_acceptance:
                        laboratory_query_list = laboratory_query_list.filter(
                            master_acceptance=input_master_acceptance
                        )
                        print(input_master_acceptance)
                        print(laboratory_query_list)
                if request.POST.get('doctor_acceptance'):
                    if input_doctor_acceptance:
                        laboratory_query_list = laboratory_query_list.filter(
                            doctor_acceptance=input_doctor_acceptance
                        )
                        print(laboratory_query_list)
            else:
                laboratory_query_list = LaboratoryInfo.objects.all()

            # laboratory_query_list = paginate_queryset(request, laboratory_query_list, 10)

            for laboratory_query in laboratory_query_list:
                laboratory = laboratory_query.laboratory
                laboratory_info = laboratory.info_of_laboratory
                keywords = laboratory_query.research_keywords
                university = laboratory_query.laboratory.belong_university
                create_date = laboratory_query.page_create_date
                lab_url = laboratory_query.laboratory_website
                pk = laboratory_query.pk
                try:
                    image = Image.objects.filter(laboratory_info=laboratory_info)[0]
                    print(Image.objects.filter(laboratory_info=laboratory_info)[0])
                except:
                    image = None
                    print('no image except happened')
                lab_dict = {
                    'laboratory': laboratory,
                    'image': image,
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
                       'lab_list': lab_list,
                       # 'post_list': laboratory_query_list.object_list,
                       # 'page_obj': laboratory_query_list,
                       }

            # return HttpResponse(table)
            return render(request, "search/search_form.html", context)
        # されてなければ戻る
        else:
            return redirect('search:search')
    else:
        context['form'] = TagSearchForm()

    return render(request, "search/search_form.html", context)


def detail_view(request, lab_pk):
    laboratory_info = LaboratoryInfo.objects.get(pk=lab_pk)
    laboratory = LaboratoryInfo.objects.get(pk=lab_pk).laboratory
    laboratory_member = laboratory.user_belong_to_laboratory.all()
    paper = ResearchPaper.objects.filter(laboratory_id=laboratory_info.id)
    try:
        user_favorite_laboratories_id = request.user.favorite_laboratory.all().values_list('id', flat=True)
    except AttributeError:
        user_favorite_laboratories_id = None
    print(laboratory_info)
    try:
        image_list = Image.objects.filter(laboratory_info=laboratory_info)
        print(Image.objects.filter(laboratory_info=laboratory_info)[0])
    except:
        image_list = None
        print('except happened')
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'laboratory_member': laboratory_member,
        'paper_list': paper,
        'image_list': image_list,
        'user_favorite_laboratories_id': user_favorite_laboratories_id
    }

    # return HttpResponse(table)

    return render(request, "search/detail.html", context)


def research_paper_list_view(request, lab_pk):
    laboratory_info = LaboratoryInfo.objects.get(pk=lab_pk)
    laboratory = LaboratoryInfo.objects.get(pk=lab_pk).laboratory
    paper = ResearchPaper.objects.filter(laboratory_id=laboratory_info.id)
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'paper_list': paper,
    }

    # return HttpResponse(table)

    return render(request, "search/research_paper_list.html", context)


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

            title = send_massage_form.title
            kind_of_notification = send_massage_form.kind_of_notification
            laboratory_belong_to = send_massage_form.laboratory
            send_user = send_massage_form.send_user
            notification_detail = send_massage_form.notification_detail

            emails = laboratory.user_belong_to_laboratory.all()
            send_to_mails = []
            for email in emails:
                send_to_mails.append(email.email)
            print(send_to_mails)

            context_for_mail = {
                'title': title,
                'kind_of_notification': kind_of_notification,
                'laboratory_belong_to': laboratory_belong_to,
                'send_user': send_user,
                'notification_detail': notification_detail
            }

            inquiry = render_to_string('mail_template/lab_page/contact_message.txt', context_for_mail)

            message = EmailMessage(subject="あなたの所属する研究室へ問い合わせがきています。",
                                   body=inquiry,
                                   to=send_to_mails,
                                   cc=["lablib2021@gmail.com"])
            message.send()

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
    user_favorite_laboratories_id = request.user.favorite_laboratory.values_list('id', flat=True)
    context = {
        'laboratory': laboratory,
        'laboratory_info': laboratory_info,
        'paper_list': paper,
        'user_info': user_info,
        'follow_complete': follow_complete,
        'user_favorite_laboratories_id': user_favorite_laboratories_id
    }

    inquiry = render_to_string('mail_template/lab_page/favorite_message.txt', context)

    emails = laboratory.user_belong_to_laboratory.all()
    send_to_mails = []
    for email in emails:
        send_to_mails.append(email.email)
    print(send_to_mails)

    message = EmailMessage(subject="お気に入り登録通知",
                           body=inquiry,
                           to=send_to_mails,
                           cc=["lablib2021@gmail.com"])
    message.send()
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
