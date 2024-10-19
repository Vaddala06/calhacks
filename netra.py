import reflex as rx

# Define the state for the chatbot
class ChatState(rx.State):
    # Holds the conversation history as a list of messages
    conversation: list = []
    user_input: str = ""

    def add_message(self, sender: str, message: str):
        """Add a message to the conversation."""
        self.conversation.append(f"{sender}: {message}")
        self.user_input = ""

    def process_user_message(self):
        """Process the user message and generate a bot response."""
        # Add user message to conversation
        user_message = self.user_input
        self.add_message("You", user_message)

        # Simple bot response logic
        if "hello" in user_message.lower():
            bot_message = "Hello! How can I assist you today?"
        elif "how are you" in user_message.lower():
            bot_message = "I'm just a bot, but thanks for asking!"
        else:
            bot_message = "I'm not sure about that. Can you ask me something else?"

        # Add bot message to conversation
        self.add_message("Bot", bot_message)

# Define the main chatbot interface
def index():
    return rx.vstack(
        # Chat messages display area using rx.foreach
        rx.box(
            rx.foreach(
                ChatState.conversation,
                lambda msg: rx.text(msg)
            ),
            padding="20px",
            border="1px solid gray",
            height="300px",
            overflow_y="scroll",
            width="100%",
            max_width="600px",
        ),
        # Input field for user message
        rx.input(
            placeholder="Type your message here...",
            value=ChatState.user_input,
            on_change=lambda val: ChatState.set_user_input(val),
            width="100%",
            max_width="600px",
        ),
        # Send button
        rx.button(
            "Send",
            on_click=ChatState.process_user_message,
            margin_top="10px",
        ),
        spacing="10px",
        align_items="center",
    )

# Create the app and add the chatbot page
app = rx.App()
app.add_page(index)
# app.compile()
