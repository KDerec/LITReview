from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserFollows


class SignUpView(CreateView):
    """
    Display the user creation form and handle the sign up action to create an
    user account.

    **Templates:**

    :template:`registration/signup.html`
    """

    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:home")
    template_name = "registration/signup.html"


def redirect_view(request):
    """Redirect to url if user is connected or not."""
    if request.user.is_authenticated:
        return HttpResponseRedirect("/catalog/")
    else:
        return HttpResponseRedirect("/home/")


def subscription(request):
    """
    Display selectable users to follow, followed users and subscribers.
    When POST method, call functions to achieve UserFollows object creation.

    **Templates:**

    :template:`subscription_page.html`
    """
    connected_user = request.user
    followed_users_list = create_followed_users_list(connected_user)
    subscribers_list = create_subscribers_list(connected_user)
    followable_users = (
        get_user_model()
        .objects.exclude(username="admin")
        .exclude(username__in=followed_users_list)
        .exclude(username=connected_user.username)
        .order_by("username")
    )

    context = {
        "followable_users": followable_users,
        "followed_users_list": followed_users_list,
        "subscribers_list": subscribers_list,
    }

    if request.method == "POST":
        user_to_follow = get_user_to_follow(request)
        if user_to_follow:
            create_user_follow(user_to_follow, connected_user)
        else:
            context["message"] = "Cet utilisateur n'existe pas."
            return render(request, "subscription_page.html", context=context)

        return HttpResponseRedirect("/accounts/subscription/")

    return render(request, "subscription_page.html", context=context)


def create_followed_users_list(user):
    """Create and return a list of followed users of the user in argument."""
    followed_users_list = []
    followed_users = UserFollows.objects.all().filter(user=user)
    for user in followed_users:
        followed_users_list.append(user.followed_user)

    return followed_users_list


def create_subscribers_list(user):
    """Create and return a list of subscribers of the user in argument."""
    subscribers_list = []
    subscribed_users = UserFollows.objects.all().filter(followed_user=user)
    for user in subscribed_users:
        subscribers_list.append(user.user)

    return subscribers_list


def get_user_to_follow(request):
    chosen_username = request.POST.get("followable-users-choice")
    user_to_follow = get_user_model().objects.filter(username=chosen_username)
    if user_to_follow:
        return user_to_follow


def create_user_follow(user_to_follow, connected_user):
    """Create an instance of UserFollow and save it in the db."""
    UserFollows(user=connected_user, followed_user=user_to_follow[0]).save()


def delete_user_follows(request, pk):
    """
    Select a UserFollows object in db according to connected user and
    followed user with his id (pk) and delete the selected object.
    """
    if request.method == "POST":
        UserFollows.objects.all().filter(user=request.user, followed_user=pk).delete()

    return HttpResponseRedirect("/accounts/subscription/")
