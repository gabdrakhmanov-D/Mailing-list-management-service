from django.urls import path
from message_sender.views import *

app_name = 'catalog'

urlpatterns = [
    path("home/messages_list/", MessagesListView.as_view(), name="messages"),
    path("home/messages_list/add_message/", MessageCreate.as_view(), name="add_message"),
    path("home/messages_list/<int:pk>/edit_message/", MessageUpdateView.as_view(), name="edit_message"),
    path("home/messages_list/<int:pk>/message_confirm_delete/", MessagesDeleteView.as_view(), name="delete_message"),
    path("home/mailing_list/", MailingListView.as_view(), name="mailing"),
    path("home/mailing_list/add_mailing/", MailingCreate.as_view(), name="add_mailing"),
    path("home/mailing_list/<int:pk>/edit_mailing/", MailingUpdateView.as_view(), name="edit_mailing"),
    path("home/mailing_list/<int:pk>/mailing_confirm_delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    ]
