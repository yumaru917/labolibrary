from django import forms
from search.models import Laboratory


class NewLaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        # モデルのインスタンスを生成

        fields = '__all__'
        # fieldsに__all__をセットすると、モデル内の全てのフィールドが用いられる
