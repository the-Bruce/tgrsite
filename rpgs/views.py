from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# testing
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from notifications.models import NotifType, notify_everybody, notify
from users.models import Member
from .forms import RpgForm
from .models import Rpg, Tag
from .templatetags.rpg_tags import can_manage


# list view
# TODO: paginate
class Index(generic.ListView):
    template_name = 'rpgs/index.html'
    model = Rpg
    context_object_name = 'rpgs'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('showfinished',False):
            return Rpg.objects.order_by('-created_at')
        else:
            return Rpg.objects.filter(is_in_the_past=False).order_by('-created_at')


class Detail(generic.DetailView):
    template_name = 'rpgs/rpg.html'
    model = Rpg
    context_object_name = 'rpg'


# list view filtered by tag
class Filter(Index):
    def get_queryset(self):
        return Rpg.objects.filter(tags__name=self.kwargs['tag'])


# takes a POST form and redirects to the Filter view
def tag_form(request):
    tag = request.POST.get('tag')
    if tag == '' or tag == None:
        return HttpResponseRedirect(reverse('rpgs'))
    return HttpResponseRedirect(reverse('rpg_tag', kwargs={'tag': tag}))


@login_required
def join(request):
    rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
    if rpg.members.count() < rpg.players_wanted:
        rpg.members.add(request.user.member)
        url = reverse('rpg', kwargs={'pk': request.POST.get('id')})
        notify(rpg.creator, NotifType.RPG_JOIN,
               'User {} joined your game "{}"!'.format(request.user.username, rpg.title), url)
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(reverse('rpg', kwargs={'pk': request.POST.get('id')}) + '?error=full')


@login_required
def leave(request):
    rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
    rpg.members.remove(request.user.member)
    url = reverse('rpg', kwargs={'pk': request.POST.get('id')})
    notify(rpg.creator, NotifType.RPG_LEAVE, 'User {} left your game "{}".'.format(request.user.username, rpg.title),
           url)
    return HttpResponseRedirect(url)


@login_required
def create(request):
    return render(request, 'rpgs/create.html', {'form': RpgForm})


@login_required
def kick(request):
    rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
    if request.user.member == rpg.creator:
        rpg.members.remove(request.POST.get('user-to-remove'))
        notify(User.objects.get(member__id=request.POST.get('user-to-remove')).member, NotifType.RPG_KICK,
               'You were kicked from the game "{}".'.format(rpg.title), reverse('rpg', kwargs={'pk': request.POST.get('id')}))
    return HttpResponseRedirect(reverse('rpg', kwargs={'pk': request.POST.get('id')}) + '?nousername=1')


@login_required
def add_to(request):
    """ adds a player to an RPG using the `username` and `id` fields of form"""
    # Notes: could do this through a URLconf instead?
    # /rpg/<id>/add/<username>? userid instead of username?

    # TODO: This 404 doesn't fire, it just fails silently.
    # Might work to instead try/except and redirect back with error?
    # Also worth noting that this kind of form is exactly the kind of thing
    # that could be enhanced with AJAX, and that could shape the response structure.
    rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
    url = reverse('rpg', kwargs={'pk': request.POST.get('id')})
    if request.user.member == rpg.creator:
        users = User.objects.filter(username=request.POST.get('username'))
        if users.count() == 0:
            return HttpResponseRedirect(reverse('rpg', kwargs={'pk': request.POST.get('id')}))
        rpg.members.add(users[0].member.id)
        notify(users[0].member, NotifType.RPG_ADDED, 'You were added to the game "{}".'.format(rpg.title), url)
    return HttpResponseRedirect(url)


@login_required
def create_done(request):
    # create a new RPG from all the form's fields
    # except the middleware token
    # and am_i_gm which is used here instead
    # Probably not required? Pretty sure fields not in the model are ignored...
    args = {i: request.POST.get(i, None) for i in request.POST if
            i != 'am_i_gm' and i != 'tags' and i != 'csrfmiddlewaretoken'}

    args['creator_id'] = request.user.member.id

    # weird shit
    try:
        if args['is_in_the_past'] == 'on':
            args['is_in_the_past'] = True
        else:
            args['is_in_the_past'] = False
    # if the box is unchecked I think it's just omitted so bleh
    except KeyError:
        args['is_in_the_past'] = False

    # Make a form in order to validate the data
    fargs = RpgForm(args)

    if not fargs.is_valid():
        # TODO: Better error!
        return HttpResponse('Unknown error: RpgForm is not valid')

    me = Member.objects.get(id=request.user.member.id)

    ins = Rpg(**args)
    try:
        ins.full_clean()
    except ValidationError:
        # Unlikely to ever be reached, but assuming that the form validates everything is not always the best plan...
        return HttpResponse('Unknown error: RpgForm is not valid')
    ins.save()

    # add tags
    ins.tags.set(tags_from_str(request.POST.get('tags', '')))

    if (request.POST.get('am_i_gm', None)):
        ins.game_masters.add(me)

    notify_everybody(NotifType.RPG_CREATE, "New Events are available for signup.",
                     reverse('rpg', kwargs={'pk': ins.id}), merge_key=ins.id)
    # send them to the page that was created
    return HttpResponseRedirect(reverse('rpg', kwargs={'pk': ins.id}) + '?status=created')


# not a view
def tags_from_str(str):
    tags = []
    for tag in str.split(','):
        if tag.strip() == '':
            continue
        tags.append(Tag.objects.get_or_create(name=tag.strip().lower())[0])
    return tags


@login_required
def edit(request, pk):
    rpg = get_object_or_404(Rpg, id=pk)
    # TODO: Test permission code
    if rpg.creator.equiv_user.id != request.user.id:
        return HttpResponseForbidden()
    form = RpgForm(instance=rpg, initial={'tags': rpg.tags_str()})
    context = {'form': form, 'id': pk, 'rpg': rpg}
    return render(request, 'rpgs/edit.html', context)


@login_required
def edit_process(request, pk):
    rpg = get_object_or_404(Rpg, id=pk)
    if not can_manage(request.user.member, rpg):
        return HttpResponseForbidden()
    form = RpgForm(
        request.POST,
        instance=rpg
    )
    if (form.is_valid):
        """newtags = []
        for tag in form.data['tags'].split(','):
            # determine new tag
            newtags.append(Tag.objects.get_or_create(name=tag)[0])"""

        # change tags
        rpg.tags.set(tags_from_str(form.data['tags']))

        # cleanup?
        # remove tags that have no uses
        for tag in Tag.objects.all():
            if (tag.rpg_set.count() == 0):
                tag.delete()

        form.save()
        return HttpResponseRedirect(reverse('rpg', kwargs={'pk': pk}))
    else:
        # TODO: Proper errors
        return HttpResponseBadRequest()


@login_required
def delete(request, pk):
    # TODO: ask user for confirmation !
    rpg = get_object_or_404(Rpg, id=pk)

    if not can_manage(request.user.member, rpg):
        return HttpResponseForbidden()

    rpg.delete()
    return HttpResponseRedirect(reverse('rpgs'))
