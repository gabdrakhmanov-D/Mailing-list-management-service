from django.urls import path

from messages_for_clients.views import *

app_name = 'messages_for_clients'

urlpatterns = [
    path("home/messages_list/", MessagesListView.as_view(), name="messages"),
    path("home/messages_list/add_message/", MessageCreate.as_view(), name="add_message"),
    path("home/messages_list/<int:pk>/edit_message/", MessageUpdateView.as_view(), name="edit_message"),
    path("home/messages_list/<int:pk>/message_confirm_delete/", MessagesDeleteView.as_view(), name="delete_message"),
    ]
