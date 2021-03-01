import os
from tkinter import simpledialog
from slack import WebClient
from slack.errors import SlackApiError


class Bot:

    def __init__(self):
        self.token_path = "slack_token.txt"
        self.__set_client()

    def send_message(self, channel: str = "#general", message:str = ""):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message)
            assert response["message"]["text"] == message
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
            if os.path.exists(self.token_path):
                os.remove(self.token_path)
            self.__set_client()

    def __set_client(self):
        while True:
            try:
                with open(self.token_path, 'r') as f:
                    token = f.read()
                self.client = WebClient(token=token)
                break
            except:
                token = simpledialog.askstring("Slack APP Token", "Please provide slack app token:")
                if token == None:
                    continue
                with open(self.token_path, 'w') as f:
                    f.write(token)
