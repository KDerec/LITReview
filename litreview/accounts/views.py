from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render
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
    success_url = reverse_lazy("accounts:home")
    template_name = "registration/signup.html"


def subscription(request):
    user = get_user_model()
    users = user.objects.exclude(username="admin").order_by("username")
    context = {
        "users": users,
    }
    return render(request, "subscription_page.html", context=context)
