from django.urls import path
from . import views


urlpatterns = [
    path("", views.feed, name="feed"),
    path("feed/", views.feed, name="feed"),
    path("create-ticket/", views.TicketCreateView.as_view(), name="create-ticket"),
    path("ticket/<int:pk>", views.TicketDetailView.as_view(), name="ticket-detail"),
]
