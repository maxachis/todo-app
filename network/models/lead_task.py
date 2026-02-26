from django.db import models


class LeadTask(models.Model):
    lead = models.ForeignKey(
        "network.Lead",
        on_delete=models.CASCADE,
        related_name="task_links",
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="lead_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lead", "task"],
                name="unique_lead_task_link",
            )
        ]
