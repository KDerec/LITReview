from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from accounts.models import UserFollows


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
    connected_user = request.user
    followed_users = UserFollows.objects.all().filter(user=connected_user)
    followed_users_list = []
    for user in followed_users:
        followed_users_list.append(user.followed_user)
    users = (
        get_user_model()
        .objects.exclude(username="admin")
        .exclude(username__in=followed_users_list)
        .exclude(username=connected_user.username)
        .order_by("username")
    )
    context = {
        "users": users,
    }
    if request.method == "POST":
        id_selected_user_to_follow = request.POST.get("users-list")
        user_to_follow = users.filter(id=id_selected_user_to_follow)[0]
        create_user_follow(user_to_follow, connected_user)
        return HttpResponseRedirect("")

    return render(request, "subscription_page.html", context=context)


def create_user_follow(user_to_follow, connected_user):
    new_user_follow = UserFollows(user=connected_user, followed_user=user_to_follow)
    new_user_follow.save()
