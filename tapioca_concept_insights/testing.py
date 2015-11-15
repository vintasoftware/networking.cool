
from tapioca_concept_insights import ConceptInsights
from tapioca.exceptions import TapiocaException


ACCOUNT_ID = 'wikipedia'
GRAPH = 'en-latest'


cli = ConceptInsights(user='252f3e20-0ae7-42c3-a3ae-ee21dc216db6', password='5dJHn3GjNxgl')


data = """Guy Kawasaki is the chief evangelist of Canva, an online graphic design tool. Formerly, he was an advisor to the Motorola business unit of Google and chief evangelist of Apple. He is also the author of APE, What the Plus!, Enchantment, and nine other books. Kawasaki has a BA from Stanford University and an MBA from UCLA as well as an honorary doctorate from Babson College.

http://www.guykawasaki.com/enchantment/pictures/

Specialties: innovation, entrepreneurship, marketing, and social media."""


try:
	response = cli.annotate_text(account_id=ACCOUNT_ID, graph=GRAPH).post(data=data)
except TapiocaException as e:
	print e.client().data


print response


