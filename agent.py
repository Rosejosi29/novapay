from pathlib import Path
import asyncio
import os
import re

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pypdf import PdfReader
from rank_bm25 import BM25Okapi

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    set_default_openai_client,
    set_tracing_disabled,
)

from agents.memory import SQLiteSession

load_dotenv()
set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

set_default_openai_client(client)

model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-chat-v3-0324",
    openai_client=client,
)


PDF_PATH = Path("resources") / "NovaPay Profile.pdf"


def load_pdf_chunks(pdf_path: Path) -> list[str]:
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    text = re.sub(r"\n+", "\n", text)

    return [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]


DOCUMENTS = load_pdf_chunks(PDF_PATH)

TOKENIZED_DOCUMENTS = [
    document.lower().split()
    for document in DOCUMENTS
]

BM25 = BM25Okapi(TOKENIZED_DOCUMENTS)


@function_tool
def search_novapay_docs(query: str) -> str:
    """
    Search NovaPay documentation for information relevant to the user's question.
    """

    tokenized_query = query.lower().split()

    scores = BM25.get_scores(tokenized_query)

    ranked = sorted(
        zip(scores, DOCUMENTS),
        reverse=True,
    )

    results = [
        document
        for score, document in ranked
        if score > 0
    ]

    if not results:
        return "No relevant information was found in the NovaPay documentation."

    return "\n\n".join(results[:3])


agent = Agent(
    name="NovaPay Assistant",
    model=model,
    tools=[search_novapay_docs],
    instructions="""
You are NovaPay's AI customer support assistant.

You have access to NovaPay's official documentation through the
search_novapay_docs tool.

Whenever a user asks anything about:

- pricing
- transfers
- wallets
- merchant services
- APIs
- support
- products
- security
- limits
- contact information

Always call the search_novapay_docs tool before answering.

Only use information returned by the tool for NovaPay-specific questions.

If the tool cannot find the answer, tell the user that the information
is unavailable in the official documentation.

Never invent NovaPay-specific information.

Be friendly, concise and professional.
""",
)

session = SQLiteSession("novapay")


async def run_agent(user_message: str) -> str:
    result = await Runner.run(
        agent,
        user_message,
        session=session,
    )

    return result.final_output


def chat(user_message: str) -> str:
    return asyncio.run(run_agent(user_message))


if __name__ == "__main__":

    print("NovaPay AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        message = input("You: ")

        if message.lower() in {"exit", "quit"}:
            break

        response = chat(message)

        print(f"\nNovaPay: {response}\n")