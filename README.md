# Overview
This Repo is an exploration space for all things LLM including transformers, gpt, llama2

# WIP - Where Am I

* I have gotten to the point of prompting and querying the db, there are no returned results so must add one
* I need to load some documents into the doc db and vectordb in order to run the prompt against the doc db



# Resources

* Embeddings:
    - **all-MiniLM-L6-v2**
        - https://www.sbert.net/docs/pretrained_models.html
        - Usage: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

* Vector DB:
    - vectordb - https://jina.ai/news/vectordb-a-python-vector-database-you-just-need-no-more-no-less/

* Llama Index:
    - https://www.llamaindex.ai/

* Services:
    - https://chat.openai.com/c/b12024cf-2f00-47f1-a277-ddad399e2cf6


* Running Llama Locally: https://replicate.com/blog/run-llama-locally
* When to Fine Tune: https://towardsdatascience.com/when-should-you-fine-tune-llms-2dddc09a404a
* Run Llama locally on python: https://swharden.com/blog/2023-07-29-ai-chat-locally-with-python/
* Get Llama 2 from hubbingface: https://huggingface.co/blog/llama2
* llama2 7B chat: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
* Meta License, AUP: https://ai.meta.com/llama/license/, https://ai.meta.com/llama/use-policy/
* huggingface: https://huggingface.co/welcome
* Transformers Reinforcement Learning: https://github.com/huggingface/trl
* PEFT (Parameter Efficient Fine Tuning): https://huggingface.co/blog/peft

# Development
> `make attach-dev`
The above command will spin up a docker container and attach to it via shell. You will start up in `/opt/dev-workspace` which contains a bind mount of the local pwd, enabling you to interactively develop in the container environment while persisting the repo code on the host machine.

**Note** when the application is in production, only the contents of `/app` folder, and `requirements.txt` file are copied to run the application.

# llama 2 git
> Must have accepted license and received email with url for downloading the weights
This repo contains a llama 2 subpackage by running * `git clone git@github.com:facebookresearch/llama.git`
* Then subsequently cd into the llama dir ad run ./download.sh

must have wget and md5sha1sum