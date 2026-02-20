from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, blank=True, default="")
    position = models.IntegerField(default=0)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="lists"
    )

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
    PRIORITY_NONE = 0
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 3
    PRIORITY_HIGH = 5
    PRIORITY_CHOICES = [
        (PRIORITY_NONE, "None"),
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

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
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=PRIORITY_NONE)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    position = models.IntegerField(default=0)
    external_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title

    @property
    def open_subtask_count(self):
        """Return the number of non-completed direct subtasks."""
        return self.subtasks.filter(is_completed=False).count()

    def complete(self):
        """Mark this task and all descendant subtasks as completed."""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()
        for subtask in self.subtasks.filter(is_completed=False):
            subtask.complete()

    def uncomplete(self):
        """Mark this task as not completed."""
        self.is_completed = False
        self.completed_at = None
        self.save()


class TimeEntry(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="time_entries"
    )
    tasks = models.ManyToManyField("Task", blank=True, related_name="time_entries")
    description = models.CharField(max_length=500, blank=True, default="")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.project.name} - {self.date}"
