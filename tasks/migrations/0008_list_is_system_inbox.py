from django.db import migrations, models


def create_inbox(apps, schema_editor):
    List = apps.get_model("tasks", "List")
    Section = apps.get_model("tasks", "Section")

    # Shift existing list positions up by 1
    List.objects.all().update(position=models.F("position") + 1)

    # Create the system Inbox list
    inbox = List.objects.create(
        name="Inbox",
        emoji="\U0001f4e5",
        position=0,
        is_system=True,
    )

    # Create a single nameless section
    Section.objects.create(list=inbox, name="", position=0)


def remove_inbox(apps, schema_editor):
    List = apps.get_model("tasks", "List")
    List.objects.filter(is_system=True, name="Inbox").delete()
    # Shift positions back down
    List.objects.all().update(position=models.F("position") - 1)


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0007_projectlink"),
    ]

    operations = [
        migrations.AddField(
            model_name="list",
            name="is_system",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(create_inbox, remove_inbox),
    ]
