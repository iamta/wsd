import pickle
import rowordnet as rwn
import stanza
import string
import requests
import csv
import sys
from copy import deepcopy


PRINT_DETAILS = True

def print_to_console(string):
    if PRINT_DETAILS == False:
        return
    else:
        sys.stdout.write(str(string) + "\n")


stopwords_link = "https://raw.githubusercontent.com/stopwords-iso/stopwords-ro/master/stopwords-ro.txt"
stopwords = requests.get(stopwords_link).text.split()

stanza.download('ro')
stz = stanza.Pipeline('ro')

wn = rwn.RoWordNet()

with open("dataset.pickle", "rb") as pickleFile:
    db = pickle.load(pickleFile)


def most_likely_sense(sentence):
    word = sentence["literal"]

    sense_count = dict()
    for i in range(len(db[word])):
        correct_sense = db[word][i]['correct_synset_id']
        if correct_sense not in sense_count:
            sense_count[correct_sense] = 1
        else:
            sense_count[correct_sense] += 1

    max_l = 0
    max_sid = []

    for sid in sense_count:
        if sense_count[sid] > max_l:
            max_l = sense_count[sid]
            max_sid = []
            max_sid.append(sid)
        elif sense_count[sid] == max_l:
            max_sid.append(sid)

    return max_sid


def simplified_lesk(sentence):
    if "synsets" not in sentence:
        synset_ids = wn.synsets(sentence['literal'])
    else:
        synset_ids = sentence['synsets'].split(' ')

    context = set(sentence["sentence"].split())

    print_to_console("Context is: ")
    print_to_console(context)

    lens = []

    for id in synset_ids:
        try:
            if id != "-1":
                print_to_console("Intersection with: ")
                print_to_console(wn.synset(id).definition.split())
                lens.append(len(context.intersection(
                    wn.synset(id).definition.split())))
                print_to_console("Intersection length: " + str(lens[-1]))
        except:
            lens.append(-1)

    max_l = max(lens)
    max_sid = []

    for i in range(len(lens)):
        if lens[i] == max_l:
            max_sid.append(synset_ids[i])

    return max_sid


def parse_and_tokenize(s):
    # print_to_console(s)
    result = list()
    doc = stz(s)
    for _, sentence in enumerate(doc.sentences):
        for token in sentence.tokens:
            for word in token.words:
                if word.upos in ["VERB", "NOUN", "ADV", "ADJ", "PROPN"]:
                    result.append(word.lemma)
    # print_to_console(result)
    return result


def split_sentence(s):
    l = []
    for w in s.split():
        w = w.lstrip(string.punctuation).rstrip(string.punctuation).lower()
        if w in stopwords:
            continue
        if len(w) == 0:
            continue
        l.append(w)
    return l


def simplified_lesk_wordnet(sentence):
    if "synsets" not in sentence:
        synset_ids = wn.synsets(sentence['literal'])
    else:
        synset_ids = sentence['synsets'].split(' ')

    context = set(split_sentence(sentence["sentence"]))

    print_to_console("Context is: ")
    print_to_console(context)

    lens = []

    for id in synset_ids:
        try:
            print_to_console("")
            print_to_console("Intersection with synset definition: ")
            print_to_console(split_sentence(wn.synset(id).definition))
            current_len = len(context.intersection(
                split_sentence(wn.synset(id).definition)))
            current_len *= current_len
            print_to_console(
                "Intersection length (squared): " + str(current_len))
            for rel in wn.outbound_relations(id):
                if rel[1] == "hypernym":
                    id_hypernym = rel[0]
                    print_to_console("Intersection with hypernym " +
                                     str(wn.synset(id_hypernym).literals) + " definition: ")
                    print_to_console(split_sentence(
                        wn.synset(id_hypernym).definition))
                    current_len += len(context.intersection(
                        split_sentence(wn.synset(id_hypernym).definition)))
                    print_to_console("Intersection length with hypernym: " + str(len(context.intersection(
                        split_sentence(wn.synset(id_hypernym).definition)))))
            print_to_console("Total intersection length: " + str(current_len))
            lens.append(current_len)
        except:
            lens.append(-1)

    max_l = max(lens)
    max_sid = []

    for i in range(len(lens)):
        if lens[i] == max_l:
            max_sid.append(synset_ids[i])

    return max_sid


