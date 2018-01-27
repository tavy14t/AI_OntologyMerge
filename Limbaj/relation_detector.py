#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
# import unicodedata


def get_propozitii(text):
    text = text.decode('UTF-8')
    list_of_prop = re.split(";|\\.|\\!|\\?|\\n", text)
    return list_of_prop
# -------------------------------------------------


def get_good_prop(propozitii, termeni_1, termeni_2):
    good_propozitions = []
    for prop in propozitii:
        for term1 in termeni_1:
            for term2 in termeni_2:
                if term1 and term2 in prop:
                    good_propozitions.append(prop)
    good_propozitions = set(good_propozitions)
    return list(good_propozitions)


# prop=get_propozitii("Fluxul sanguin cerebral este
# asigurat prin cele două artere carotide interne şi
# de cele două artere vertebrale care se unesc în
# trunchiul vertebrobazilar. Ramificaţiile intracraniene
# ale acestor artere sunt de tip terminal ceea ce conferă
# o gravitate crescută ocluziilor vasculare cerebrale.
# În plus celula nervoasă are o sensibilitate deosebită la hipoxie
# (moarte celulară în 3-5 minute de la oprirea circulaţiei).
# Hipoperfuzia este de asemeni urmată de consecinţe.")
# print(get_good_prop(prop, ["intracraniene", "sanguin cerebral"],
#                     ["artere", "trunchi", "vasculare"]))
# --------------------------------------------------


def include_relation(term1, term2, prop):
    filter_1 = ["include", " are ", "detine ", "cuprinde ", "înglobează ",
                "definesc ", "defineste ", "includ ", "comasează ", "acoperă "]
    try:
        indx_1 = re.search(term1, prop).span()[1]
        prop = prop[indx_1:]
    except Exception:
        return []
    for fi_1 in filter_1:
        try:

            index_fi = re.search(fi_1, prop).span()[1]
            index_fi -= 1
            aux = prop[index_fi:]
            if re.search(term2, aux):
                return [(term1, "includes", term2)]
        except Exception:
            pass
    return []


def part_of_relation(term1, term2, prop):
    filter_1 = ["este ", "numește", "descrie", "sunt", "descriu", "numesc",
                "inclus", " incluse ", "aparține",
                "face parte", "aparțin", "fac parte"]
    filter_2 = ["o ", "un ", "din ", "în"]
    try:
        indx_1 = re.search(term1, prop).span()[1]
        prop = prop[indx_1:]
    except Exception:
        return []
    for fi_1 in filter_1:
        try:

            index_fi = re.search(fi_1, prop).span()[1]
            index_fi -= 1
            aux = prop[index_fi:]
            for fi_2 in filter_2:
                if re.search(fi_2 + term2, aux) or \
                        re.search(term2 + fi_2, aux):
                    return [(term1, "is_included", term2)]
        except Exception:
            pass
    return []


def get_relations(li_term_1, li_term_2, text):
    propozitii = get_propozitii(text)
    good_texts = get_good_prop(propozitii, li_term_1, li_term_2)
    relations = []
    for prop in good_texts:
        for t1 in li_term_1:
            for t2 in li_term_2:
                if t1 and t2 in prop:
                    relations += part_of_relation(t1, t2, prop)
                    relations += include_relation(t1, t2, prop)
    return relations


# print(get_relations(["Caine", "Pisica", "Mixer", "Vietuitoare"],
#                     ["Electric", "Animal", "vasculare"],
#                     "Pasarea este un Animal.O vietate Moarta este Inghetata."
#                     "Regnul Animal include specii precum Pisica si Canine."
#                     "Mixer este un Electric.Caine este un Animal."
#                     "Se zice ca Pisica face parte din Animal."
#                     "Clasa Vietuitoarelor include Animal."))
