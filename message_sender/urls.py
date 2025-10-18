from django.urls import path
from message_sender.views import *

app_name = 'catalog'

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("home/list_recipients/", RecipientsListView.as_view(), name="recipients"),
    path("home/list_recipients/add_recipient/", RecipientCreate.as_view(), name="add_recipient"),
    path("home/list_recipients/<int:pk>/edit_recipient/", RecipientUpdateView.as_view(), name="edit_recipient"),
    path("home/list_recipients/<int:pk>/recipient_confirm_delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("home/messages_list/", MessagesListView.as_view(), name="messages"),
    path("home/messages_list/add_message/", MessageCreate.as_view(), name="add_message"),
    path("home/messages_list/<int:pk>/edit_message/", MessageUpdateView.as_view(), name="edit_message"),
    path("home/messages_list/<int:pk>/message_confirm_delete/", MessagesDeleteView.as_view(), name="delete_message")
]
