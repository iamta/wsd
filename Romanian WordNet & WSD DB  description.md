# Romanian WordNet

Ce e WordNet-ul? [WordNet - A Lexical Database for English (princeton.edu)](https://wordnet.princeton.edu/)

 In esenta, WordNet-ul este un graf in care nodurile sunt synset-uri si legaturile dintre noduri sunt relatii intre ele.

    Synset:: Lista de cuvinte cu acelasi sens.
    Literal:: Cuvant din componenta unui synset.
    Exemplu:: Literalul 'cal' poate sa faca parte din synset-urile [cal de sah] sau [cal (animal)].

Ca sa intelegeti mai bine, click pe [BulNet (bas.bg)](http://dcl.bas.bg/bulnet/), apoi din dreapta sus selectati BulNet & RoWN, si apoi scrieti “cal” la query si dati search. Veti vedea 6 synseturi, iar la click pe fiecare veti vedea literalii + glosa (descrierea/definitia fiecarui synset) + alte legaturi.

 Pentru subiectele curente, nu avem nevoie sa mergem mai departe in a explica relatiile dintre synseturi, ci este important ca exista aceste synseturi, prin ele putand identifica sensul unui literal in mod obiectiv.

API-ul pentru RoWordNet este in Python [aici](https://github.com/dumitrescustefan/RoWordNet). Aveti exemplu de cum se incarca WordNet, cum se cauta un cuvant (literal) si cum se listeaza synset-urile gasite.

# WSD Database description

 Baza de date este reprezentata de un fisier pickle (Python) care contine o lista de dictionare. Fiecare dictionar are cheie un literal, valoarea fiind o lista cu urmatorul format:

**literal: [{propozitie, cuvant target, synseturi candidat, synsetul corect, user}, …]**

SAU

**literal: [{„user_id“: „valoare_user_id“, „literal“: „cuvant_target“, „synsets“: „synset-uri candidat“, „correct_synset_id“: „valoare_correct_synset_id“, „text_prefix“: „valoare_text_prefix“, „text“: „cuvant_de_dezambiguizat“, „text_postfix“: „valoare_text_postfix“, „sentence“: „valoare_propozitie_intreaga“} {} …]**

 Ce ne intereseaza pe noi:

    user_id : neimportant
    literal: string, cuvantul in forma lematizata, este folosit pentru a cauta in WordNet
    synsets: string, lista cu synset-uri din WordNet (id-uri) candidate pentru acest cuvant. Mai exact, daca veti cauta literal-ul in WordNet veti obtine aceasta lista de synset-uri.
    correct_synset_id: synset-ul ales corect de voi, pentru aceasta propozitie
    sentence: propozitia in sine
    text_prefix: prima parte din propozitie
    text: cuvantul target (nelematizat, asa cum apare in propozitie)
    text_postfix: restul propozitiei. Text_prefix, text si text_postfix, daca sunt concatenate, vor rezulta exact stringul din “sentence”.

Incarcati baza de date in memorie cu pickle. Literal-ul este de tip obiect, are mai multe proprietati. Literalul a fost obtinut prin folosirea Stanza pentru tokenizare si lematizare propozitie. 
