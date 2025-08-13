import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GMAIL_EMAIL=os.getenv('GMAIL_EMAIL')
GMAIL_APP=os.getenv('GMAIL_APP')
