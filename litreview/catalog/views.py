from django.shortcuts import render
from django.views import generic
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from catalog.models import Ticket, Review
from accounts.models import UserFollows


def feed(request):
    connected_user = request.user
    followed_users_list = []
    followed_users = list(UserFollows.objects.all().filter(user=connected_user))
    for user in followed_users:
        followed_users_list.append(user.followed_user)
    current_user_tickets_list = list(Ticket.objects.all().filter(user=connected_user).order_by("time_created"))
    followed_users_tickets_list = list(Ticket.objects.all().filter(user__in=followed_users_list).order_by("time_created"))
    current_user_reviews_list = list(Review.objects.all().filter(user=connected_user).order_by("time_created"))
    followed_users_reviews_list = list(Review.objects.all().filter(user__in=followed_users_list).order_by("time_created"))
    id_list_of_ticket_with_review = []
    reviews_list = list(Review.objects.all())
    posts_list = followed_users_tickets_list + followed_users_reviews_list + current_user_tickets_list + current_user_reviews_list
    for review in reviews_list:
        if review.ticket:
            id_list_of_ticket_with_review.append(review.ticket.id)
            if review.ticket.user == connected_user and review not in posts_list:
                posts_list.append(review)

    posts_list.sort(key=lambda post: post.time_created, reverse=True)
    context = {
        "posts_list": posts_list,
        "id_list_of_ticket_with_review": id_list_of_ticket_with_review,
    }
    return render(request, "feed.html", context=context)


def my_post(request):
    tickets_list = list(
        Ticket.objects.filter(user=request.user).order_by("time_created")
    )
    reviews_list = list(
        Review.objects.filter(user=request.user).order_by("time_created")
    )
    posts_list = tickets_list + reviews_list
    posts_list.sort(key=lambda r: r.time_created, reverse=True)
    context = {
        "posts_list": posts_list,
    }
    return render(request, "my_post.html", context=context)


def create_review(request, pk=None):
    ticket_id = pk
    if ticket_id:
        ticket = Ticket.objects.filter(id=ticket_id)
        context = {
            "ticket": ticket[0],
        }
    else:
        context = {}

    if request.method == "GET":
        review_form = ReviewForm()
        ticket_form = TicketForm()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            if ticket_id:
                new_review.ticket = ticket[0]
            else:
                new_review.ticket = new_ticket
            new_review.user = request.user
            new_review.save()
            return HttpResponseRedirect(new_review.get_absolute_url())

    context["review_form"] = review_form
    if not ticket_id:
        context["ticket_form"] = ticket_form

    return render(request, "create_review.html", context=context)


class TicketCreateView(generic.edit.CreateView):
    model = Ticket
    template_name = "create_ticket.html"
    fields = ["title", "description", "image"]

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class TicketUpdateView(generic.UpdateView):
    model = Ticket
    fields = ["title", "description", "image"]
    template_name = "update_ticket.html"


class TicketDeleteView(generic.edit.DeleteView):
    model = Ticket
    success_url = reverse_lazy("catalog:my-post")
    template_name = "confirm_delete_ticket.html"


class TicketDetailView(generic.DetailView):
    model = Ticket


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]


class ReviewUpdateView(generic.UpdateView):
    model = Review
    fields = ["rating", "headline", "body"]
    template_name = "update_review.html"


class ReviewDeleteView(generic.edit.DeleteView):
    model = Review
    success_url = reverse_lazy("catalog:my-post")
    template_name = "confirm_delete_review.html"


class ReviewDetailView(generic.DetailView):
    model = Review
