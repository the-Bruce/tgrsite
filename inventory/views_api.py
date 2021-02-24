from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from notifications.models import NotifType
from notifications.utils import notify
from users.permissions import PERMS
from .models import Loan, Suggestion


@require_http_methods(["POST"])
@permission_required(PERMS.inventory.change_suggestion)
def archiveSuggestion(request, pk):
    item = get_object_or_404(Suggestion, pk=pk)
    item.archived = True
    item.save()
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required(PERMS.inventory.can_authorise)
def rejectLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.rejected = request.user.member
    item.save()
    notify(item.requester, NotifType.LOAN_REQUESTS, f"A pending loan request has been rejected.",
                                  reverse('inventory:loan_detail',
                                          kwargs={'inv': item.inventory.canonical_(), 'pk': item.id}))
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required(PERMS.inventory.can_authorise)
def authoriseLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.authorised = request.user.member
    item.save()
    notify(item.requester, NotifType.LOAN_REQUESTS,
                                  f"A pending loan request has been authorised.",
                                  reverse('inventory:loan_detail',
                                          kwargs={'inv': item.inventory.canonical_(), 'pk': item.id}))
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required(PERMS.inventory.can_witness)
def takeLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.taken_who = request.user.member
    item.taken_when = datetime.now()
    item.save()
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required(PERMS.inventory.can_witness)
def returnLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.returned_who = request.user.member
    item.returned_when = datetime.now()
    item.save()
    return redirect(item.get_absolute_url())
