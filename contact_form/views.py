from django.views import generic
from . import forms
from django.urls import reverse_lazy


class IndexView(generic.FormView):
    template_name = "contact_form/contact_form.html"
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact_form:index')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
