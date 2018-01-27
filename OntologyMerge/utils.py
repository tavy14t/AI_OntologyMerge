import os
import typing
import Translation
import Language
import Conceptualization


def get_translated_ontology(engpath: str) -> str:
        """ Wrapper function for the main translation function. Main purpose is to add a return value.

        Takes the path to an English ontology and returns the path to the translated Romanian ontology.
        The Romanian ontology will be deposited in the same folder as the original ontology but will have '_ro'
        appended at the end of its name('ont_1.owl' will become 'ont_1_ro.owl').

        Args:
                engpath (str):  The path to the ontology to be translated.

        Return:
                str:            The path to the translated ontology.
        """
        ropath = f'{os.path.splitext(engpath)[0]}_ro{os.path.splitext(engpath)[1]}'
        engpath = f'file://{engpath}'
        Translation.Translate(engpath, ropath)
        return ropath


def get_relations(l1: typing.List[str], l2: typing.List[str]) -> typing.List[str]:
        """ Wrapper for the main Language module function. Introduces type safety and style consistency.

        Args:
                l1 (typing.List[str]):  The first list to be merged.
                l2 (typing.List[str]):  The second list to be merged.

        Returns:
                typing.List[str]:       The merged list.
        """
        return Language.relations(l1, l2)


def get_merged_ontology_path(ont_path_1: str, ont_path_2: str, relations: typing.List[str]) -> str:
        """ Wrapper for the main Conceptualization module function. Introduces type safety and adds a return value.

        The resulting ontology will be created in the same folder as the first notology and will have the name of the
        first ontology concatenated with the name of the second ontology with a '_' character.
        ont_1.owl + ont_2.owl = ont_1_ont_2.owl

        Args:
                ont_path_1 (str):               The absolute or relative path to the first .owl ontology.
                ont_path_2 (str):               The absolute or relative path to the second .owl ontology.
                relations (typing.List[str]):   The list of relations from the Language module.

        Returns:
                str:                            The path to the resulting ontology.
        """
        ont_path_res = rf'{os.path.splitext(ont_path_1)[0]}_{os.path.split(ont_path_2)[1]}'
        Conceptualization.mergeOntologies(
            ont_path_1, ont_path_2, relations, ont_path_res)
        return ont_path_res
