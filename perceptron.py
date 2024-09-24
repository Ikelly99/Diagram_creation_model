import pickle
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def classiffier(new_data: List[str]) -> List[str]:
    """Classifies one or more prompts from a list as good or bad

    Args:
        new_data (List[str]): list containing one or more prompts

    Returns:
        List[str]: returns a list with 0 if bad or 1 if good
    """
    logging.info("Loading vectorizer and perceptron model.")
    with open("perceptron/vectorizer.pkl", 'rb') as file:
        vectorizer = pickle.load(file)
        logging.info("Vectorizer loaded.")

    with open("perceptron/perceptron.sav", 'rb') as file:
        perceptron = pickle.load(file)
        logging.info("Perceptron model loaded.")

    new_X = vectorizer.transform(new_data)
    logging.info("Data transformed using vectorizer.")

    prediction = perceptron.predict(new_X)
    logging.info(f"Prediction made: {prediction}")

    return prediction

def phrase_clasiffier(new_data: List[str]) -> int:
    """Separates a large prompt into smaller ones and classifies them

    Args:
        new_data (List[str]): list containing one or more prompts

    Returns:
        List[str]: returns a list containing one or more verified prompts
    """
    logging.info("Starting phrase classification.")
    if len(new_data) == 1:
        banned_str = 0
        new_data_separated = []
        for i in range(0, len(new_data[0]) + 1, 70):
            new_data_separated.append(new_data[0][i:i + 70])
        logging.info(f"Data separated into chunks: {new_data_separated}")

        new_chain = ""

        for phrase in new_data_separated:
            classif = classiffier([phrase])
            if classif[0] == 1:
                new_chain += f"\n{phrase}"
            elif classif[0] == 0:
                banned_str += 1
            logging.info(f"Phrase classified: {phrase} - {'Good' if classif[0] == 1 else 'Bad'}")

        if banned_str > 0:
            logging.warning("One or more phrases classified as bad.")
            return 0

        logging.info("All phrases classified as good.")
        return 1

    else:
        new_chains = []
        for i in new_data:
            new_chain = phrase_clasiffier([i])
            new_chains.append(new_chain)
        logging.info(f"Multiple data chains classified: {new_chains}")
        return new_chains
