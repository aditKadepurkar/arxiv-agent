import json

def main():
    topic = input("Enter the topic you are interested in: ")
    
    print("\nEXAMPLE FORMAT FOR AUTHORS: John Doe, Ben V. Joe")
    
    authors = input("Enter authors that you are interested in using the example format: ")
    
    authors_list = authors.split(", ")
    
    print(f"\nYou are interested in the topic: {topic}")
    print(f"Authors you are interested in: {authors_list}")
    
    generate_json(topic, authors_list)

def generate_json(topic, authors_list):
    data = {
        "topic": topic,
        "authors": {}
    }
    for author in authors_list:
        data["authors"][author] = author_data(author)
    
    with open("userdata.json", "w") as f:
        json.dump(data, f)
        
    print("\nData has been saved to userdata.json")

def author_data(author):
    author_data = {
        "twitter_handle": "",
        "tweets": [],
        "coauthors": [],
    }
    return author_data

if __name__ == "__main__":
    main()