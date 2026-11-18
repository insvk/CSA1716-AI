from nltk.chat.util import Chat, reflections

# Pattern-matching chatbot demonstrating NLP regex matching.
pairs = [
    [r"(?i).*\bmy name is ([A-Za-z]+).*", ["Hello %1, how can I help you today?"]],
    [r"(?i).*\bwhat is your name\?.*", ["I am an NLP chatbot created to assist you."]],
    [r"(?i).*\bhow are you\?.*", ["I am doing well, thank you! How about you?"]],
    [r"(?i).*\b(location|city|where).*", ["I am a software chatbot and do not have a physical location."]],
    [r"(?i).*\b(hi|hello|hey)\b.*", ["Hello! How can I help you?"]],
    [r"(?i).*\b(quit|exit|bye)\b.*", ["Goodbye! Have a great day."]],
]


def start_chat():
    print("Hi! I am a simple NLP Chatbot. Type 'quit' to exit.")
    chatbot = Chat(pairs, reflections)
    chatbot.converse()


if __name__ == "__main__":
    start_chat()
