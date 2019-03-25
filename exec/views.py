from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .forms import ExecBioForm
from .models import ExecRole


def index(request):
    context = {
        'execs': ExecRole.objects.all().order_by('sort_index')
    }
    return render(request, 'exec/index.html', context)


# This is hella boilerplate but I didn't want to wrangle with the weirdness of generic views
@login_required
def editbio(request, pk):
    # role = ExecRole.objects.get(id=pk)
    role = get_object_or_404(ExecRole, id=pk)

    if request.user.member != role.incumbent:
        return HttpResponseForbidden()

    form = ExecBioForm(instance=role)
    context = {'rolename': role.role_title, 'form': form, 'pk': pk}
    return render(request, 'exec/editbio.html', context)


@login_required
def editbio_done(request, pk):
    role = ExecRole.objects.get(id=pk)
    form = ExecBioForm(request.POST)
    if form.is_valid():
        role.bio = form.cleaned_data['bio']
        role.save()
        return HttpResponseRedirect(reverse_lazy('exec'))
    else:
        return HttpResponseRedirect(reverse_lazy('exec_editbio', kwargs={'pk': pk}) + '?message=invalid')
