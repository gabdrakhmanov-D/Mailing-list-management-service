from django.shortcuts import render
from django.views.generic import TemplateView
from .models import MailingRecipient
# Create your views here.


class HomeView(TemplateView):
    model = MailingRecipient
    template_name = 'message_sender/home.html'
