#!/bin/bash

# From: https://replicate.com/blog/run-llama-locally
# Avoiding: curl -L "https://replicate.fyi/install-llama-cpp" | bash

# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Build it. `LLAMA_METAL=1` allows the computation to be executed on the GPU
LLAMA_METAL=1 make

# Download model
export MODEL=llama-2-13b-chat.ggmlv3.q4_0.bin
if [ ! -f models/${MODEL} ]; then
    curl -L "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/${MODEL}" -o models/${MODEL}
fi

# Set prompt
PROMPT="Hello! How are you?"

# Run in interactive mode
./main -m ./models/llama-2-13b-chat.ggmlv3.q4_0.bin \
  --color \
  --ctx_size 2048 \
  -n -1 \
  -ins -b 256 \
  --top_k 10000 \
  --temp 0.2 \
  --repeat_penalty 1.1 \
  -t 8