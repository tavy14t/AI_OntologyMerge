from .Relation_extractor import extract_relations
from .SinonimList import get_sinonim_list
from .lang_module import get_synonymus


def relations(l1, l2):
    s = extract_relations(
        l1, l2,
        "C:\\Users\\George\\Documents\\GitHub\\AI_OntologyMerge\\Limbaj")
    s = s + get_sinonim_list(l1, l2)
    s = s + get_synonymus(l1, l2)

    return (list(set(s)))


if __name__ == '__main__':
    l1 = ["Caine", "prieten", "Pisica", "briceag",
          "Mixer", "Vietuitoare", "fericit"]
    l2 = ["Electric", "norocit", "Animal", "amic", "vasculare", "brisca"]

    print(relations(l1, l2))
