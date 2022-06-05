from django.urls import path
from . import views


urlpatterns = [
    path("", views.feed, name="feed"),
    path("create-ticket/", views.TicketCreateView.as_view(), name="create-ticket"),
    path("ticket/<int:pk>", views.TicketDetailView.as_view(), name="ticket-detail"),
    path("create-review/", views.create_review, name="create-review"),
    path(
        "create-review/<int:pk>", views.create_review, name="create-review-from-ticket"
    ),
    path("review/<int:pk>", views.ReviewDetailView.as_view(), name="review-detail"),
]
