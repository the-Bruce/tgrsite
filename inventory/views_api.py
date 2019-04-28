from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Loan, Suggestion


@require_http_methods(["POST"])
@permission_required('change_suggestion')
def archiveSuggestion(request, pk):
    item = get_object_or_404(Suggestion, pk=pk)
    item.archived = True
    item.save()
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required('can_authorise')
def rejectLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.rejected = request.user.member
    item.save()
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required('can_authorise')
def authoriseLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.authorised = request.user.member
    item.save()
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required('can_witness')
def takeLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.taken_who = request.user.member
    item.taken_when = datetime.now()
    item.save()
    return redirect(item.get_absolute_url())


@require_http_methods(["POST"])
@permission_required('can_witness')
def returnLoan(request, pk):
    item = get_object_or_404(Loan, pk=pk)
    item.returned_who = request.user.member
    item.returned_when = datetime.now()
    item.save()
    return redirect(item.get_absolute_url())
