from django import forms
from search.models import Laboratory, ResearchPaper


class NewLaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        # モデルのインスタンスを生成

        fields = '__all__'
        widgets = {'uploader': forms.HiddenInput()}
        # fieldsに__all__をセットすると、モデル内の全てのフィールドが用いられる


class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper

        fields = '__all__'
        widgets = {'laboratory': forms.HiddenInput()}
