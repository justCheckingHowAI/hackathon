from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai

vertexai.init(project=PROJECT_ID, location="us-east4")



def insert_talks():
    