from django.urls import path
from message_sender.views import *

app_name = 'catalog'

urlpatterns = [
    path("home/mailing_list/", MailingListView.as_view(), name="mailing"),
    path("home/mailing_list/add_mailing/", MailingCreate.as_view(), name="add_mailing"),
    path("home/mailing_list/<int:pk>/edit_mailing/", MailingUpdateView.as_view(), name="edit_mailing"),
    path("home/mailing_list/<int:pk>/mailing_confirm_delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    ]
