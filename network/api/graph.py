from ninja import Router

from network.models import (
    Organization,
    Person,
    RelationshipOrganizationOrganization,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
)

router = Router(tags=["network-graph"])


@router.get("/graph/")
def graph_data(request):
    people = Person.objects.order_by("last_name", "first_name")
    organizations = Organization.objects.select_related("org_type").order_by("name")
    person_person = RelationshipPersonPerson.objects.select_related("person_1", "person_2", "relationship_type")
    organization_person = RelationshipOrganizationPerson.objects.select_related("organization", "person", "relationship_type")

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
                    "relationship_type_id": relationship.relationship_type_id,
                    "relationship_type_name": relationship.relationship_type.name if relationship.relationship_type else None,
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
                    "relationship_type_id": relationship.relationship_type_id,
                    "relationship_type_name": relationship.relationship_type.name if relationship.relationship_type else None,
                }
            }
        )

    org_org = RelationshipOrganizationOrganization.objects.select_related("org_1", "org_2", "relationship_type")

    for relationship in org_org:
        edges.append(
            {
                "data": {
                    "id": f"organization-organization-{relationship.id}",
                    "source": f"organization-{relationship.org_1_id}",
                    "target": f"organization-{relationship.org_2_id}",
                    "type": "organization-organization",
                    "notes": relationship.notes,
                    "relationship_type_id": relationship.relationship_type_id,
                    "relationship_type_name": relationship.relationship_type.name if relationship.relationship_type else None,
                }
            }
        )

    return {"nodes": nodes, "edges": edges}
