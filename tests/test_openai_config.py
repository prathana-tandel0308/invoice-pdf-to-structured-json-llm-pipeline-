from config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    LOCAL_LLM_MODEL
)


if not OPENAI_API_KEY:
    print("OpenAI API key not found!")

else:
    print("OpenAI API key loaded successfully!")
    print(f"OpenAI model: {OPENAI_MODEL}")
    print(f"Local model: {LOCAL_LLM_MODEL}")