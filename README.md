# Word Sense Disambiguation (WSD)

## Statistici status curent WSD Database si afisare grafica

Această tema se bazează pe setul de date de [aici](https://drive.google.com/file/d/1IV_nodlm-dw-EWl1DtngkATgAldEdAGO/view). Descrierea setului de date o gasiti [aici](docs/'Romanian WordNet & WSD DB description.md').

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
