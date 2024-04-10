# AI Audio Summarizer
## Welcome to Kevin's AI Audio Summarizer!
### Instructions
1. Click "Choose File" and select an audio file from your device
2. Click "Upload" and wait for the audio to upload
3. When the "Summarize Audio" button appears, click it to produce a summary of the audio
4. After the summary displays, you can scroll down to the "Q/A" section to ask questions about the audio using the textbox
5. To use another audio file, simply choose and upload another file

### Design Choices

#### APIs, Framework, etc. Used
* AssemblyAI (Speech to Text)
* OpenAI API
* LangChain
* FAISS

#### Why use AssemblyAI?
* Very easy to integrate
* 92.5% Accuracy
* 30.4s Latency on 30 min audio file
* 12.5M Hours of multilingual training data

#### How does the LLM do summarization?
* I have combined OpenAI's GPT-4 model and LangChain's load_summarize_chain
* AssemblyAI splits the transcribed text into paragraphs which I use the above features to summarize each paragraph and create one final summary of those summaries

#### How does the Q/A work?
* I have combined both Langchain's retriever and agent to create an efficient answering system to the user's questions.
* I created a tool containing the retriever and equipped the agent with this toolkit
