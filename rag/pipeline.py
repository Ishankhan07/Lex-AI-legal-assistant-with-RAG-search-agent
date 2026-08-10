from models.reasoning import ReasoningModel
from rag.retriever import Retriever
from utils.web_search import WebSearchAgent



class RAGPipeline:


    def __init__(self):

        print("Loading Retriever...")


        self.retriever = Retriever(
            index_path="vector_db/index.faiss",
            chunk_path="vector_db/chunks.pkl"
        )



        print("Loading Web Search Agent...")


        self.web_agent = WebSearchAgent()



        print("Loading Reasoning Model...")


        self.reasoning_model = ReasoningModel()



        print("LexAI Ready ✅")




    def ask(self, question):


        web_keywords = [

            "latest",
            "recent",
            "today",
            "news",
            "judgement",
            "judgment",
            "supreme court",
            "high court",
            "update",
            "current"

        ]



        use_web = any(

            keyword in question.lower()

            for keyword in web_keywords

        )



        context = ""



        # =========================
        # Web Search
        # =========================

        if use_web:


            print(
                "\nSearching Web using Tavily...\n"
            )


            web_results = self.web_agent.search(
                question
            )



            for item in web_results:


                context += (

                    "Title: "
                    + item.get("title", "")
                    + "\n\n"

                    + item.get("content", "")

                    + "\n\n"

                )



        # =========================
        # Legal Knowledge Base
        # =========================

        else:


            results = self.retriever.search(

                question,

                top_k=3

            )



            for result in results:


                context += (

                    result["text"]

                    + "\n\n"

                )



        # =========================
        # Final Answer
        # =========================


        answer = self.reasoning_model.generate_answer(

            question,

            context

        )



        return answer





if __name__ == "__main__":


    pipeline = RAGPipeline()



    question = input(
        "\nAsk LexAI: "
    )



    response = pipeline.ask(
        question
    )



    print(
        "\n===================="
    )

    print(
        "LexAI Answer:"
    )

    print(
        "====================\n"
    )


    print(response)