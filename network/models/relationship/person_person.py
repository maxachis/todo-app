from django.db import models
from django.db.models import Q, F


class RelationshipPersonPerson(models.Model):
    person_1 = models.ForeignKey(
        "network.Person",
        on_delete=models.CASCADE,
        related_name="relationships_outgoing",
    )
    person_2 = models.ForeignKey(
        "network.Person",
        on_delete=models.CASCADE,
        related_name="relationships_incoming",
    )

    notes = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # 1. Prevent self-relationships
            models.CheckConstraint(
                condition=~Q(person_1=F("person_2")),
                name="no_self_relationship",
            ),
            # 2. Enforce ordering so (A,B) and (B,A) can’t both exist
            models.CheckConstraint(
                condition=Q(person_1__lt=F("person_2")),
                name="enforce_person_ordering",
            ),
            # 3. Enforce uniqueness
            models.UniqueConstraint(
                fields=["person_1", "person_2"],
                name="unique_person_relationship",
            ),
        ]

    def save(self, *args, **kwargs):
        # Normalize ordering so (A,B) and (B,A) are stored consistently.
        if self.person_1_id is not None and self.person_2_id is not None:
            if self.person_1_id > self.person_2_id:
                self.person_1_id, self.person_2_id = self.person_2_id, self.person_1_id
        super().save(*args, **kwargs)
