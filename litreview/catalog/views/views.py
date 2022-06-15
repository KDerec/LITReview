from django.shortcuts import render
from accounts.views import create_followed_users_list
from .ticket_view import (
    create_ticket_id_list_with_review,
    create_user_tickets_list,
    create_followed_users_tickets_list,
)
from .review_view import (
    append_reviews_to_my_tickets_from_unfollowed_users,
    create_all_reviews_list,
    create_user_reviews_list,
    create_followed_users_reviews_list,
)


def feed(request):
    """
    Display tickets and reviews of the connected user and users he is following.

    **Templates:**

    :template:`feed.html`
    """
    connected_user = request.user
    followed_users_list = create_followed_users_list(connected_user)
    current_user_tickets_list = create_user_tickets_list(connected_user)
    current_user_reviews_list = create_user_reviews_list(connected_user)
    followed_users_tickets_list = create_followed_users_tickets_list(
        followed_users_list
    )
    followed_users_reviews_list = create_followed_users_reviews_list(
        followed_users_list
    )
    posts_list = (
        current_user_tickets_list
        + current_user_reviews_list
        + followed_users_tickets_list
        + followed_users_reviews_list
    )
    reviews_list = create_all_reviews_list()
    ticket_id_list_with_review = create_ticket_id_list_with_review(reviews_list)
    posts_list = append_reviews_to_my_tickets_from_unfollowed_users(
        reviews_list, posts_list, connected_user
    )
    posts_list = sort_posts_list_by_time_created(posts_list)

    context = {
        "posts_list": posts_list,
        "ticket_id_list_with_review": ticket_id_list_with_review,
    }

    return render(request, "feed.html", context=context)


def my_post(request):
    """
    Display tickets and reviews of the connected user.

    **Templates:**

    :template:`my_post.html`
    """
    connected_user = request.user
    current_user_tickets_list = create_user_tickets_list(connected_user)
    current_user_reviews_list = create_user_reviews_list(connected_user)
    posts_list = current_user_tickets_list + current_user_reviews_list
    posts_list = sort_posts_list_by_time_created(posts_list)
    context = {
        "posts_list": posts_list,
    }

    return render(request, "my_post.html", context=context)


def sort_posts_list_by_time_created(posts_list):
    """Return posts list sorted by "time_created" attribut."""
    return sorted(posts_list, key=lambda post: post.time_created, reverse=True)
