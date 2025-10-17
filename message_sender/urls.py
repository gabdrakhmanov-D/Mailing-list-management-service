from django.urls import path

from .views import HomeView, RecipientCreate, RecipientsListView, RecipientDeleteView, RecipientUpdateView

app_name = 'catalog'

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("home/list_recipients/", RecipientsListView.as_view(), name="recipients"),
    path("home/list_recipients/add_recipient/", RecipientCreate.as_view(), name="add_recipient"),
    path("home/list_recipients/edit_recipient/<int:pk>/", RecipientUpdateView.as_view(), name="edit_recipient"),
    path("home/list_recipients/recipient_confirm_delete/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
