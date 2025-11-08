from django.urls import path

from message_sender.views import MailingListView, MailingAttemptView, MailingCreate, MailingUpdateView, \
    MailingDeleteView, start_mailing, hide_mailing, activ_mailing

app_name = 'message_sender'

urlpatterns = [
    path("message_sender/mailing_list/", MailingListView.as_view(), name="mailing"),
    path("message_sender/mailing_statistics/", MailingAttemptView.as_view(), name="statistics"),
    path("message_sender/add_mailing/", MailingCreate.as_view(), name="add_mailing"),
    path("message_sender/<int:pk>/edit_mailing/", MailingUpdateView.as_view(), name="edit_mailing"),
    path("message_sender/<int:pk>/mailing_confirm_delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("message_sender/<int:pk>/start/", start_mailing, name="start"),
    path("message_sender/<int:mailing_id>/hide_mailing/", hide_mailing, name="hide"),
    path("message_sender/<int:mailing_id>/activ_mailing/", activ_mailing, name="activ")
]
