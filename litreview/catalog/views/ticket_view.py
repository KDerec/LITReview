from django.views import generic
from django.urls import reverse_lazy
from django.forms import ModelForm
from catalog.models import Ticket


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


def create_user_tickets_list(user):
    return list(Ticket.objects.all().filter(user=user).order_by("time_created"))


def create_followed_users_tickets_list(followed_users_list):
    return list(
        Ticket.objects.all()
        .filter(user__in=followed_users_list)
        .order_by("time_created")
    )


def create_ticket_id_list_with_review(reviews_list):
    ticket_id_list_with_review = []
    for review in reviews_list:
        if review.ticket:
            ticket_id_list_with_review.append(review.ticket.id)

    return ticket_id_list_with_review


def create_context_with_ticket_according_to_pk(pk):
    if pk:
        ticket = Ticket.objects.filter(id=pk)
        context = {"ticket": ticket[0]}
    else:
        context = {}

    return context
