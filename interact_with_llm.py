from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain import hub
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

QUESTION_ANSWER_MAP = {
    "Question1: Are you usually?": {
        "A 'Good Mixer with groups of people": "Extrovert",
        "Rather quiet and reserved": "Introvert"
    },
    "Question2: Among your friends, you are?": {
        "Full of news about everybody": "Extrovert",
        "One of the last to hear what is going on": "Introvert"
    },
    "Question3: In doing something that many other people do, you would rather?": {
        "Invent a way of your own": "Intuition",
        "Do it in the accepted way": "Sensing"
    },
    "Question4: Do you admire the people who are?": {
        "Normal-acting to never make themselves the center of attention": "Sensing",
        "Too original and individual to care whether they are the center of attention or not": "Intuition"
    },
    "Question5: Do you more often let?": {
        "Your heart rule your head": "Feeling",
        "Your head rule your heart": "Thinking"
    },
    "Question6: Do you usually?": {
        "Value emotion more than logic": "Feeling",
        "Value logic more than feelings": "Thinking"
    },
    "Question7: When you go somewhere for the day, you would rather": {
        "Plan what you will do and when": "Judging",
        "Just go": "Perceiving"
    },
    "Question8: When you have a special job to do, you like to": {
        "Organize it carefully before you start": "Judging",
        "Find out what is necessary as you go along": "Perceiving"
    }
}

os.environ['OPENAI_API_KEY']= os.environ.get('OPENAI_API_KEY')
class Agent():
    def __init__(self) -> None:

        # embeddings = OpenAIEmbeddings()
        # documents = TextLoader("document_0.txt").load()
        # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        # docs = text_splitter.split_documents(documents)
        vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db")
        retriever = vectorstore.as_retriever()
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        rag_prompt = hub.pull("rlm/rag-prompt")
        self.rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | rag_prompt 
            | llm 
        )

    def send_msg(self,dic):
        for k, v in dic.items():
            original = k
            question= k.split(":")[1].strip()
            ans = v

        options = list(QUESTION_ANSWER_MAP[original].items())
        optionA = options[0][0]
        optionB = options[1][0]
        desA = options[0][1]
        desB = options[1][1]

        result = self.rag_chain.invoke( "Given the question: '{}', the possible answers are: "
        "A. '{}' and B. '{}'. Choosing A indicates the person is {} "
        "while B indicates the person is {}. Based on the response: "
        "{}, "
        "determine how much this person aligns with being {} on a scale of 0-100. "
        "0-10 means 'Extremely {}', 11-20 means 'Very {}', 21-45 means '{}', "
        "55-80 means 'Moderately {}', 81-90 means 'Very {}', "
        "91-100 means 'Extremely {}'. Give a number as output, don't give any explanation!"
        "If the answer provided by this person is not related, return 50."
        .format(question, optionA, optionB, desA, desB, ans,desA, desA, desA, desA, desB, desB, desB))

        return (desA, result.content)
    def send_post(self, post):
        result = self.rag_chain.invoke(
    f"Based on the content of the post '{post}',"
    "provide a guess using the MBTI dimensions. "
    "For each dimension, assign a score from 0 to 100 to indicate the likelihood of the author displaying the first trait over the second." 
    "For example, a score of 60 for 'Extrovert-Introvert' would indicate 60% Extrovert and 40% Introvert." 
    "Along with the score, provide a brief rationale for your judgment. If the information is not enough, just try to guess, don't worry about the correctness."
    "Return the results in a structured format that includes both the scores and rationales, suitable for parsing with Python's json library.")
        return result.content

