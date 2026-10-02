import os
import truststore
from crewai import LLM
from dotenv import load_dotenv

# The corporate proxy (Zscaler) re-signs outbound TLS, and its root CA lives in
# the Windows certificate store rather than in certifi's bundle. Without this,
# every OpenAI request fails the handshake and surfaces as "Connection error".
truststore.inject_into_ssl()

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

def get_llm():
    return LLM(
        model = "openai/gpt-4o-mini",
        api_key = api_key
    )
