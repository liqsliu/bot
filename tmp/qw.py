#!/bin/python3

import sys
from gradio_client import Client

client = Client("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/")
result = client.predict(
		sys.argv[1],	# str  in 'Input' Textbox component
    #  [[sys.argv[1], sys.argv[1]]],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
    [],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
    "You are a helpful assistant.",	# str  in 'parameter_9' Textbox component
		api_name="/model_chat"
)
#  print(result)
#  print(result[1][1][1])
print(result[1][0][1])
