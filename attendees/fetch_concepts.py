
from tapioca_concept_insights import ConceptInsights
from tapioca.exceptions import TapiocaException

from attendees.models import Atendee, Concept


ACCOUNT_ID = 'wikipedia'
GRAPH = 'en-latest'


cli = ConceptInsights(
    user='252f3e20-0ae7-42c3-a3ae-ee21dc216db6',
    password='5dJHn3GjNxgl')


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











