import nltk
from nltk.chat.util import Chat, reflections

# Basic pattern-matching chatbot using NLP techniques (Regex/NLTK)
pairs = [
    [r"my name is (.*)", ["Hello %1, how can I help you today?",]],
    [r"what is your name?", ["I am an NLP chatbot created to assist you.",]],
    [r"how are you?", ["I'm doing well, thank you! How about you?",]],
    [r"(.*) (location|city) ?", ['I am based in the cloud.']],
    [r"quit", ["Bye! Have a great day ahead!"]],
]

def start_chat():
    print("Hi! I am a simple NLP Chatbot. Type 'quit' to exit.")
    chatbot = Chat(pairs, reflections)
    chatbot.converse()

if __name__ == "__main__":
    start_chat()
