from ninja import Router

from network.models import (
    Organization,
    Person,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
)

router = Router(tags=["network-graph"])


@router.get("/graph/")
def graph_data(request):
    people = Person.objects.order_by("last_name", "first_name")
    organizations = Organization.objects.select_related("org_type").order_by("name")
    person_person = RelationshipPersonPerson.objects.select_related("person_1", "person_2")
    organization_person = RelationshipOrganizationPerson.objects.select_related("organization", "person")

    nodes = []
    for person in people:
        label = f"{person.last_name}, {person.first_name}"
        nodes.append(
            {
                "data": {
                    "id": f"person-{person.id}",
                    "label": label.strip(),
                    "type": "person",
                    "details": {
                        "name": label.strip(),
                        "notes": person.notes,
                    },
                }
            }
        )

    for organization in organizations:
        nodes.append(
            {
                "data": {
                    "id": f"organization-{organization.id}",
                    "label": organization.name,
                    "type": "organization",
                    "details": {
                        "name": organization.name,
                        "type": str(organization.org_type),
                        "notes": organization.notes,
                    },
                }
            }
        )

    edges = []
    for relationship in person_person:
        edges.append(
            {
                "data": {
                    "id": f"person-person-{relationship.id}",
                    "source": f"person-{relationship.person_1_id}",
                    "target": f"person-{relationship.person_2_id}",
                    "type": "person-person",
                    "notes": relationship.notes,
                }
            }
        )

    for relationship in organization_person:
        edges.append(
            {
                "data": {
                    "id": f"organization-person-{relationship.id}",
                    "source": f"organization-{relationship.organization_id}",
                    "target": f"person-{relationship.person_id}",
                    "type": "organization-person",
                    "notes": relationship.notes,
                }
            }
        )

    return {"nodes": nodes, "edges": edges}
