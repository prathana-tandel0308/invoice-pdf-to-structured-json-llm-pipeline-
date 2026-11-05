from google import genai
from config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

print("\nAVAILABLE GEMINI MODELS")
print("=======================")

for model in client.models.list():
    supported_actions = getattr(model, "supported_actions", [])

    if "generateContent" in supported_actions:
        print(model.name)