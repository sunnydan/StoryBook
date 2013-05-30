from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from stories.models import *
from django.http import HttpResponseRedirect

class RichUserCreationForm(UserCreationForm):
    # first_name = forms.CharField(label = "First name")
    # last_name = forms.CharField(label = "Last name")

    def save(self, commit=True):
        user = super(RichUserCreationForm, self).save(commit=False)
        # self.cleaned_data["first_name"]
        first_name = "First"
        # self.cleaned_data["last_name"]
        last_name = "Last"
        user.first_name = first_name
        user.last_name = last_name
        if commit:
            user.save()
            user.has_perm('adventure.add_Branch')
            user.has_perm('adventure.change_Branch')
            user.has_perm('adventure.delete_Branch')
        return user


class TokenRegistrationForm(RichUserCreationForm):
    token = forms.CharField(max_length=20, label="Registration Token")

    def clean_token(self):
        data = self.cleaned_data["token"]
        if data != settings.REGISTRATION_TOKEN:
            raise forms.ValidationError("Incorrect Registration Token!")
        return data


class AccountForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()


def edit_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            # form.cleaned_data['first_name']
            request.user.first_name = "First"
            # form.cleaned_data['last_name']
            request.user.last_name = "Last"
            request.user.save()
            return HttpResponseRedirect('/words/')
    else:
        user_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }
        form = AccountForm(user_data)
    context_dict = {'title': 'Edit Account Settings', 'form': form}
    return render_to_response('account_form.html', context_dict,
         context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST':
        if settings.REGISTRATION_TOKEN:
            form = TokenRegistrationForm(request.POST)
        else:
            form = RichUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        if settings.REGISTRATION_TOKEN:
            form = TokenRegistrationForm()
        else:
            form = RichUserCreationForm()
    return render_to_response("registration/register.html", {'form': form},
            context_instance=RequestContext(request))
