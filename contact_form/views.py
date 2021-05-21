from django.views import generic
from . import forms
from django.urls import reverse_lazy


class IndexView(generic.FormView):
    template_name = "contact_form/contact_form.html"
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact_form:send_contact_success')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SendContactSuccessView(generic.TemplateView):
    template_name = "contact_form/send_contact_success.html"
