from django.db import models

class RelationshipOrganizationPerson(models.Model):
    organization = models.ForeignKey(
        to="network.Organization",
        on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        to="network.Person",
        on_delete=models.CASCADE
    )
    notes = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)