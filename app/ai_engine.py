from transformers import pipeline

class AIEngine:
    _instance = None

    def __init__(self):
        # Using a lightweight distilbert-based toxicity model
        self.classifier = pipeline("text-classification", model="martin-ha/toxic-comment-model")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

def analyze_message(message):
    """
    Analyzes a message for cyberbullying content using a pretrained Transformers model.
    """
    engine = AIEngine.get_instance()
    result = engine.classifier(message)[0]

    label = result['label']
    score = result['score']

    # The model uses 'toxic' and 'non-toxic' labels
    is_bullying = label == 'toxic' and score > 0.5

    if is_bullying:
        classification = "Bullying"
        response = (
            f"It appears that this message contains language that could be considered harmful or toxic. "
            f"Using words that attack or threaten others can have a deeply negative impact on someone's mental health and well-being. "
            f"We encourage you to express your feelings and opinions in a more respectful and constructive manner. "
            f"Remember that behind every screen is a real person with feelings, and choosing kindness helps build a safer community for everyone. "
            f"If you are feeling overwhelmed or angry, taking a moment to breathe before responding can make a huge difference. "
            f"There are many healthy ways to resolve conflicts without resorting to hurtful language."
        )
    else:
        classification = "Not Bullying"
        response = (
            f"This message seems to be safe and does not contain obvious signs of toxicity or bullying. "
            f"Maintaining a positive and respectful tone in your communications helps foster a supportive environment for everyone involved. "
            f"Even when the content is safe, it is always a good practice to be mindful of how your words might be perceived by others. "
            f"Continuing to use clear and kind language is a great way to ensure that your messages are well-received and effective. "
            f"If you ever feel uncertain about a conversation, don't hesitate to reach out to someone you trust for a second opinion. "
            f"Keep up the great work in promoting healthy and respectful digital interactions!"
        )

    return classification, response
