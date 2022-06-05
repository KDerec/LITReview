from django.shortcuts import render
from django.views import generic
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from catalog.models import Ticket, Review


def feed(request):
    ticket_list = Ticket.objects.all().order_by("time_created")
    context = {
        "ticket_list": ticket_list,
    }
    return render(request, "feed.html", context=context)


def create_review(request, pk=None):
    if pk:
        ticket = Ticket.objects.filter(id=pk)
        context = {
            "ticket": ticket[0],
        }
    else:
        context = {}

    if request.method == "GET":
        form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.ticket = ticket[0]
            new_review.user = request.user
            new_review.save()
            return HttpResponseRedirect(new_review.get_absolute_url())

    context["form"] = form

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


class TicketDetailView(generic.DetailView):
    model = Ticket


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]


class ReviewDetailView(generic.DetailView):
    model = Review
