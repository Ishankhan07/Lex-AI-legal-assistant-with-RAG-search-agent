import os
from groq import Groq

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class ReasoningModel:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "openai/gpt-oss-120b"


    def generate_answer(self, question, context):

        prompt = f"""


You are LexAI, an AI legal assistant specialized in Indian law.

Answer the user's question using only the provided legal context.

Rules:
- Do not change the meaning of legal terms.
- Do not assume information not present in the context.
- If the context is insufficient, clearly say so.
- Provide a concise and accurate explanation.
- Mention relevant sections/articles when available.

Legal Context:
{context}


User Question:
{question}


Answer:
"""


        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        return response.choices[0].message.content



if __name__ == "__main__":

    model = ReasoningModel()


    answer = model.generate_answer(
        "What is Bharatiya Nagarik Suraksha Sanhita?",
        """
        The Bharatiya Nagarik Suraksha Sanhita, 2023 is an Act
        to consolidate and amend the law relating to criminal procedure.
        """
    )


    print(answer)