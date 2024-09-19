import pickle
from typing import List

def classiffier(new_data:List[str]) -> List[str]:
    """classifies one or more prompts from a list as good or bad

    Args:
        new_data (List[str]): list containing one or more prompts

    Returns:
        List[str]: returns a list with 0 if bad or 1 if good
    """
    with open("perceptron/vectorizer.pkl", 'rb') as file:
        vectorizer = pickle.load(file)

    with open("perceptron/perceptron.sav", 'rb') as file:
        perceptron = pickle.load(file)
    new_X = vectorizer.transform(new_data)
    prediction = perceptron.predict(new_X)
    return prediction

def phrase_clasiffier(new_data:List[str]) -> int:
    """separates a large prompt into smaller ones and classifies them

    Args:
        new_data (List[str]): list containing one or more prompts

    Returns:
        List[str]: returns a list containing one or more verified prompts
    """
    if len(new_data)==1:
        banned_str = 0
        new_data_separated = []
        for i in range(0,len(new_data[0])+1,70):
            new_data_separated.append(new_data[0][i:i+70])

        new_chain = ""

                
        for phrase in new_data_separated:
            classif = classiffier([phrase])
            if classif[0]==1:
                new_chain += f"\n{phrase}"
            elif classif[0]==0:
                banned_str +=1

        if banned_str > 0:
            return 0

        return 1
   
    else:
        new_chains = []
        for i in new_data:
            new_chain = phrase_clasiffier([i])
            new_chains.append(new_chain)
        return new_chains


