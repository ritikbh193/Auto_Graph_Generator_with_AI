# !pip -q install sentence-transformers
# !pip install -q transformers
# !CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python==0.2.44 --force-reinstall --no-cache-dir

# !apt update
# !apt install -y build-essential

# !pip install -q llama-index==0.9.47
# !pip install langchain


import llama_cpp
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext


import torch

from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
llm = LlamaCPP(
    model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q3_K_M.gguf',
    # model_url = 'https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-uncensored-GGUF/resolve/main/Llama-3.2-3B-Instruct-uncensored-Q6_K.gguf',
    model_path=None,
    temperature=0.1,
    max_new_tokens=256,
    context_window=3000,
    generate_kwargs={},
    model_kwargs={"n_gpu_layers": -1},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,

)

respone = llm.complete(f'Extact the important information from this text and arrange in structure fromate {l}')
print(respone)