combinations = []


def get_combinations(synsets, index, partial):
    if index == len(synsets):
        global combinations
        combinations.append(partial)
        return
    for i in range(len(synsets[index])):
        copy = deepcopy(partial)
        copy.append(synsets[index][i])
        get_combinations(synsets, index+1, copy)


def gloss_overlap(gloss1, gloss2):
    words1 = split_sentence(gloss1)
    words2 = split_sentence(gloss2)
    score = 0
    i = 0
    while i < len(words1):
        j = 0
        while j < len(words2):
            if words1[i] == words2[j]:
                seq = [words1[i]]
                l = 1
                i2 = i
                j2 = j
                while j2 + 1 < len(words2) and i2 + 1 < len(words1):
                    if words1[i2 + 1] == words2[j2 + 1]:
                        seq.append(words1[i2 + 1])
                        l += 1
                        i2 += 1
                        j2 += 1
                    else:
                        break
                for w in seq:
                    if w not in stopwords:
                        score += l * l
                        break
            j += 1
        i += 1
    return score


def adapted_lesk(sentence, n=2):
    word = sentence['literal']
    text_prefix = sentence['text_prefix']
    text_postfix = sentence['text_postfix']

    global combinations
    combinations = []
    context = [word]
    text_prefix = parse_and_tokenize(text_prefix)
    text_prefix.reverse()
    text_postfix = parse_and_tokenize(text_postfix)
    for i in range(max(len(text_prefix), len(text_postfix))):
        for text in [text_prefix, text_postfix]:
            if i < len(text) and len(context) < 2 * n + 1:
                # we include in the context only words from the db
                if(text[i] in db):
                    if text[i] not in stopwords:
                        context.append(text[i])
    synsets = []

    print_to_console("Context is: ")
    print_to_console(context)
    for cword in context:
        synsets_cword = db[cword][0]['synsets'].split()[:-1]
        synsets.append(synsets_cword)
        print_to_console("The word " + cword + " appears in " +
                         str(len(synsets_cword)) + " synsets")
    get_combinations(synsets, 0, [])
    max_score = 0
    results = []
    print_to_console("There are " + str(len(combinations)) +
                     " combinations possible")
    for c in combinations:
        d = []
        score = 0
        for s in c:
            d.append(wn.synset(s).definition)
        print_to_console(
            "We calculate the overlap between the definitions (each pair): ")
        print_to_console(d)
        for d1 in d:
            for d2 in d:
                if d1 != d2:
                    score += gloss_overlap(d1, d2)
        print_to_console("Final score is " + str(score))
        print_to_console("")
        if score > max_score:
            max_score = score
            results = []
            results.append(c[0])
        elif score == max_score:
            results.append(c[0])

    freq_results = dict()
    for r in results:
        if r not in freq_results:
            freq_results[r] = 1
        else:
            freq_results[r] += 1

    most_freq = []
    max_freq = 0
    for r in freq_results:
        if freq_results[r] > max_freq:
            max_freq = freq_results[r]
            most_freq = []
            most_freq.append(r)
        elif freq_results[r] == max_freq:
            most_freq.append(r)

    return most_freq


possible_rel = set()


def simplified_lesk_wordnet_complete(sentence):
    if "synsets" not in sentence:
        synset_ids = wn.synsets(sentence['literal'])
    else:
        synset_ids = sentence['synsets'].split(' ')

    context = set(split_sentence(sentence["sentence"]))

    print_to_console("Context is: ")
    print_to_console(context)

    lens = []

    for id in synset_ids:
        try:
            print_to_console("")
            print_to_console("Intersection with synset definition: ")
            print_to_console(split_sentence(wn.synset(id).definition))
            current_len = len(context.intersection(
                split_sentence(wn.synset(id).definition)))
            current_len *= current_len
            print_to_console(
                "Intersection length (squared): " + str(current_len))
            for rel in wn.outbound_relations(id):
                if rel[1] not in ["hyponym", "instance_hyponym", "substance_meronym", "member_meronym", "part_meronym"]:
                    id_hypernym = rel[0]
                    print_to_console("Intersection with " + rel[1] + " " +
                                     str(wn.synset(id_hypernym).literals) + " definition: ")
                    print_to_console(split_sentence(
                        wn.synset(id_hypernym).definition))
                    current_len += len(context.intersection(
                        split_sentence(wn.synset(id_hypernym).definition)))
                    print_to_console("Intersection length with hypernym: " + str(len(context.intersection(
                        split_sentence(wn.synset(id_hypernym).definition)))))
            print_to_console("Total intersection length: " + str(current_len))
            lens.append(current_len)
        except:
            lens.append(-1)

    max_l = max(lens)
    max_sid = []

    for i in range(len(lens)):
        if lens[i] == max_l:
            max_sid.append(synset_ids[i])

    return max_sid


