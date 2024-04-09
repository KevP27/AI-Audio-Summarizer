from dotenv import load_dotenv
from pprint import pprint
import os

from langchain_community.chat_models import ChatOpenAI
import assemblyai as aai
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders.assemblyai import TranscriptFormat

load_dotenv()

def audio_summarizer(audio_file):
    #Setting temperature to 0 to have more concrete summarizations
    #llm = ChatOpenAI(temperature=0.1, api_key=os.getenv("OPENAI_API_KEY"))
    llm = ChatOpenAI(model='gpt-4-0613',temperature=0.1, api_key=os.getenv("OPENAI_API_KEY"))

    #Getting the AssemblyAI API key
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    #Saving the entire transcribed text for later use of answering follow-up question
    entireLoader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)

    #Setting up a global document variable to use it in the answerQuestion file as well
    global entireDocument
    #Loading the entireddocument to this variable
    entireDocument = entireLoader.load()
    
    #This is using AssemblyAI's built-in splitter where I can choose between many options (TEXT, SENTENCES, PARAGRAPHS, etc.)
    splitLoader = AssemblyAIAudioTranscriptLoader(
        file_path=audio_file,
        transcript_format=TranscriptFormat.PARAGRAPHS,
    )

    #Loading the split documents into this variable
    documents = splitLoader.load()

    #Setting up the chain
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)

    #Running the chain with the documents and retrieving the final summary text
    final_summary = chain.run(documents)
    return final_summary

if __name__ == "__main__":
    print('\n***Transcribe and Summarize Audio Files ***\n')
    audio = input("\nPlease upload an audio file")
    summary = audio_summarizer(audio)
    
    print("\n")
    pprint(summary)