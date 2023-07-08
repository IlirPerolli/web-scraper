import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


class OpenAiModel:
    system_message = None
    prompt = ""
    type = ""

    def __init__(self, type, prompt):
        self.type = type
        self.prompt = prompt

        self.set_types()

    def set_types(self):
        if self.type == 'deadline':
            self.system_message = "By the text provided, you need to get the deadline of the application. I need an " \
                                  "answer provided by you specifying only the date, not followed by a description. " \
                                  "ONLY THE DATE in format: %d/%m/%Y."

    def get_response(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": self.prompt}
            ]
        )
        return completion.choices[0].message.content
