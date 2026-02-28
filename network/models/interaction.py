from django.db import models
from django.utils import timezone


class Interaction(models.Model):
    people = models.ManyToManyField(
        to="network.Person",
        related_name="interactions",
        blank=True,
    )
    organizations = models.ManyToManyField(
        to="network.Organization",
        related_name="interactions",
        blank=True,
    )
    interaction_type = models.ForeignKey(
        to="network.InteractionType",
        on_delete=models.RESTRICT,
    )
    medium = models.ForeignKey(
        to="network.InteractionMedium",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date = models.DateField(default=timezone.now)
    notes = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.interaction_type} {self.date}"

    class Meta:
        indexes = [
            models.Index(fields=["-date", "-id"]),
        ]
