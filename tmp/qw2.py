#!/bin/python3

import sys

from gradio_client import Client

client = Client("Qwen/Qwen1.5-110B-Chat-demo")
result = client.predict(
		query=sys.argv[1],
		history=[],
		system="You are a helpful assistant.",
		api_name="/model_chat"
)

#  exit()
#  print(result)
#  print(result[1][1][1])
print(result[1][0][1])
