from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
import os
import summarizer


def answerQ(question):

  #Getting the embedding engine prepared
  embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


  #Setting up the text splitter
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

  # Splitting documents into texts
  texts = text_splitter.split_documents(summarizer.entireDocument)

  # Embedding the texts
  db = FAISS.from_documents(texts, embeddings)

  #Setting the argument (input) to querty
  query = question

  #Setting up the retriever for the database
  retriever = db.as_retriever()

  #Creating a tool for the agent, specifically for retrieval purposes
  tool = create_retriever_tool(
      retriever,
      "Answering_question",
      "Finds and returns the answer to the user input question from the documents",
  )

  #Creating a toolkit with the tool
  tools = [tool]

  #Using a pre-defined prompt template to feed the agent 
  prompt = hub.pull("hwchase17/openai-tools-agent")
  prompt.messages

  #Setting up the llm to use
  llm = ChatOpenAI(temperature=0)

  #Creating the agent and giving it the llm, toolkit, and prompt
  agent = create_openai_tools_agent(llm, tools, prompt)

  #Creating an agent executor to call the agent and execute its actions with an input
  agent_executor = AgentExecutor(agent=agent, tools=tools)

  #Saving the result of the agent's findings given a query
  result = agent_executor.invoke({"input": query})

  #Returning the output of the agent's findings
  return result["output"]