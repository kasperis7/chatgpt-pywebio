from revChatGPT.Official import Chatbot
from pywebio import start_server
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env
import os

api_key = "your_api_key_here"

def main():

    chatbot = Chatbot(api_key)

    @use_scope("out")
    def chatbot_reset():
        chatbot.reset()
        clear()

    @use_scope("out")
    def chatbot_rollback():
        try:
            chatbot.rollback(1)
            put_table([["⬇️This message is rollbacked."]], position=0)
        except IndexError as _:
            toast("Chat history is empty.")

    @use_scope("out")
    def show_response():
        prompt = pin.prompt
        pin.prompt = ""
        if prompt.startswith("!"):
            if chatbot_commands(prompt):
                return
        with put_loading(position=0):        
            response = chatbot.ask(prompt)
        put_table([
            ['Q:', prompt],
            ['A:', put_markdown(response["choices"][0]["text"])]
        ], position=0)
    
    set_env(title="ChatGPT bot")
    put_textarea("prompt",placeholder="Input prompt here", rows=3)
    put_buttons(['submit', 'reset', 'rollback'], 
                onclick=[show_response, chatbot_reset, chatbot_rollback], small=True)
    put_scope("out")

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
