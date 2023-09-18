import logging
import os
from flask import Flask, request, jsonify

from typing import List
from llama import Llama, Dialog

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CHKPT_DIR = '/model/llama-2-7b-chat'
TOKENIZER_PATH = '/model/tokenizer.model'

# TODO: Find good starting points for seq len and batch
MAX_SEQ_LEN=512
MAX_BATCH_SIZE=6
MAX_GEN_LEN = 100
TEMPERATURE = 0.6
TOP_P = 0.9


@app.route('/infer', methods=['GET', 'POST'])
def infer():

    message = ''

    input_prompt = request.json['input_prompt']
    context_doc = request.json['doc_text']

    app.logger.info(f'Input Prompt Text: {input_prompt}')
    app.logger.info(f'Input Context Doc: {context_doc}')

    generator = Llama.build(
        ckpt_dir=CHKPT_DIR,
        tokenizer_path=TOKENIZER_PATH,
        max_seq_len=MAX_SEQ_LEN,
        max_batch_size=MAX_BATCH_SIZE)

    dialogs: List[Dialog] = [
        [{"role": "system",
          "content": """
          You are a helpful, respectful and honest assistant.
          Always answer as helpfully as possible, while being safe.
          Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
          Please ensure that your responses are socially unbiased and positive in nature.
          If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
          If you don't know the answer to a question, please don't share false information.
          You should also respond to the prompt as though you are Jerry Seinfeld in his TV show.
          """,
          },
         {"role": "system",
          "content": f"Take into account the following relevant information:{context_doc.strip()}"
          },
         {"role": "user", "content": input_prompt.strip()}
        ]]

    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=MAX_GEN_LEN,
        temperature=TEMPERATURE,
        top_p=TOP_P,
    )

    for dialog, result in zip(dialogs, results):
        for msg in dialog:
            message += f"{msg['role'].capitalize()}: {msg['content']}\n"
            message += f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
            message += "\n==================================\n"

    app.logger.info(f'OUTPUT: {message}')

    return jsonify({"response": message})

if __name__ == '__main__':
    import torch
    app.logger.info(f'Torch Device: {torch.device("mps")}')
    app.logger.info(f"MPS support: {torch.backends.mps.is_available()}")
    app.logger.info(f"MPS is built: {torch.backends.mps.is_built()}")
    app.run(host="0.0.0.0", port=os.environ['LLM_SERVICE_PORT'])