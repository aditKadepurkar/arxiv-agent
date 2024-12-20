import csv
import threading
import openai


def parse():
    def process_paper(paper):
        # Implement the logic to parse the paper with the LLM
        llm = openai.OpenAI.completions.create(
            model="gpt-4o",
        )
        # TODO
        
        # Add logic to check if the result matches the specified topic/authors
        # and handle the result accordingly

    with open('arxiv_feed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        threads = []
        for paper in reader:
            thread = threading.Thread(target=process_paper, args=(paper,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()