from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from config import TMP_DIRECTORY, PERSIST_DIRECTORY, MODEL_NAME, EMBEDDING_MODEL_NAME

def load_docs(directory):
    loader = DirectoryLoader(directory)
    return loader.load()

def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

def initialize_models(last_update):
    documents = load_docs(TMP_DIRECTORY)
    docs = split_docs(documents)

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    vectordb.persist()

    llm = ChatOpenAI(model_name=MODEL_NAME)
    db = Chroma.from_documents(docs, embeddings)
    chain = load_qa_chain(llm, chain_type="stuff", verbose=True)

    return db, chain

def get_answer(query, db, chain):
    matching_docs_score = db.similarity_search_with_score(query)
    matching_docs = [doc for doc, score in matching_docs_score]
    answer = chain.run(input_documents=matching_docs, question=query)

    sources = [{
        "content": doc.page_content,
        "metadata": doc.metadata,
        "score": score
    } for doc, score in matching_docs_score]

    return {"answer": answer, "sources": sources}
