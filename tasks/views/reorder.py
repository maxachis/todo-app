def reorder_siblings(instance, queryset, new_index):
    """Move `instance` to `new_index` within `queryset` and renumber all with gap-based positions."""
    siblings = list(queryset.exclude(pk=instance.pk).order_by("position"))
    new_index = max(0, min(len(siblings), new_index))
    siblings.insert(new_index, instance)
    for i, obj in enumerate(siblings):
        obj.position = (i + 1) * 10
        obj.save(update_fields=["position"])
