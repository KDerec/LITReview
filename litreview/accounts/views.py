from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect


def redirect_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/catalog/")
    else:
        return HttpResponseRedirect("/home/")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = "/accounts/home/"
    template_name = "registration/signup.html"
