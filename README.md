# Word Sense Disambiguation (WSD)

Setul de date se gaseste [aici](https://drive.google.com/file/d/1IV_nodlm-dw-EWl1DtngkATgAldEdAGO/view). Descrierea setului de date o gasiti [aici](https://github.com/iamta/wsd/blob/main/Romanian%20WordNet%20%26%20WSD%20DB%20%20description.md).

## Statistici status curent WSD Database si afisare grafica

**Scop:** Obtinerea de date despre ce s-a facut pana in acest moment + afisarea lor intr-un format grafic

Input: baza de date (fisierul pickle)

Output: pandas dataframes (daca nu se doreste implementarea interfetei grafice), sau interfata grafica cu statusul

Se cere:

    A. Numarul mediu de propozitii per literal
    B. Numarul mediu de synset-uri candidat (fara synsetul „-1“) per literal
    C. Pentru fiecare literal avem n propozitii, iar acel literal are s synseturi. Prin urmare se cere calculul distributiei la nivel de literal pentru synset-urile posibile. Mai concret, se cere scoaterea unei statistici finale care sa cuprinda listati lieralii si pentru fiecare dintre acestia sa fie calculate metricile: media, varianta, deviatia standard, skewness (indicele/coeficient de asimetrie), numarul de synset-uri cu zero propozitii si suma totala de propozitii per literal.

De exemplu, daca avem 10 propozitii, si presupunem 3 synseturi posibile (ignoram tot timpul synsetul „-1“) numite 1, 2 si, respectiv, 3, atunci putem avea: 7 propozitii cu synsetul corect 1, 3 pentru synsetul 2, si nicio propozitie pentru synsetul 3, deci distributia ar fi 7-3-0. Pentru acest sir de valori putem calcula: media, varianta, deviatia standard, skewness (indicele/coeficient de asimetrie). Adaugam in afara de cele 4 valori pt fiecare literal si numarul de synset-uri cu zero propozitii (in exemplul de aici: 1 synset nu are nicio propozitie cu synsetul corect ales 3), si suma totala de propozitii per literal din exemplu, aceasta fiind 10 (aceasta ultima masura trebuie calculata oricum pentru rezovarea pct a).

    D. Privind invers problema, se cere lista tuturor synseturilor atinse, si numarul de propozitii pentru fiecare.

De exemplu, un synset are 3 literali. Lista tuturor synseturilor se va prelua din RoWordNet, (Data + API for Python) (github.com) Se poate intampla sa avem in baza de date 0, 1, 2 sau 3 literali existenti care sa aiba un numar de propozitii. Concret, se va calcula pentru fiecare synset (substantiv) din RoWordNet cati dintre literali sunt acoperiti in baza noastra de date cu specificarea clara a acestora sub forma unui fisier usor de urmarit. Deci se va scoate lista cu synseturi si pentru fiecare literal din fiecare synset (extras din RoWordNet) se va returna numarul de propozitii acoperite de catre fiecare literal. Un urmator rezultat cerut aici este suma de propozitii pt toti literalii fiecarui synset.

    E.Lista cu numar de propozitii realizat de catre fiecare user.

Concluzie: Din toate aceste date va rezulta acoperirea bazei de date pe care s-a lucrat (exp. cate dintre synseturi sunt acoperite)


## Script export din baza de date in format antrenare/validare/testare json

**Scop:** La exportul din baza de date in format json, se cere (i) obtinerea unei distributii similare intre exemplele din multimile de antrenare, validare si testare și (ii) generarea de statistici.

**Input:** Fisierul pickle.

**Output:** 3 fisiere json in acelasi format ca cel din baza de date pickle + metrica propusa de voi care sa demonstreze ca distributia intre split-uri este similara. Vezi exemplul de metrica de mai jos.

Multimea de literali va fi impartita intr-un procent de x% antrenare, y% validare si z% testare, unde x + y + z = 1.

Similar propozitiile vor fi impartite tot in acelasi format x% antrenare, y% validare si z% testare, unde x + y + z = 1.

**Exemplu:** presupunem existenta unui literal cu 20 de propozitii si 5 synseturi, cu urmatoarea distributie: 10, 4, 6, 0, 0. Interpretare: 10 propozitii pt synset-ul 1, 4 pt synsetul 2, 6 pentru synsetul 3 etc. Daca x = 0.8 (adica 80%), y si z = 0.1 (adica 10% fiecare), sa avem in submultimea de date destinate antrenarii:

    8 propozitii din cele 10 (80%) pt synsetul 1,
    2 propozitii din 4 pt synsetul 2,
    4 propozitii din 6 pt synsetul 3,
    0 si 0 pt synseturile 4 si 5.

Interpretare distributie antrenare/validare/testare: pt xyz = 0.8 0.1 0.1 vom avea

|Synsets|#1|#2|#3|#4|#5|
|---|---|---|---|---|---|
|Literalul initial are|10|4|6|0|0|
|Antrenare va avea|8|2|4|0|0|
|Validalidarea va avea|1|1|1|0|0|
|Testarea va avea|1|1|1|0|0|

**Explicatie:** se muta x = 80% din propozitii in antrenare pt synseul 1, y = 10% si z = 10% in valid si test. INSA, la synsetul 2 avem 0.1*4 propozitii < 1 propozitie. Deci, va trebui sa mutam o propozitie intreaga cu prioritate pentru datele de test, inca (minim) una pentru datele de validare (tot 0.1 are si valid) si ce ramane se muta la setul de antrenare. Atentie! Se observa ca setul de date de validare si cel de test au prioritate la calcularea procentuala a numarului de propozitii corespunzator fiecarui synset in parte: TESTARE > VALIDARE > ANTRENARE. De aceea, pt synsetul 3 am ales o propozitie pentru testare si una pentru validare, iar restul in multimea de antrenare.

**Hint:** Poti calcula pentru test parte_intreaga_functie_ceil(z * <cate_propozitii_are_synsetul>), astfel incat valorile mai mici decat 1 sa devina 1.

Generare statistici:
- literali din datele de test si validare care nu apar in propozitii in setul de antrenare, dacă este cazul
- explorarea datelor din mulțimile generate și elaborarea de anlize personalizate fiecărei echipe



*Exemplu de metrica simpla*

Am in total N literali ai caror propozitii trebuie sa le impart in 3 parti (train/dev/test).

Daca pot gasi o metrica buna care sa imi spuna daca un literal e bine balansat, atunci pot face media intre toti literalii sa obtin o metrica la nivel de dataset, adica suma metrica literal / N. Deci subproblema e acum sa obtin o metrica la nivel de literal.

Continuam. Un literal are M propozitii valide (ignoram TOATE propozitiile are au synset_correct = -1, inseamna ca propozitia respectiva este invalida, nici nu o luam in calcul, nu trebuie sa apara pe nicaieri), unde M este intre 0 si oricat. Daca M = 0 (ex un literal are 10 propozitii invalide, ignoram literalul cu totul).

Acum fiecare propozitie are un synset corect din cele S synseturi posibile pentru acest literal.

Se pune problema sa distribuim cele M propozitii in 3 parti (a.i. sa avem acelasi raport intre M si S pentru fiecare parte).

Alegeti voi cum doriti sa le distribuiti, sa zicem ca aveam M = 10 propozitii, cu S = 3 synseturi posibile, cu impartirea urmatoare:

    propozitiile 1-6 au sysnetul corect = S1
    7-9 cu synsetul corect = S2
    propozitia 10 cu synsetul corect S3

si, impartite 80% train, 10% dev, 10% train, ati obtinut:

    test: propozitia 1, 7 si 10 (a.i. in test aveti synseturile corecte S1 S2 si S3)
    dev: propozitia 2 si 8 (aici aveti synseturile S1 si S2, nu mai sunt propozitii pt S3 ca le-ati pus deja in test care are prioritate mai mare)
    train: restul de propozitii 3,4,5,6 (cu S1) si 9 (cu S2)

O metrica simpla ar verifica sa existe 3 din 3 synseturi (aici S = 3 in exemplu) in train, test si dev. Adica, daca in test, am 3/3 = 1.0, in dev am 2/3 = 0.66, in train am 2/3 synseturi corecte prezente = tot 0.66. Deci per total, metrica pentru acest literal este ( 1.0 + 0.66 + 0.66 )/ 3
