import openai

openai.api_key = "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"

try:
    response = openai.Model.list()
    print("API Key is working:", response)
except Exception as e:
    print("Error:", e)
