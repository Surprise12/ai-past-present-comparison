import re
import random

class CustomEliza:
    def __init__(self):
        self.rules = [
            (r'hello|hi|hey|greetings', [
                "Hello! How are you feeling today?",
                "Hi there! How can I help you?",
                "Greetings! Tell me what's on your mind."
            ]),
            (r'my name is (.+)', [
                "Nice to meet you, {0}. How does that make you feel?",
                "Hello {0}! What brings you here today?",
                "Thanks for telling me your name, {0}. How are you doing?"
            ]),
            (r'i feel (stressed|anxious|worried|nervous|overwhelmed)', [
                "Why do you think you're feeling stressed?",
                "Can you tell me more about what's causing this stress?",
                "How long have you been feeling this way?"
            ]),
            (r'i am tired|i\'m tired|feeling tired|exhausted', [
                "What's been keeping you from resting well?",
                "Do you think your schedule might be too demanding?",
                "Lack of sleep can really affect us. Tell me more."
            ]),
            (r'because (.+)', [
                "So you're saying {0}. How does that affect you?",
                "I understand. Does {0} bother you often?",
                "Tell me more about how {0} makes you feel."
            ]),
            (r'my mother|my dad|my parent|my father', [
                "Tell me more about your relationship with them.",
                "How does that make you feel about your family?",
                "Family relationships can be complex. What else?"
            ]),
            (r'sleep|rest|bed|sleeping', [
                "How many hours of sleep do you typically get?",
                "Do you think better sleep might help you feel better?",
                "What keeps you from sleeping well?"
            ]),
            (r'exam|test|study|homework|assignment', [
                "Exams can be stressful. How are you preparing?",
                "Do you feel ready for your upcoming exams?",
                "What subject is causing you the most concern?"
            ]),
            (r'.*', [
                "That's interesting. Can you tell me more?",
                "I see. How does that make you feel?",
                "Why do you say that?",
                "Please continue.",
                "What do you think about that?"
            ])
        ]
        
        self.compiled_rules = [(re.compile(pattern, re.IGNORECASE), responses) 
                               for pattern, responses in self.rules]
    
    def respond(self, user_input: str) -> str:
        user_input = user_input.strip()
        
        if not user_input:
            return "Please tell me what's on your mind."
        
        for pattern, responses in self.compiled_rules:
            match = pattern.match(user_input)
            if match:
                groups = match.groups()
                response = random.choice(responses)
                if groups:
                    response = response.format(*groups)
                return response
        
        return "That's interesting. Can you tell me more?"

eliza = CustomEliza()

def get_eliza_response(user_input: str) -> str:
    return eliza.respond(user_input)

if __name__ == "__main__":
    print("ELIZA Chatbot")
    print("Type 'quit' to stop.\n")
    
    while True:
        user = input("You: ")
        if user.lower() == "quit":
            print("ELIZA: Goodbye!")
            break
        print("ELIZA:", get_eliza_response(user))