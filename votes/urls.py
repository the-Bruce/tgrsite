from django.contrib import admin
from django.urls import path, include

from .views import ApprovalVoteView, DoneView, ApprovalResultView, HomeView, VoteView, FPTPResultView, FPTPVoteView, STVVoteView, STVResultView

app_name = "votes"

urlpatterns = [
    path('', HomeView.as_view(), name="elections"),
    path('<int:id>/', VoteView.as_view(), name="vote"),
    path('<int:id>/approval/', ApprovalVoteView.as_view(), name="approval_vote"),
    path('<int:id>/fptp/', FPTPVoteView.as_view(), name="fptp_vote"),
    path('<int:id>/stv/', STVVoteView.as_view(), name="stv_vote"),
    path('<int:election>/<uuid:slug>/', DoneView.as_view(), name="vote_done"),
    path('<int:election>/results/approval/', ApprovalResultView.as_view(), name="approval_results"),
    path('<int:election>/results/fptp/', FPTPResultView.as_view(), name="fptp_results"),
    path('<int:election>/results/stv/', STVResultView.as_view(), name="stv_results"),
]