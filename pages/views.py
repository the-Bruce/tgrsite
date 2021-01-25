from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages import add_message, WARNING

from .models import Page


class ViewPage(UserPassesTestMixin, generic.DetailView):
    model = Page
    slug_field = 'name'
    slug_url_kwarg = 'name'
    context_object_name = 'page'
    template_name = "pages/page.html"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        o = self.get_object()
        if o.permission == Page.Permissions.PUBLIC:
            return True
        if self.request.user.is_authenticated:
            if o.permission == Page.Permissions.USER:
                return self.request.user.is_authenticated
            elif o.permission == Page.Permissions.MEMBER:
                return (self.request.user.member.is_exec()
                        or self.request.user.member.is_ex_exec()
                        or self.request.user.member.is_soc_member)
            elif o.permission == Page.Permissions.EX_EXEC:
                return (self.request.user.member.is_exec()
                        or self.request.user.member.is_ex_exec())
            elif o.permission == Page.Permissions.EXEC:
                return self.request.user.member.is_exec()
            else:
                raise NotImplemented("Invalid Page Permission Value")
        else:
            add_message(self.request, WARNING, "Please log in to see that page")
            return False
