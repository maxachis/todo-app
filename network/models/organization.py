from django.db import models

from network.models.org_type import OrgType


class Organization(models.Model):
    name = models.CharField(max_length=255)
    org_type = models.ForeignKey(OrgType, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_org_name"
            )
        ]

    def __str__(self):
        return self.name