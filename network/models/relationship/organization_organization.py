from django.db import models
from django.db.models import Q, F


class RelationshipOrganizationOrganization(models.Model):
    org_1 = models.ForeignKey(
        "network.Organization",
        on_delete=models.CASCADE,
        related_name="org_relationships_outgoing",
    )
    org_2 = models.ForeignKey(
        "network.Organization",
        on_delete=models.CASCADE,
        related_name="org_relationships_incoming",
    )

    relationship_type = models.ForeignKey(
        "network.OrgOrgRelationshipType",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    notes = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(org_1=F("org_2")),
                name="no_self_org_relationship",
            ),
            models.CheckConstraint(
                condition=Q(org_1__lt=F("org_2")),
                name="enforce_org_ordering",
            ),
            models.UniqueConstraint(
                fields=["org_1", "org_2"],
                name="unique_org_relationship",
            ),
        ]

    def save(self, *args, **kwargs):
        if self.org_1_id is not None and self.org_2_id is not None:
            if self.org_1_id > self.org_2_id:
                self.org_1_id, self.org_2_id = self.org_2_id, self.org_1_id
        super().save(*args, **kwargs)
