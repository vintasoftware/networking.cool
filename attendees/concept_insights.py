
from decimal import Decimal

from django.conf import settings

from tapioca_concept_insights import ConceptInsights
from tapioca.exceptions import TapiocaException

from attendees.models import Attendee, Concept


ACCOUNT_ID = 'wikipedia'
GRAPH = 'en-latest'


cli = ConceptInsights(
    user=settings.CONCEPT_INSIGHTS_USER,
    password=settings.CONCEPT_INSIGHTS_PASSWORD)


def fetch_concepts(attendee):
    response = cli.annotate_text(
        account_id=ACCOUNT_ID, graph=GRAPH).post(data=attendee.description)

    annotations = response.annotations
    concepts_set = set()

    for concept in annotations:
        score = concept.score().to_decimal()
        label = concept.concept.label().data.strip()

        concept_instance, new = Concept.objects.get_or_create(
            attendee=attendee, label=label,
            defaults={'score': score})

        if concept_instance.score != score:
            concept_instance.score = score
            concept_instance.save()

        concepts_set.update([label])

        if len(concepts_set) >= 20:
            break


def fetch_attendees_concepts():
    attendees = Attendee.objects.all()
    for attendee in attendees:
        fetch_concepts(attendee)
