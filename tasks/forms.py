from django import forms

from tasks.models import List, Section, Task


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name", "emoji"]


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name", "emoji"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "notes", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
