from django.db import models


class ContactDraft(models.Model):
    name = models.CharField(max_length=255)
    quick_notes = models.TextField(blank=True, default="")
    source_page = models.ForeignKey(
        "notebook.Page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_drafts",
    )
    promoted_to_person = models.ForeignKey(
        "network.Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_drafts",
    )
    promoted_to_org = models.ForeignKey(
        "network.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_drafts",
    )
    dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_pending(self):
        return (
            self.promoted_to_person_id is None
            and self.promoted_to_org_id is None
            and not self.dismissed
        )
