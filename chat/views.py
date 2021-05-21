from django.shortcuts import render
from django.db.models import Q


from accounts.models import User
from chat.models import ChatMessageBetweenUserAndUser

from chat.forms import SendMessageForUserForm

# Create your views here.


def chat_between_user_and_user_view(request, user_pk):
    talk_to = User.objects.get(pk=user_pk)
    user = request.user
    form = SendMessageForUserForm()
    text = ChatMessageBetweenUserAndUser.objects.filter(
        Q(send_user=user, receive_user=talk_to) | Q(send_user=talk_to, receive_user=user)
    ).order_by('-send_date')
    if request.method == 'POST':
        form = SendMessageForUserForm(
            request.POST,
            initial={
                'receive_user': talk_to,
                'send_user': request.user
            }
        )
        if form.is_valid():
            send_massage_form = form.save(commit=False)
            send_massage_form.send_user = user
            send_massage_form.receive_user = talk_to
            send_massage_form.save()
            context = {
                'user': user,
                'talk_to': talk_to,
                'form': form,
                'text': text
            }
            return render(request, 'chat/user_and_user.html', context)
        else:
            print('ERROR send_massage FORM INVALID')
    context = {
        'user': user,
        'talk_to': talk_to,
        'form': form,
        'text': text
    }

    # return HttpResponse(table)

    return render(request, 'chat/user_and_user.html', context)

