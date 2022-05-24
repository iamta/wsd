# Romanian WordNet

Ce e WordNet-ul? [WordNet - A Lexical Database for English (princeton.edu)](https://wordnet.princeton.edu/)

 In esenta, WordNet-ul este un graf in care nodurile sunt synset-uri si legaturile dintre noduri sunt relatii intre ele.

    Synset:: Lista de cuvinte cu acelasi sens.
    Literal:: Cuvant din componenta unui synset.
    Exemplu:: Literalul 'cal' poate sa faca parte din synset-urile [cal de sah] sau [cal (animal)].

Pentru o mai buna intelegere, a se vedea [BulNet (bas.bg)](http://dcl.bas.bg/bulnet/). Se selecteaza, din dreapta sus, BulNet & RoWN si se poate testa pentru “cal” la query si search. Se pot vedea 6 synseturi, iar la click pe fiecare dintre acestia se pot vedea literalii, precum si glosa (descrierea/definitia fiecarui synset), dar si alte legaturi.

Pentru tematica curenta, nu este necesara explicarea relatiilor dintre synseturi, ci faptul ca aceste synseturi exista, prin ele putand identifica sensul unui literal in mod obiectiv.

API-ul pentru RoWordNet este in Python [aici](https://github.com/dumitrescustefan/RoWordNet), cu exemple de incarcare WordNet, cautare a unui cuvant (literal) si listare a synset-urilor gasite.

# WSD Database description

 Baza de date este reprezentata de un fisier pickle (Python) care contine o lista de dictionare. Fiecare dictionar are cheie un literal, valoarea fiind o lista cu urmatorul format:

**literal: [{propozitie, cuvant target, synseturi candidat, synsetul corect, user}, …]**

SAU

**literal: [{„user_id“: „valoare_user_id“, „literal“: „cuvant_target“, „synsets“: „synset-uri candidat“, „correct_synset_id“: „valoare_correct_synset_id“, „text_prefix“: „valoare_text_prefix“, „text“: „cuvant_de_dezambiguizat“, „text_postfix“: „valoare_text_postfix“, „sentence“: „valoare_propozitie_intreaga“} {} …]**

 Intereseaza:

    user_id : neimportant
    literal: string, cuvant in forma lematizata folosit pentru a cauta in WordNet
    synsets: string, lista cu synset-uri din WordNet (id-uri) candidate pentru acest cuvant. Mai exact, daca se cauta literal-ul in WordNet, se obtine aceasta lista de synset-uri
    correct_synset_id: synset-ul ales corect pentru o anumita propozitie
    sentence: propozitia in sine
    text_prefix: prima parte din propozitie
    text: cuvantul target (nelematizat, asa cum apare in propozitie)
    text_postfix: restul propozitiei. Daca text_prefix, text si text_postfix,  sunt concatenate, atunci va rezulta exact stringul din “sentence”.

Baza de date trebuie incarcata in memorie folosind fisierul pickle. Literal-ul este de tip obiect cu mai multe proprietati si a fost obtinut prin folosirea Stanza pentru tokenizare si lematizare propozitie. 
