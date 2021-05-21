from django.views import generic
from . import forms
from django.urls import reverse_lazy


class IndexView(generic.FormView):
    template_name = "feedback/feedback.html"
    form_class = forms.ContactForm
    success_url = reverse_lazy('feedback:send_feedback_success')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SendFeedbackSuccessView(generic.TemplateView):
    template_name = "feedback/send_feedback_success.html"
