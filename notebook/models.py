from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    PAGE_TYPE_CHOICES = [
        ("daily", "Daily"),
        ("wiki", "Wiki"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    page_type = models.CharField(max_length=10, choices=PAGE_TYPE_CHOICES, default="wiki")
    date = models.DateField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["-updated_at"]),
            models.Index(fields=["page_type", "-date"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.page_type == "daily" and self.date:
                self.slug = str(self.date)
            else:
                base_slug = slugify(self.title) or "untitled"
                slug = base_slug
                counter = 2
                while Page.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)


class PageEntityMention(models.Model):
    ENTITY_TYPE_CHOICES = [
        ("person", "Person"),
        ("organization", "Organization"),
        ("task", "Task"),
        ("project", "Project"),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="entity_mentions")
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["page", "entity_type", "entity_id"],
                name="unique_page_entity_mention",
            )
        ]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return f"{self.page} → {self.entity_type}:{self.entity_id}"


class PageLink(models.Model):
    source_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="outgoing_links")
    target_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="incoming_links")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_page", "target_page"],
                name="unique_page_link",
            )
        ]

    def __str__(self):
        return f"{self.source_page} → {self.target_page}"
