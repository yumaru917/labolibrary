from django import forms

from accounts.models import UserProfile


class UserProfileCreateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('user', 'research_detail', 'interested_area', 'future_works', 'free_comment')
        # widgets = {
        #     'user': forms.HiddenInput(),
        # }
        labels = {
            'research_detail': '自信が行っている研究内容',
            'interested_area': '興味のある研究',
            'future_works': '予定進路',
            'free_comment': '自由記入',
        }
