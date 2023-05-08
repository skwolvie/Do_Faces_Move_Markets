import spacy
from spacy import displacy

nlp= spacy.load('en_core_web_lg')

def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text, '-', ent.label_)

doc1= nlp("ServiceNow CEO: Strategic Necessities | Mad Money | CNBC")

show_ents(doc1)
displacy.serve(doc1, style='ent')
