from django.shortcuts import render, redirect
from search.models import Laboratory
from register_lab.forms import NewLaboratoryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def register_lab(request):
    # form登録用のビュー

    form = NewLaboratoryForm()
    # formのインスタンス作成

    if request.method == 'POST':
        # 画面からPOSTした場合に、実行される

        form = NewLaboratoryForm(request.POST)
        # 画面からPOSTした値を取得

        if form.is_valid():
            form.save(commit=True)
            # form.saveとするとデータが登録される

            return render(request, 'register/register_complete.html', {})
        else:
            print('ERROR FORM INVALID')
    return render(request, 'register/register.html', {'form': form})
    # POSTしない場合の画面にformを渡す
