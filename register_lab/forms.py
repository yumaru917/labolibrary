from django import forms

from search.models import LaboratoryInfo, ResearchPaper
from mypage.models import Laboratory


class NewLaboratoryForm(forms.ModelForm):

    class Meta:
        model = LaboratoryInfo
        # モデルのインスタンスを生成

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
        labels = {
            'campus': 'キャンパス',
            'professor_name': '研究室責任者氏名',
            'all_student_count': '学生総数',
            'master_count': '修士学生数',
            'doctor_count': '博士学生数',
            'after_graduation': '卒業した学生の進学先・就職先',
            'research_keywords': '研究テーマ・キーワード',
            'research_info': '研究詳細',
            'entrance_examination_date': '院試日',
            'entrance_examination_info': '院試詳細',
            'master_acceptance': '修士学生受け入れ可否',
            'doctor_acceptance': '博士学生受け入れ可否',
            'adult_graduate_student_acceptance': '社会人学生受け入れ可否',
            'degree_of_difficulty': '院試難易度',
            'students_rate': '内部性と外部生の割合',
            'information_source': '情報元webページ',
        }
        # fieldsに__all__をセットすると、モデル内の全てのフィールドが用いられる


class PaperUploadForm(forms.ModelForm):
    paper_kind = forms.ChoiceField(
        label='論文の種類',
        widget=forms.Select,
        choices=(
            ('graduation_thesis', '卒業論文'),
            ('academic_conference_thesis', '学会論文'),
            ('others', 'その他')
        )
    )

    class Meta:
        model = ResearchPaper

        fields = ('paper_title', 'paper_kind', 'paper_info', 'paper_file', 'laboratory', 'paper_uploader')
        widgets = {
            'laboratory': forms.HiddenInput(),
            'paper_uploader': forms.HiddenInput()
        }
