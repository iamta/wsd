import pandas
import pickle
import matplotlib.pyplot as plt

with open("dataset.pickle", "rb") as pickleFile:
    db = pickle.load(pickleFile)

def numberOfSensuri(word):
    number_of_correct_senses = len(db[word][0]['synsets'].split(' ')) -1
    return number_of_correct_senses

def setStrict(data,file_strict):
    data.loc[:,'Strict']=0
    with open(file_strict, "rt", encoding="utf-8") as f:
        lines_strict = f.readlines()

        disct_strict = {}
        vector_dict_strict=[]

        for line in lines_strict[:-1]:
            words=line.split(' ')
            word=words[4]
            word = word[:-1]
            accuracy_scores=words[5].split('/')
            if(int(accuracy_scores[1])==0):
                score=0
            else:
                score=int(accuracy_scores[0])/int(accuracy_scores[1])

            vector_dict_strict.append({"word": word , "accuracy": score })
            data.loc[data['word'] == word, 'Strict'] = score


def setLoose(data,file_loose):
    data.loc[:,'Loose']=0
    with open(file_loose, "rt", encoding="utf-8") as f:
        lines_loose = f.readlines()

        dict_loose = {}
        vector_dict_loose=[]

        for line in lines_loose[:-1]:
            words=line.split(' ')
            word=words[4]
            word = word[:-1]
            accuracy_scores=words[5].split('/')
            if(int(accuracy_scores[1])==0):
                score=0
            else:
                score=int(accuracy_scores[0])/int(accuracy_scores[1])

            vector_dict_loose.append({"word": word , "accuracy": score })
            data.loc[data['word'] == word, 'Loose'] = score

    
def createStat(filename,file_loose,file_strict,title_):
    data=pandas.read_csv(filename)
    data.loc[:,'Senses']=0
    

    setLoose(data,file_loose)
    
    setStrict(data,file_strict)

    for word in db:
        data.loc[data['word'] == word, 'Senses'] = numberOfSensuri(word)

    print(data)

    average_sense = data.groupby('Senses',as_index=False).mean()
    print(average_sense)

    average_sense.plot(y = ['Strict','Loose'],x = 'Senses',kind="bar",title=title_)

    plt.legend()
    plt.show()

def setAccuracy(data,txtfile):
    data.loc[:,'Acurracy']=0
    with open(txtfile, "rt", encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines[:-1]:
            words=line.split(' ')
            word=words[4]
            word = word[:-1]
            accuracy_scores=words[5].split('/')
            if(int(accuracy_scores[1])==0):
                score=0
            else:
                score=int(accuracy_scores[0])/int(accuracy_scores[1])

            data.loc[data['word'] == word, 'Accuracy'] = score

def createStatForBERT(csvfile, txtfile):
    data=pandas.read_csv(csvfile)
    data.loc[:,'Senses']=0

    setAccuracy(data, txtfile)
    
    for word in db:
        data.loc[data['word'] == word, 'Senses'] = numberOfSensuri(word)

    average_sense = data.groupby('Senses',as_index=False).mean()
    average_sense.plot(y = ['Accuracy'],x = 'Senses',kind="bar",title="BERT")

    plt.legend()
    plt.show()

def addAccuracyForAlg(alg, df, txtfile):
    with open(txtfile, "rt", encoding="utf-8") as f:
            lines = f.readlines()
            numbers = lines[-1].split()[2].split('/')
            val = int(numbers[0]) / int(numbers[1])
            df.loc[len(df.index)] = [alg, val]

def addAccuracyForBERT(df):
    bertdf = pandas.DataFrame(columns = ["Accuracy"])
    with open("output\\bert.txt", "rt", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            words=line.split(' ')
            word=words[4]
            word = word[:-1]
            accuracy_scores=words[5].split('/')
            if(int(accuracy_scores[1])==0):
                score=0
            else:
                score=int(accuracy_scores[0])/int(accuracy_scores[1])
            bertdf.loc[len(bertdf.index)] = score

    bertavg = bertdf.mean()
    avg = bertavg['Accuracy']
    df.loc[len(df.index)] = ["BERT", avg]

def createGlobalGraph():
    df = pandas.DataFrame(columns = ["Algorithm", "Accuracy"])
    addAccuracyForAlg("MFS L", df, "output\most_likely_sense_loose.txt")
    addAccuracyForAlg("MFS S", df, "output\most_likely_sense_strict.txt")
    addAccuracyForAlg("Lesk L", df, "output\simplified_lesk_loose.txt")
    addAccuracyForAlg("Lesk S", df, "output\simplified_lesk_strict.txt")
    addAccuracyForAlg("Lesk Wn L", df, "output\simplified_lesk_wordnet_loose.txt")
    addAccuracyForAlg("Lesk Wn S", df, "output\simplified_lesk_wordnet_strict.txt")
    addAccuracyForAlg("Lesk WnC L", df, "output\simplified_lesk_wordnet_complete_loose.txt")
    addAccuracyForAlg("Lesk WnC S", df, "output\simplified_lesk_wordnet_complete_strict.txt")
    addAccuracyForBERT(df)
    
    df.plot(y = 'Accuracy',x = 'Algorithm',kind="bar",title="Total Accuracy")

    plt.legend()
    plt.show()

def main():

    #createStat("output\simplified_lesk.csv","output\simplified_lesk_loose.txt","output\simplified_lesk_strict.txt","Simplified Lesk")
    #createStat("output\simplified_lesk_wordnet.csv","output\simplified_lesk_wordnet_loose.txt","output\simplified_lesk_wordnet_complete_strict.txt","Simplified Lesk WordNet")
    #createStat("output\simplified_lesk_wordnet_complete.csv","output\simplified_lesk_wordnet_complete_loose.txt","output\simplified_lesk_wordnet_complete_strict.txt","Simplified Lesk WordNet Complete")
    #createStat("output\most_likely_sense.csv","output\most_likely_sense_loose.txt","output\most_likely_sense_strict.txt","Most Likely Sense")
    
    #createStatForBERT("output\\bert.csv", "output\\bert.txt")
    createGlobalGraph()
    return


if __name__ == "__main__":
    main()