last_word = None
last_definitions = None


def parsed_simplified_lesk(sentence):
    if "synsets" not in sentence:
        synset_ids = wn.synsets(sentence['literal'])
    else:
        synset_ids = sentence['synsets'].split(' ')

    context = set(parse_and_tokenize(sentence["sentence"]))
    print_to_console("Context is: ")
    print_to_console(context)

    global last_word
    global last_definitions
    if last_word == sentence['literal']:
        definitions = last_definitions
    else:
        definitions = []
        for id in synset_ids:
            try:
                definition = set(parse_and_tokenize(wn.synset(id).definition))
                definitions.append(definition)
            except:
                continue
        last_definitions = definitions
        last_word = sentence['literal']

    lens = []

    for definition in definitions:
        try:
            # print_to_console(context, definition)
            print_to_console("Intersection with: ")
            print_to_console(definition)
            lens.append(len(context.intersection(definition)))
            print_to_console("Intersection length: " +
                             str(len(context.intersection(definition))))
        except:
            lens.append(-1)

    # print_to_console(lens)
    max_l = max(lens)
    max_sid = []

    for i in range(len(lens)):
        if lens[i] == max_l:
            max_sid.append(synset_ids[i])

    return max_sid


def benchmark(f, limit=None, word_list=None):
    print_to_console("----- Testing " + f.__name__ + " -----")

    correct_total_s = 0
    correct_total_l = 0
    computed_sentences_total = 0

    filename_strict = "output/" + f.__name__ + "_strict"
    filename_loose = "output/" + f.__name__ + "_loose"
    filename_csv = "output/" + f.__name__

    if word_list is not None or limit is not None:
        filename_loose += ".partial"
        filename_strict += ".partial"
        filename_csv += ".partial"

    out_strict = open(filename_strict + ".txt", "wt", encoding="utf-8")
    csv_out = open(filename_csv + ".csv",
                   "w", encoding="utf-8", newline='')
    out_loose = open(filename_loose + ".txt", "wt", encoding="utf-8")
    header = ['word', 'sentence_id', 'correct_synset_id',
              'predicted_synsets', 'chosen_synset']
    writer = csv.writer(csv_out)
    writer.writerow(header)
    word_count = 0

    if word_list is None:
        word_list = db

    for word in word_list:
        word_sentence_nr = len(db[word])
        correct_s = 0
        correct_l = 0
        computed_sentences = 0
        for i in range(word_sentence_nr):
            correct_sid = db[word][i]['correct_synset_id']
            if correct_sid == '-1':
                continue

            computed_sentences = computed_sentences + 1
            result = f(db[word][i])
            result_str = ""
            for r in result:
                result_str += r + " "
            if len(result) == 1:
                writer.writerow(
                    [word, i, correct_sid, result_str[:-1], result[0]])
                if result[0] == correct_sid:
                    correct_s += 1
            else:
                max_freq = -1
                max_sid = result[0]
                for sid in result:
                    freq = 0
                    for k in range(len(db[word])):
                        if db[word][k]['correct_synset_id'] == sid:
                            freq += 1
                    if freq > max_freq:
                        max_freq = freq
                        max_sid = sid
                writer.writerow(
                    [word, i, correct_sid, result_str[:-1], max_sid])
                if max_sid == correct_sid:
                    correct_l += 1

        # print('Correct strict guesses for word ' + word + ": " +
        #       str(correct_s) + "/" + str(computed_sentences))
        # print('Correct loose guesses for word ' + word + ": " +
        #       str(correct_l) + "/" + str(computed_sentences))
        out_strict.write('Correct guesses for word ' + word + ": " +
                         str(correct_s) + "/" + str(computed_sentences) + "\n")
        correct_total_s += correct_s
        out_loose.write('Correct guesses for word ' + word + ": " +
                        str(correct_l) + "/" + str(computed_sentences) + "\n")
        correct_total_l += correct_l + correct_s
        computed_sentences_total += computed_sentences
        word_count += 1
        if limit and word_count == limit:
            break

    out_strict.write('Correct guesses: ' + str(correct_total_s) +
                     "/" + str(computed_sentences_total))
    out_loose.write('Correct guesses: ' + str(correct_total_l) +
                    "/" + str(computed_sentences_total))

    print('Correct strict guesses: ' + str(correct_total_s) +
                     "/" + str(computed_sentences_total))
    print('Correct loose guesses: ' + str(correct_total_l) +
                     "/" + str(computed_sentences_total))

    out_strict.close()
    out_loose.close()
    csv_out.close()


