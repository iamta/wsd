import pandas as pd
import pickle
import rowordnet as rwn
import matplotlib.pyplot as plt

wn = rwn.RoWordNet()

def create_word_statistics(word):
    most_likely = pd.read_csv("output\most_likely_sense.csv")
    simplified = pd.read_csv("output\simplified_lesk.csv")
    simplified_wordnet = pd.read_csv("output\simplified_lesk_wordnet.csv")
    simplified_wordnet_complete = pd.read_csv("output\simplified_lesk_wordnet_complete.csv")
    bert = pd.read_csv("output\\bert.csv")

    most_likely.loc[:, 'Algorithm'] = "Most Likely Sense"
    simplified.loc[:, 'Algorithm'] = "Simplified Lesk"
    simplified_wordnet.loc[:, 'Algorithm'] = "Simplified Lesk Wordnet"
    simplified_wordnet_complete.loc[:, 'Algorithm'] = "Simplified Lesk Wordnet Complete"
    bert.loc[:, 'Algorithm'] = "BERT"

    word_data = most_likely[most_likely['word'] == word].head(1)
    simplified = simplified[simplified['word'] == word].head(1)
    simplified_wordnet = simplified_wordnet[simplified_wordnet['word'] == word].head(1)
    simplified_wordnet_complete = simplified_wordnet_complete[simplified_wordnet_complete['word'] == word].head(1)
    bert = bert[bert['word'] == word].head(1)

    word_data = pd.concat([word_data, simplified])
    word_data = pd.concat([word_data, simplified_wordnet])
    word_data = pd.concat([word_data, simplified_wordnet_complete])
    word_data = pd.concat([word_data, bert])

    return word_data

def get_definitions_for_word(word):
    with open("dataset.pickle", "rb") as pickleFile:
        db = pickle.load(pickleFile)
        synsets = db[word][0]['synsets'].split()
        definitions = []
        for syn in synsets:
            try:
                definitions.append(wn.synset(syn).definition)
            except:
                continue
        
        correct_synset_id = db[word][0]['correct_synset_id']
        correct_definition = wn.synset(correct_synset_id).definition

    return definitions, correct_definition

def print_algorithm_statistics(alg, word_data):
    print("----Algorithm "+ alg + "----")
    alg_data = word_data[word_data["Algorithm"] == alg]

    predicted_synsets = alg_data['predicted_synsets'].to_list()[0].split()

    if (len(predicted_synsets) > 1):
        print("Synsets with maximum score")

        for syn in predicted_synsets:
                try:
                    print("* " + wn.synset(syn).definition)
                except:
                    continue

    print()
    print("Predicted definition")
    chosen_synset = alg_data['chosen_synset'].to_list()[0]
    print(wn.synset(chosen_synset).definition)
    print()

def main(word):
    print("Chosen word: " + word)
    word_data = create_word_statistics(word)
    sentence_data = word_data[word_data["Algorithm"] == "BERT"]
    sentence = sentence_data['sentence_id'].to_list()[0]
    definitions, marked_as_correct = get_definitions_for_word(word)

    print("Sentence: ")
    print(sentence)
    print()

    print("All possible definitions: ")
    for definition in definitions:
        print("* " + definition)
    print()

    print("Marked as correct: ")
    print(marked_as_correct)
    print()

    print_algorithm_statistics("Simplified Lesk", word_data)
    print_algorithm_statistics("Most Likely Sense", word_data)
    print_algorithm_statistics("Simplified Lesk Wordnet", word_data)
    print_algorithm_statistics("Simplified Lesk Wordnet Complete", word_data)
    print_algorithm_statistics("BERT", word_data)
    return


if __name__ == "__main__":
    main("familie")