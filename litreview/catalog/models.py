from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.urls import reverse


class Ticket(models.Model):
    """Stores a ticket related to :model:`auth.User`."""

    title = models.CharField(
        max_length=128, help_text="Titre du livre ou de l'article de la demande."
    )
    description = models.TextField(
        max_length=2048, blank=True, help_text="Description relative à la demande."
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:ticket-detail", args=[str(self.id)])


class Review(models.Model):
    """
    Stores a review related to a :model:`catalog.Ticket` and
    :model:`auth.User`.
    """

    rating_min_value = 0
    rating_max_value = 5
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(rating_min_value),
            MaxValueValidator(rating_max_value),
        ],
        help_text="Note de la critique allant de 1 à 5.",
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, help_text="Titre de la critique.")
    body = models.TextField(
        max_length=8192, blank=True, help_text="Corps de la critique."
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("catalog:review-detail", args=[str(self.id)])

    def return_star_rating(self):
        """Return a string of unicode star according to self rating."""
        stars = ""
        for i in range(self.rating):
            stars = stars + "★"
        while len(stars) < self.rating_max_value:
            stars = stars + "☆"

        return stars