def main():
    # benchmark(simplified_lesk)
    # benchmark(parsed_simplified_lesk, limit=1)
    # benchmark(parsed_simplified_lesk, word_list=["rol"])
    # benchmark(simplified_lesk_wordnet)
    # benchmark(simplified_lesk_wordnet_complete)
    # benchmark(adapted_lesk, word_list=["măr"])
    # benchmark(most_likely_sense)

    # sentence = {
    #     "sentence": "Mănânc un măr roșu cules din pom.", "literal": "măr"}
    # result_id = parsed_simplified_lesk(sentence)
    # wn.print_synset(result_id)

    word = "bancă"
    print_to_console("Căutăm înțelesul cuvântului " + word +
                     " în propoziția: " + db[word][0]['sentence'])
    result = simplified_lesk(db[word][0])

    print_to_console("Selected definitions:")
    for id in result:
        print_to_console(wn.synset(id).definition)
    print_to_console("Definition marked as correct: ")
    print_to_console(wn.synset(db[word][0]['correct_synset_id']).definition)

    print_to_console("___________________________________")

    print_to_console("Căutăm înțelesul cuvântului " + word +
                     " în propoziția: " + db[word][0]['sentence'])
    result = parsed_simplified_lesk(db[word][0])

    print_to_console("Selected definitions: ")
    for id in result:
        print_to_console(wn.synset(id).definition)
    print_to_console("Definition marked as correct: ")
    print_to_console(wn.synset(db[word][0]['correct_synset_id']).definition)

    print_to_console("___________________________________")

    print_to_console("Căutăm înțelesul cuvântului " + word +
                     " în propoziția: " + db[word][0]['sentence'])
    result = simplified_lesk_wordnet(db[word][0])

    print_to_console("Selected definitions:")
    for id in result:
        print_to_console(wn.synset(id).definition)
    print_to_console("Definition marked as correct:")
    print_to_console(wn.synset(db[word][0]['correct_synset_id']).definition)

    print_to_console("___________________________________")

    print_to_console("Căutăm înțelesul cuvântului " + word +
                     " în propoziția: " + db[word][0]['sentence'])
    result = simplified_lesk_wordnet_complete(db[word][0])

    print_to_console("Selected definitions:")
    for id in result:
        print_to_console(wn.synset(id).definition)
    print_to_console("Definition marked as correct:")
    print_to_console(wn.synset(db[word][0]['correct_synset_id']).definition)

    # print_to_console("___________________________________")

    # print_to_console("Căutăm înțelesul cuvântului " + word +
    #                  " în propoziția: " + db[word][0]['sentence'])
    # result = adapted_lesk(db[word][0])

    # print_to_console("Selected definitions:")
    # for id in result:
    #     print_to_console(wn.synset(id).definition)
    # print_to_console("Definition marked as correct:")
    # print_to_console(wn.synset(db[word][0]['correct_synset_id']).definition)

    return


if __name__ == "__main__":
    main()
