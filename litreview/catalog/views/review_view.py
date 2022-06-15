from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.urls import reverse_lazy
from catalog.models import Review
from .ticket_view import TicketForm, create_context_with_ticket_according_to_pk


def create_review(request, pk=None):
    connected_user = request.user
    context = create_context_with_ticket_according_to_pk(pk)

    if request.method == "GET":
        review_form = ReviewForm()
        ticket_form = TicketForm()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = connected_user
            new_ticket.save()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            if context:
                new_review.ticket = context.get("ticket")
            else:
                new_review.ticket = new_ticket
            new_review.user = connected_user
            new_review.save()
            return HttpResponseRedirect(new_review.get_absolute_url())

    if not context:
        context["ticket_form"] = ticket_form
    context["review_form"] = review_form

    return render(request, "create_review.html", context=context)


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


def create_user_reviews_list(user):
    return list(Review.objects.all().filter(user=user).order_by("time_created"))


def create_followed_users_reviews_list(followed_users_list):
    return list(
        Review.objects.all()
        .filter(user__in=followed_users_list)
        .order_by("time_created")
    )


def create_all_reviews_list():
    return list(Review.objects.all())


def append_reviews_to_my_tickets_from_unfollowed_users(reviews_list, posts_list, user):
    for review in reviews_list:
        if review.ticket.user == user and review not in posts_list:
            posts_list.append(review)

    return posts_list
