import os
from dotenv import load_dotenv
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

load_dotenv()

print("Current folder:", os.getcwd())
class WebSearchAgent:


    def __init__(self):

        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )


    def search(self, query):

        response = self.client.search(
            query=query,
            max_results=3
        )


        results = []


        for item in response["results"]:

            results.append(
                {
                    "title": item["title"],
                    "content": item["content"],
                    "url": item["url"]
                }
            )


        return results



if __name__ == "__main__":


    agent = WebSearchAgent()


    query = "latest Indian legal updates"


    results = agent.search(query)


    for i, result in enumerate(results):

        print("\n================")
        print("Result:", i+1)

        print("Title:")
        print(result["title"])

        print("\nContent:")
        print(result["content"][:500])

        print("\nURL:")
        print(result["url"])