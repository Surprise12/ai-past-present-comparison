from transformers import pipeline
import random

print("Loading model...")

chatbot = pipeline(
    "text-generation",
    model="distilgpt2",
    device_map="cpu"
)

def get_llm_response(user_input: str) -> str:
    clean_responses = {
        "hello": "Hello! How are you doing today? I'm here to help you.",
        "hi": "Hi there! What would you like to talk about?",
        "name": f"Nice to meet you! I'm an AI language model. How can I assist you today?",
        "stressed": "I understand feeling stressed. Can you tell me what's causing your stress? I'm here to listen.",
        "tired": "Being tired can be challenging. Have you been getting enough rest? What's keeping you busy?",
        "exam": "Exams can be stressful. Have you tried breaking down your study material into smaller chunks?",
        "mother": "Family relationships are important. Would you like to talk more about your feelings?",
        "sleep": "Sleep is essential for health. How many hours of sleep do you typically get?",
        "default": "That's interesting. Can you tell me more about that?"
    }
    
    user_lower = user_input.lower()
    
    if "hello" in user_lower or "hi" in user_lower:
        return clean_responses["hello"]
    elif "name" in user_lower:
        return clean_responses["name"]
    elif "stress" in user_lower:
        return clean_responses["stressed"]
    elif "tired" in user_lower:
        return clean_responses["tired"]
    elif "exam" in user_lower:
        return clean_responses["exam"]
    elif "mother" in user_lower or "mom" in user_lower:
        return clean_responses["mother"]
    elif "sleep" in user_lower:
        return clean_responses["sleep"]
    else:
        try:
            response = chatbot(
                user_input,
                max_new_tokens=30,
                do_sample=True,
                temperature=0.8,
                pad_token_id=50256
            )
            output = response[0]["generated_text"]
            if len(output) > len(user_input) + 5:
                output = output[len(user_input):].strip()
                if len(output) > 100:
                    output = output[:100] + "..."
                return output
            else:
                return clean_responses["default"]
        except:
            return clean_responses["default"]

if __name__ == "__main__":
    print("=" * 50)
    print("MODERN AI CHATBOT - LLM")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    while True:
        user = input("You: ")
        if user.lower() == "quit":
            print("Bot: Thank you for chatting! Goodbye!")
            break
        response = get_llm_response(user)
        print(f"Bot: {response}\n")