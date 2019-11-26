from openie import StanfordOpenIE

with StanfordOpenIE() as client:
    entity_relations = client.annotate(text='Barack Obama was born in Hawaii.')
