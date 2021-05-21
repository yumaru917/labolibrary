from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from mypage.models import (University, Faculty, Department, Laboratory, UniversityArea)
from accounts.models import UniversityEmail

User = get_user_model()


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


# メイン（まずはこれだけ使う）
class LabUserCreateForm(UserCreationForm):
    """研究室ユーザー登録用フォーム"""

    # department = forms.ModelChoiceField(
    #     label='学科・専攻',
    #     queryset=Department.objects,
    # )

    class Meta:
        model = User
        fields = ('is_lab_member', 'last_name', 'first_name', 'email',
                  'university', 'faculty', 'department', 'laboratory', 'status_position')
        # widgets = {'is_lab_member': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        is_lab_member = self.cleaned_data['is_lab_member']
        User.objects.filter(email=email, is_active=False).delete()
        # ドメインの確認
        str_email = str(email)
        pos_a = str_email.find('@')
        email_domain = str_email[pos_a+1:]
        print(email_domain)
        certification_email_domain = UniversityEmail.objects.all().values_list('university_email_domain', flat=True)
        if is_lab_member:
            if email_domain not in certification_email_domain:
                raise forms.ValidationError('研究室配属者アカウントとして認証されていないメールアドレスのドメインです。')
        return email

    def clean(self):
        cleaned_data = super().clean()
        user_laboratory = Laboratory.objects.get(id=cleaned_data.get('laboratory').id)
        user_department = Department.objects.get(id=cleaned_data.get('department').id)
        user_faculty = Faculty.objects.get(id=cleaned_data.get('faculty').id)
        user_university = University.objects.get(id=cleaned_data.get('university').id)

        if cleaned_data.get('laboratory') != Laboratory.objects.get(id=user_laboratory.id):
            # print(cleaned_data.get('laboratory'), Laboratory.objects.get(id=user_laboratory.id))
            # print('False laboratory')
            raise forms.ValidationError("学科・専攻のデータベースに存在しない研究室です。研究室を登録してください。")
        if user_department != user_laboratory.belong_department:
            # print(user_department, user_laboratory.belong_department)
            # print('false department')
            raise forms.ValidationError("学部・研究科のデータベースに存在しない学科・専攻です。学科・専攻を登録してください。")
        if user_faculty != user_laboratory.belong_department.belong_faculty:
            # print(user_faculty, user_laboratory.belong_department.belong_faculty)
            # print('false faculty')
            raise forms.ValidationError("大学のデータベースに存在しない学部・研究科です。学部・研究科を登録してください。")
        if user_university != user_laboratory.belong_department.belong_faculty.belong_university:
            # print(user_university, user_laboratory.belong_department.belong_faculty.belong_university)
            # print('false university')
            raise forms.ValidationError("データベースに存在しない大学です。大学を登録してください。")

        return cleaned_data


class StudentUserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email',
                  'university', 'faculty', 'department', 'laboratory', 'status_position')
        widgets = {'is_lab_member': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

    def clean(self):
        cleaned_data = super().clean()
        user_department = Department.objects.get(id=cleaned_data.get('department').id)
        user_faculty = Faculty.objects.get(id=cleaned_data.get('faculty').id)
        user_university = University.objects.get(id=cleaned_data.get('university').id)

        if user_department != user_department:
            # print(user_department, user_laboratory.belong_department)
            # print('false department')
            raise forms.ValidationError("学部・研究科のデータベースに存在しない学科・専攻です。学科・専攻を登録してください。")
        if user_faculty != user_department.belong_faculty:
            # print(user_faculty, user_laboratory.belong_department.belong_faculty)
            # print('false faculty')
            raise forms.ValidationError("大学のデータベースに存在しない学部・研究科です。学部・研究科を登録してください。")
        if user_university != user_department.belong_faculty.belong_university:
            # print(user_university, user_laboratory.belong_department.belong_faculty.belong_university)
            # print('false university')
            raise forms.ValidationError("データベースに存在しない大学です。大学を登録してください。")

        return cleaned_data


class NewUniversityForm(forms.ModelForm):
    class Meta:
        model = University
        # モデルのインスタンスを生成

        fields = '__all__'


class NewDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        # モデルのインスタンスを生成

        fields = '__all__'


class NewLaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        # モデルのインスタンスを生成

        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        user_department = Department.objects.get(id=cleaned_data.get('belong_department').id)
        user_faculty = Faculty.objects.get(id=cleaned_data.get('belong_faculty').id)
        user_university = University.objects.get(id=cleaned_data.get('belong_university').id)

        if user_faculty != user_department.belong_faculty:
            print(user_department, user_department)
            print('false department')
            raise forms.ValidationError("学部・研究科のデータベースに存在しない学科・専攻です。学科・専攻を登録してください。")
        if user_university != user_department.belong_faculty.belong_university:
            print(user_faculty, user_department.belong_faculty)
            print('false faculty')
            raise forms.ValidationError("大学のデータベースに存在しない学部・研究科です。学部・研究科を登録してください。")

        return cleaned_data


class NewFacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        # モデルのインスタンスを生成

        fields = '__all__'


# 本番は削除する。（都道府県の登録が終わったら。）
class NewUniversityAreaForm(forms.ModelForm):
    class Meta:
        model = UniversityArea
        # モデルのインスタンスを生成

        fields = '__all__'
