from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    linkedin_url = models.CharField(max_length=500, blank=True)
    notes = models.TextField(
        blank=True
    )
    follow_up_cadence_days = models.IntegerField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_person_name"
            )
        ]
        indexes = [
            models.Index(fields=["last_name", "first_name", "id"]),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} "
