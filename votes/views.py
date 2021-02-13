import random
from operator import itemgetter, attrgetter

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse

from users.permissions import PERMS
from .forms import ElectionForm, CandidateForm
from .models import Election, STVVote, STVPreference, FPTPVote, APRVVote, Candidate, Ticket, Vote, STVResult
from .stv import Election as StvCalculator


# Create your views here.
class HomeView(ListView):
    template_name = "votes/home.html"
    model = Election
    context_object_name = "elections"

    def get_queryset(self):
        tickets = self.request.user.member.ticket_set.filter(spent=False)
        return Election.objects.filter(ticket__in=tickets, open=True)


class AdminView(PermissionRequiredMixin, ListView):
    permission_required = PERMS.votes.view_election
    template_name = "votes/home.html"
    model = Election
    context_object_name = "elections"

    def get_queryset(self):
        return Election.objects.all()


class CreateElection(PermissionRequiredMixin, CreateView):
    permission_required = PERMS.votes.add_election
    model = Election
    template_name = "votes/create_election.html"
    form_class = ElectionForm


class UpdateElection(PermissionRequiredMixin, UpdateView):
    permission_required = PERMS.votes.edit_election
    model = Election
    template_name = "votes/create_election.html"
    form_class = ElectionForm


class CreateCandidate(PermissionRequiredMixin, CreateView):
    permission_required = PERMS.votes.add_candidate
    model = Candidate
    template_name = "votes/create_candidate.html"
    form_class = CandidateForm

    def form_valid(self, form):
        form.instance.inventory = get_object_or_404(Election, id=self.kwargs['election'])
        return super().form_valid(form)


class UpdateCandidate(PermissionRequiredMixin, UpdateView):
    permission_required = PERMS.votes.edit_candidate
    model = Candidate
    template_name = "votes/create_candidate.html"
    form_class = CandidateForm


class DoneView(LoginRequiredMixin, DetailView):
    model = Vote
    slug_field = "uuid"

    def get_template_names(self):
        if self.election.vote_type == Election.Types.APRV:
            return "votes/approval_done.html"
        elif self.election.vote_type == Election.Types.FPTP:
            return "votes/fptp_done.html"
        elif self.election.vote_type == Election.Types.STV:
            return "votes/stv_done.html"

    def get_queryset(self):
        self.election = get_object_or_404(Election, id=self.kwargs['election'])
        return self.election.votes()


class VoteView(LoginRequiredMixin, RedirectView):
    def get_object(self):
        return get_object_or_404(Election, id=self.kwargs['election'])

    def get_redirect_url(self, *args, **kwargs):
        election = self.get_object()
        if election.vote_type == Election.Types.APRV:
            return reverse('votes:approval_vote', args=[self.kwargs['election']])
        elif election.vote_type == Election.Types.FPTP:
            return reverse('votes:fptp_vote', args=[self.kwargs['election']])
        elif election.vote_type == Election.Types.STV:
            return reverse('votes:stv_vote', args=[self.kwargs['election']])
        else:
            raise NotImplementedError()


class ApprovalResultView(PermissionRequiredMixin, ListView):
    model = Candidate
    permission_required = PERMS.votes.view_aprvvote
    template_name = "votes/approval_results.html"
    ordering = [Count("aprvvotes_set")]
    context_object_name = "choices"

    def get_queryset(self):
        self.election = get_object_or_404(Election, id=self.kwargs['election'], vote_type=Election.Types.APRV,
                                          open=False)
        return self.election.candidate_set.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['election'] = self.election
        ctxt['choices'] = sorted(ctxt['choices'], key=lambda x: -x.votes().count())
        return ctxt


class ApprovalVoteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "votes/approval_votescreen.html"

    def test_func(self):
        return self.request.user.member.ticket_set.filter(election=self.election, spent=False).exists()

    def post(self, request, **kwargs):
        self.get_context_data(**kwargs)
        ticket = get_object_or_404(request.user.member.ticket_set.all(), election=self.election, spent=False)
        print(request.POST)
        errors = []
        if "selection" not in request.POST:
            errors.append("Please select at least one option")
            selection = []
        else:
            selection = request.POST.getlist("selection")
        if 0 < self.election.max_votes < len(selection):
            errors.append("Too many options selected")
        try:
            selection = [int(s) for s in selection]
        except ValueError:
            errors.append("Invalid option submitted")
        allowed = [a.id for a in self.election.candidate_set.all()]
        for i in selection:
            if i not in allowed:
                errors.append("Unknown option selected")

        if errors:
            return self.get(request, errors=errors)
        else:
            vote = APRVVote(
                uuid=ticket.uuid,
                election=self.election,
            )
            vote.save()
            vote.selection.add(*selection)

            ticket.spent = True
            ticket.save()

            return HttpResponseRedirect(
                reverse("votes:vote_done", kwargs={'election': self.election.id, 'slug': vote.uuid}))

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        self.election = get_object_or_404(Election, id=self.kwargs['election'], open=True, vote_type=Election.Types.APRV)
        ctxt['election'] = self.election
        ctxt['choices'] = list(self.election.candidate_set.all())
        random.shuffle(ctxt['choices'])
        return ctxt


class FPTPResultView(PermissionRequiredMixin, ListView):
    model = Candidate
    permission_required = PERMS.votes.view_fptpvote
    template_name = "votes/fptp_results.html"
    ordering = [Count("fptpvotes_set")]
    context_object_name = "choices"

    def get_queryset(self):
        self.election = get_object_or_404(Election, id=self.kwargs['election'], vote_type=Election.Types.FPTP,
                                          open=False)
        return self.election.candidate_set.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['election'] = self.election
        ctxt['choices'] = sorted(ctxt['choices'], key=lambda x: -x.votes().count())
        return ctxt


class FPTPVoteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "votes/fptp_votescreen.html"

    def test_func(self):
        return self.request.user.member.ticket_set.filter(election=self.election, spent=False).exists()

    def post(self, request, **kwargs):
        self.get_context_data(**kwargs)
        ticket = get_object_or_404(request.user.member.ticket_set.all(), election=self.election, spent=False)
        print(request.POST)
        errors = []
        if "selection" not in request.POST:
            errors.append("Please select one option")
            selection = []
        else:
            selection = request.POST.get("selection")
        try:
            selection = int(selection)
        except ValueError:
            errors.append("Invalid option submitted")
        allowed = [a.id for a in self.election.candidate_set.all()]
        if selection not in allowed:
            errors.append("Unknown option selected")

        if errors:
            return self.get(request, errors=errors)
        else:
            vote = FPTPVote(
                uuid=ticket.uuid,
                election=self.election,
                selection_id=selection
            )
            vote.save()

            ticket.spent = True
            ticket.save()

            return HttpResponseRedirect(
                reverse("votes:vote_done", kwargs={'election': self.election.id, 'slug': vote.uuid}))

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        self.election = get_object_or_404(Election, id=self.kwargs['election'], open=True, vote_type=Election.Types.FPTP)
        ctxt['election'] = self.election
        ctxt['choices'] = list(self.election.candidate_set.all())
        random.shuffle(ctxt['choices'])
        return ctxt


class STVResultView(PermissionRequiredMixin, ListView):
    model = Candidate
    permission_required = PERMS.votes.view_stvvote
    template_name = "votes/stv_results.html"
    context_object_name = "choices"

    def get_queryset(self):
        self.election = get_object_or_404(Election, id=self.kwargs['election'], vote_type=Election.Types.STV,
                                          open=False)
        return self.election.candidate_set.all()

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        ctxt['election'] = self.election
        try:
            res = self.election.stvresult
        except STVResult.DoesNotExist:
            candidates = set(map(attrgetter('id'), self.election.candidate_set.all()))
            withdrawn = set(map(attrgetter('id'), self.election.candidate_set.filter(state=Candidate.State.WITHDRAWN)))
            votes = []
            for i in self.election.stvvote_set.all():
                vote = []
                for j in STVPreference.objects.filter(stvvote=i).order_by('order'):
                    vote.append(int(j.candidate_id))
                votes.append(tuple(vote))

            calc = StvCalculator(candidates, votes, self.election.seats)
            calc.withdraw(withdrawn)
            calc.full_election()
            res = STVResult.objects.create(election=self.election, full_log="\n".join(calc.fulllog))
            res.save()
            res.winners.add(*Candidate.objects.filter(id__in=calc.winners()))
        ctxt['result'] = res
        return ctxt


class STVVoteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "votes/stv_votescreen.html"

    def test_func(self):
        return self.request.user.member.ticket_set.filter(election=self.election, spent=False).exists()

    def post(self, request, **kwargs):
        self.get_context_data(**kwargs)
        ticket = get_object_or_404(request.user.member.ticket_set.all(), election=self.election, spent=False)
        print(request.POST)
        errors = []
        allowed = set(a.id for a in self.election.candidate_set.all())

        # Almost all of these errors should never be seen (unless someone is bypassing the js)
        submitted_candidates = set(request.POST.keys())
        submitted_candidates.remove('csrfmiddlewaretoken')  # remove csrf token (the only valid non-vote value)
        try:
            submitted_candidates = set(map(int, submitted_candidates))
        except ValueError:
            errors.append("Unknown option submitted (non integer key)")
        if submitted_candidates.difference(allowed):
            errors.append("Unknown option submitted (unknown candidate)")
        if allowed.difference(submitted_candidates):
            errors.append("Missing option")

        selection = []
        for i in submitted_candidates:
            selection.append((i, request.POST.get(str(i))))

        print(selection)
        try:
            selection = [(s, int(v)) for s, v in selection if v != ""]
        except ValueError:
            errors.append("Invalid preference (non-integer)")
        for k, v in selection:
            if v not in range(1, len(selection) + 1):
                errors.append("Invalid preference (out of range)")
        if len(selection) != len(set(map(itemgetter(1), selection))):
            errors.append("Invalid preference (repeated)")
        if len(selection) == 0:
            errors.append("Please select at least one candidate")  # This one is actually possible

        if errors:
            return self.get(request, errors=set(errors), previous=request.POST)
        else:
            vote = STVVote(
                uuid=ticket.uuid,
                election=self.election,
            )
            vote.save()
            for i in selection:
                STVPreference.objects.create(stvvote=vote, candidate_id=i[0], order=i[1])

            ticket.spent = True
            ticket.save()

            return HttpResponseRedirect(
                reverse("votes:vote_done", kwargs={'election': self.election.id, 'slug': vote.uuid}))

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        self.election = get_object_or_404(Election, id=self.kwargs['election'], open=True, vote_type=Election.Types.STV)
        ctxt['election'] = self.election
        ctxt['choices'] = list(self.election.candidate_set.all())
        random.shuffle(ctxt['choices'])
        return ctxt


def maybeint(string):
    try:
        return int(string)
    except ValueError:
        return None
