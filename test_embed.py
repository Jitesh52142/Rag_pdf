from google import genai
import os

client = genai.Client(api_key="AIzaSyBzaaE0DVrwJkSOU11K4cEu-AeiZbfufF0")

models = client.models.list()

for m in models:
    print(m.name)