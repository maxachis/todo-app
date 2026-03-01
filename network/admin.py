from django.contrib import admin

from network.models import Person, Organization, RelationshipOrganizationPerson, RelationshipPersonPerson, Interaction, \
    InteractionType, OrgType, PersonPersonRelationshipType, OrgPersonRelationshipType

# Register your models here.
for model in [
    Person,
    Organization,
    OrgType,
    InteractionType,
    Interaction,
    RelationshipPersonPerson,
    RelationshipOrganizationPerson,
    PersonPersonRelationshipType,
    OrgPersonRelationshipType,
]:
    admin.site.register(
        model
    )