
from django.conf import settings

from tapioca_concept_insights import ConceptInsights
from tapioca.exceptions import TapiocaException

from attendees.models import Atendee, Concept


ACCOUNT_ID = 'wikipedia'
GRAPH = 'en-latest'


cli = ConceptInsights(
    user=settings.CONCEPT_INSIGHTS_USER,
    password=settings.CONCEPT_INSIGHTS_PASSWORD)


def fetch_concepts(attendee):
    response = cli.annotate_text(
        account_id=ACCOUNT_ID, graph=GRAPH).post(data=attendee.description)

    for concept in response.annotations:
        score = concept.score().to_decimal()
        concept_instance, _ = Concept.objects.get_or_create(
            atendee=attendee, label=concept.concept.label().data,
            defaults={'score': score})

        if concept_instance.score != score:
            concept_instance.score = score
            concept_instance.save()


def fetch_attendees_concepts():
    attendees = Atendee.objects.all()
    for attendee in attendees:
        fetch_concepts(attendee)
