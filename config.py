import os

OPENAI_API_KEY = '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'
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
TMP_DIRECTORY = 'tmp'
PERSIST_DIRECTORY = 'chroma_db'
MODEL_NAME = "gpt-3.5-turbo"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
UPLOAD_NEW = "Upload new one"
ALREADY_UPLOADED = "Already Uploaded"
