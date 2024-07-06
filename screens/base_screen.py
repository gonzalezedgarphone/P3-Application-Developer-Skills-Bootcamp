import re
from abc import ABC, abstractmethod
from datetime import datetime


class BaseScreen(ABC):
    """Abstract class for screen interaction"""

    @abstractmethod
    def get_command(self):
        """Child classes must implement this method. It must return a Command."""
        pass

    @staticmethod
    def input_string(prompt="", default=None, empty=False):
        """
        Utility function: get a string from the screen.
        If default then the default value is used. If empty is True, a user cannot provide an empty response.
        """

        prompt = prompt + "? "

        if default:
            prompt += f"[{default}] "

        while True:
            value = input(prompt)

            if not value and default:
                value = default

            if not empty:
                return value
            if empty and value:
                return value

    def input_email(self, **kwargs):
        """Utility function to get an email address"""

        # Shortened and valid email regex
        mail_rgxp = r"(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$)"
        message = "Please provide a valid email address!"
        return self.input_regexp(mail_rgxp, message, **kwargs)

    def input_regexp(self, regexp, error_message, **kwargs):
        """Utility function to get a string matching a regular expression"""
        while True:
            value = self.input_string(**kwargs)
            if re.match(regexp, value):
                return value

            print(error_message)

    def input_chess_id(self, **kwargs):
        """Utility function to get a Chess ID string"""
        chess_rgxp = r"[A-Z]{2}[0-9]{5}"
        message = "Please provide a valid Chess ID (XXNNNNN)!"
        return self.input_regexp(chess_rgxp, message, **kwargs)

    def input_birthday(self, **kwargs):
        """Utility function to get a date string"""
        while True:
            value = self.input_string(**kwargs)
            try:
                dt = datetime.strptime(value, "%d-%m-%Y")
                if dt > datetime.now():
                    raise ValueError
                return value
            except ValueError:
                print("Please provide a valid date (dd-mm-yyyy)!")

    def run(self):
        """Main method to 'run' the screen - displays a message and gets a command"""
        message = getattr(self, "display", None)

        if message and callable(message):
            message = message()

        if message:
            print(str(message))

        print("")
        return self.get_command()
