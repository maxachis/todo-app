from django.db import models


class TaskPerson(models.Model):
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="person_links",
    )
    person = models.ForeignKey(
        "network.Person",
        on_delete=models.CASCADE,
        related_name="task_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "person"],
                name="unique_task_person_link",
            )
        ]


class TaskOrganization(models.Model):
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="organization_links",
    )
    organization = models.ForeignKey(
        "network.Organization",
        on_delete=models.CASCADE,
        related_name="task_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "organization"],
                name="unique_task_organization_link",
            )
        ]


class InteractionTask(models.Model):
    interaction = models.ForeignKey(
        "network.Interaction",
        on_delete=models.CASCADE,
        related_name="task_links",
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="interaction_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["interaction", "task"],
                name="unique_interaction_task_link",
            )
        ]
