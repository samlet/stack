"""
$ pytest -s -v test_negspacy.py
"""
import pytest
import spacy
from negspacy.negation import Negex
from spacy.pipeline import EntityRuler

def build_med_docs():
    docs = list()
    docs.append(
        (
            "Patient denies cardiovascular disease but has headaches. No history of smoking. Alcoholism unlikely. Smoking not ruled out.",
            [
                ("Patient denies", False),
                ("cardiovascular disease", True),
                ("headaches", False),
                ("No history", True),
                ("smoking", True),
                ("Alcoholism", True),
                ("Smoking", False),
            ],
        )
    )
    docs.append(
        (
            "No history of headaches, prbc, smoking, acid reflux, or GERD.",
            [
                ("No history", True),
                ("headaches", True),
                ("prbc", True),
                ("smoking", True),
                ("acid reflux", True),
                ("GERD", True),
            ],
        )
    )

    docs.append(
        (
            "Alcoholism was not the cause of liver disease.",
            [("Alcoholism", True), ("cause", False), ("liver disease", False)],
        )
    )

    docs.append(
        (
            "There was no headache for this patient.",
            [("no headache", True), ("patient", True)],
        )
    )
    return docs

def test_umls():
    nlp = spacy.load("en_core_sci_sm")
    negex = Negex(
        nlp, language="en_clinical", ent_types=["ENTITY"], chunk_prefix=["no"]
    )
    nlp.add_pipe(negex, last=True)
    docs = build_med_docs()
    for d in docs:
        doc = nlp(d[0])
        for i, e in enumerate(doc.ents):
            print(e.text, e._.negex)
            assert (e.text, e._.negex) == d[1][i]


def test_umls2():
    nlp = spacy.load("en_core_sci_sm")
    negex = Negex(
        nlp, language="en_clinical_sensitive", ent_types=["ENTITY"], chunk_prefix=["no"]
    )
    nlp.add_pipe(negex, last=True)
    docs = build_med_docs()
    for d in docs:
        doc = nlp(d[0])
        for i, e in enumerate(doc.ents):
            print(e.text, e._.negex)
            assert (e.text, e._.negex) == d[1][i]

