import sys
import utils
import owlready2

############################# Get Args ############################################################
_, ont_path_1, ont_lang_1, ont_path_2, ont_lang_2 = sys.argv
###################################################################################################

print(f'Arguments received:',
      f'Ontology 1: {ont_path_1} ({ont_lang_1})',
      f'Ontology 2: {ont_path_2} ({ont_lang_2})',
      sep = '\n')

############################# Translation #########################################################
ont_path_1 = ont_path_1 if ont_lang_1 == 'ro' else utils.get_translated_ontology(ont_path_1)
ont_path_2 = ont_path_2 if ont_lang_2 == 'ro' else utils.get_translated_ontology(ont_path_2)
###################################################################################################

print(f'Translation completed:',
      f'Ro Ontology 1: {ont_path_1}',
      f'Ro Ontology 2: {ont_path_2}',
      sep = '\n')

############################# Get Lists of Terms ##################################################
ont_1 = owlready2.get_ontology("file://" + ont_path_1)
ont_1.load()
ont_1_terms = [cls.__name__ for cls in ont_1.classes()]

ont_2 = owlready2.get_ontology("file://" + ont_path_2)
ont_2.load()
ont_2_terms = [cls.__name__ for cls in ont_2.classes()]
###################################################################################################

print(f'Term extraction complete.')

############################# Language ############################################################
relations = utils.get_relations(ont_1_terms, ont_2_terms)
###################################################################################################

print(relations)

print(f'Term merging complete.')

############################# Conceptualization ###################################################
ont_path_result = utils.get_merged_ontology_path(ont_path_1, ont_path_2, relations)
###################################################################################################

print(f'Final merging complete. The result ontology is at:\n{ont_path_result}')
