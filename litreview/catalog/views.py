from django.shortcuts import render
from django.views import generic
from catalog.models import Ticket, Review


def feed(request):
    ticket_list = Ticket.objects.all().order_by("time_created")
    context = {
        "ticket_list": ticket_list,
    }
    return render(request, "feed.html", context=context)


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


class TicketDetailView(generic.DetailView):
    model = Ticket
