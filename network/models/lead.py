from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ("prospect", "Prospect"),
        ("interested", "Interested"),
        ("committed", "Committed"),
        ("fulfilled", "Fulfilled"),
        ("unfulfilled", "Unfulfilled"),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="prospect")
    notes = models.TextField(blank=True)
    person = models.ForeignKey(
        "network.Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
    )
    organization = models.ForeignKey(
        "network.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(person__isnull=True, organization__isnull=True),
                name="lead_requires_person_or_org",
            )
        ]
        indexes = [
            models.Index(fields=["-updated_at"]),
        ]

    def __str__(self):
        return self.title
