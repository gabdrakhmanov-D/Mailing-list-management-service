from django.urls import path

from messages_for_clients.views import *

app_name = 'messages_for_clients'

urlpatterns = [
    path("messages/messages_list/", MessagesListView.as_view(), name="messages_list"),
    path("messages/add_message/", MessageCreate.as_view(), name="add_message"),
    path("messages/<int:pk>/edit_message/", MessageUpdateView.as_view(), name="edit_message"),
    path("messages/<int:pk>/message_confirm_delete/", MessagesDeleteView.as_view(), name="delete_message"),
    ]
