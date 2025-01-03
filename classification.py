import json
from typing import Union

"""

The goal of this file is to provide APIs to judge whether we have found 
something relavent to what the user is looking for


input : some text/image data like a tweet, or a pdf and the users preferences in whatever json format we setup

output : a classification (I think binary for now?)


"""



class Classifier:
    def __init__(self, user_preferences: dict):
        self.user_preferences = user_preferences

    def classify(self, data) -> bool:
        """
        This will do some classification via embeddings, semantically via LLM, or just direct author match
        
        """
        
        
        pass

def load_user_preferences(file_path: str) -> dict:
    """
    rn i just have this reading a json file with user_preferences
    """
    with open(file_path, 'r') as file:
        return json.load(file)

# Example usage
if __name__ == "__main__":
    user_preferences = load_user_preferences('user_preferences.json')
    classifier = Classifier(user_preferences)
    
    sample_text = "This is a sample tweet about machine learning."
    is_relevant = classifier.classify(sample_text)
    print(f"Is the sample text relevant? {is_relevant}")
