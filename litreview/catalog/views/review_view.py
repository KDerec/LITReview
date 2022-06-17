from django import forms
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from catalog.models import Review
from .ticket_view import TicketForm, create_context_with_ticket_according_to_pk


class ReviewForm(forms.ModelForm):
    """Create a Form class from Review model."""

    choices = [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]
    rating = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]


class ReviewUpdateView(generic.UpdateView):
    """
    Display a form for editing existing Review object.

    **Templates:**

    :template:`update_review.html`
    """

    model = Review
    fields = ["rating", "headline", "body"]
    template_name = "update_review.html"


class ReviewDeleteView(generic.edit.DeleteView):
    """
    Display a confirmation page and deletes an existing Review object.

    **Templates:**

    :template:`confirm_delete_review.html`
    """

    model = Review
    success_url = reverse_lazy("catalog:my-post")
    template_name = "confirm_delete_review.html"


class ReviewDetailView(generic.DetailView):
    """
    Display details of an existing Review object in a page.

    **Templates:**

    :template:`review_detail.html`
    """

    model = Review


def create_review(request, pk=None):
    """
    Display a form for creating an Review object and save the object.

    **Templates:**

    :template:`create_review.html`
    """
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


def create_user_reviews_list(user):
    """
    Return a list of Review objects filtered by an user and ordered by
    creation time.
    """
    return list(Review.objects.all().filter(user=user).order_by("time_created"))


def create_followed_users_reviews_list(followed_users_list):
    """
    Return a list of Review objects filtered by a list of followed user
    and ordered by creation time.
    """
    return list(
        Review.objects.all()
        .filter(user__in=followed_users_list)
        .order_by("time_created")
    )


def create_all_reviews_list():
    """Return a list of all Review objects."""
    return list(Review.objects.all())


def append_reviews_to_my_tickets_from_unfollowed_users(reviews_list, posts_list, user):
    """
    Uses a list of posts and return this same list containing in addition the
    reviews of the connected user's tickets not coming from his subscriptions.
    """
    for review in reviews_list:
        if review.ticket.user == user and review not in posts_list:
            posts_list.append(review)

    return posts_list
