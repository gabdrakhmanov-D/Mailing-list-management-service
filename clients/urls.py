from django.urls import path

from clients.views import RecipientsListView, RecipientCreate, RecipientUpdateView, RecipientDeleteView

app_name = 'clients'
urlpatterns = [
    path("clients/list_recipients/", RecipientsListView.as_view(), name="recipients"),
    path("clients/list_recipients/add_recipient/", RecipientCreate.as_view(), name="add_recipient"),
    path("clients/list_recipients/<int:pk>/edit_recipient/", RecipientUpdateView.as_view(), name="edit_recipient"),
    path("clients/list_recipients/<int:pk>/recipient_confirm_delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    ]