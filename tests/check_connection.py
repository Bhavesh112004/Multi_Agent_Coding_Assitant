from langchain_ollama import ChatOllama

# Initialize the model you pulled earlier
llm = ChatOllama(model="qwen2.5-coder:7b")

try:
    response = llm.invoke("Quick check: Are you working?")
    print("Success! Response:", response.content)
except Exception as e:
    print(f"Error: {e}. Make sure 'ollama serve' is running!")