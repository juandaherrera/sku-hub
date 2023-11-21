from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy


class FormInvalidMixin:
    """
    Mixin validator of forms that come from a modal window
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class PrivilegesRequired(LoginRequiredMixin, PermissionRequiredMixin, FormInvalidMixin):
    """
    A mixin class that enforces user authentication and permission checks, combined with custom handling of invalid
    forms. This class is designed to be used as a mixin with Django's class-based views to ensure that only
    authenticated users with the required permissions can access a view. It also provides a mechanism to handle
    invalid form submissions, especially useful in AJAX requests.

    Args:
        LoginRequiredMixin (Mixin): A mixin from Django's auth module that ensures a user is logged in before
        accessing a view. If the user is not authenticated, they are redirected to the specified login URL.

        PermissionRequiredMixin (Mixin): A mixin from Django's auth module that checks if the current user has the
        required permissions set for the view. If the user does not have the required permissions, they are handled
        by the 'handle_no_permission' method.

        FormInvalidMixin (Mixin): A custom mixin to handle invalid form submissions. If the form submission is via
        an AJAX request, it returns a JsonResponse with form errors; otherwise, it follows the standard form invalid
        handling process.

    Attributes:
        login_url (str): The URL to redirect unauthenticated users to. Defaults to 'Core:login'.

        raise_exception (bool): If set to True, raises an exception when the user lacks permissions instead of
        redirecting. Defaults to False for a user-friendly redirection.

        redirect_field_name (str): The name of the query parameter added to the login URL when redirecting
        unauthenticated users. It holds the URL they were trying to access. Defaults to "redirect_to".
    """

    login_url = 'Core:login'

    raise_exception = False

    redirect_field_name = 'redirect_to'

    def handle_no_permission(self):
        if not self.request.user == AnonymousUser():
            self.login_url = "Core:no_privileges"
        return HttpResponseRedirect(reverse_lazy(self.login_url))
