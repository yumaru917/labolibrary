from django.forms import ModelForm, CharField, TextInput, Textarea
from django import forms

from mypage.models import UniversityArea, University, Faculty, Department, NotificationsForLaboratory
from search.models import SearchText


class SearchForm(ModelForm):
    class Meta:
        model = SearchText
        fields = ("search_item",)


class TagSearchForm(forms.Form):
    search_text = forms.CharField(required=False, max_length=100, label='検索ワード')
    university_area = forms.ModelChoiceField(UniversityArea.objects, required=False, label='大学の地域')
    university = forms.ModelChoiceField(University.objects, required=False, label='大学')
    faculty = forms.ModelChoiceField(Faculty.objects, required=False, label='学部・研究科')
    department = forms.ModelChoiceField(Department.objects, required=False, label='学科・専攻')
    master_acceptance = forms.NullBooleanField(required=False, label='修士受け入れ')
    doctor_acceptance = forms.NullBooleanField(required=False, label='博士受け入れ')

    def clean_master_acceptance(self):
        master_acceptance = self.cleaned_data['master_acceptance']
        if master_acceptance == "true":
            master_acceptance = True
        elif master_acceptance == "false":
            master_acceptance = False
        else:
            master_acceptance = None
        return master_acceptance

    def clean_doctor_acceptance(self):
        doctor_acceptance = self.cleaned_data['doctor_acceptance']
        if doctor_acceptance == "true":
            doctor_acceptance = True
        elif doctor_acceptance == "false":
            doctor_acceptance = False
        else:
            doctor_acceptance = None
        return doctor_acceptance


class SendContactForLaboratory(ModelForm):
    kind_of_notification = forms.ChoiceField(
        label='メッセージの種類',
        widget=forms.Select,
        choices=(
            ('大学院受験について', '大学院受験について'),
            ('研究室見学について', '研究室見学について'),
            ('研究について', '研究について'),
            ('その他', 'その他')
        )
    )

    class Meta:
        model = NotificationsForLaboratory
        # fields = '__all__'
        fields = ('title', 'kind_of_notification', 'laboratory', 'send_user', 'notification_detail', )
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトル',
            }),
            'notification_detail': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'ここに本文を記入してください',
            }),
            'laboratory': forms.HiddenInput(),
            'send_user': forms.HiddenInput(),
        }
        labels = {
            'title': 'タイトル',
            'kind_of_notification': 'メッセージの種類',
            'notification_detail': 'コメント内容',
        }
