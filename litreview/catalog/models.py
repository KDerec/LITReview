from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.urls import reverse


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by"
    )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )

    def __str__(self):
        return f"{self.user}, {self.followed_user}"


class Ticket(models.Model):
    title = models.CharField(
        max_length=128, help_text="Insérez le titre du livre ou de l'article."
    )
    description = models.TextField(
        max_length=2048, blank=True, help_text="Exprimez votre demande."
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:ticket-detail", args=[str(self.id)])


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Renseignez une note allant de 0 à 5.",
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(
        max_length=128, help_text="Renseignez un titre à votre critique."
    )
    body = models.TextField(
        max_length=8192, blank=True, help_text="Renseignez votre critique."
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("catalog:review-detail", args=[str(self.id)])
