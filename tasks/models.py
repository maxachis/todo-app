from django.db import models
from django.utils import timezone


class List(models.Model):
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, blank=True, default="")
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        prefix = f"{self.emoji} " if self.emoji else ""
        return f"{prefix}{self.name}"


class Section(models.Model):
    list = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name="sections"
    )
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, blank=True, default="")
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        prefix = f"{self.emoji} " if self.emoji else ""
        return f"{prefix}{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="tasks"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subtasks",
    )
    title = models.CharField(max_length=500)
    notes = models.TextField(blank=True, default="")
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    position = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title

    def complete(self):
        """Mark this task as completed."""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def uncomplete(self):
        """Mark this task as not completed."""
        self.is_completed = False
        self.completed_at = None
        self.save()
