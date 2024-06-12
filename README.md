# Enhancing ChatGPT with Long-Term Memory: A Step-by-Step Guide

This repository contains the code and instructions to integrate long-term memory into a ChatGPT-based chatbot. This allows the chatbot to remember previous conversations and provide more contextually relevant responses.

## Prerequisites

Before you begin, ensure you have the following installed:
- [MongoDB](https://www.mongodb.com/) (cloud-based or local instance)
- [Python](https://www.python.org/) (version 3.7 or higher)
_ [OpenAI](https://platform.openai.com/api-keys) API key

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/msuliot/long-term-memory.git
    cd chatgpt-long-term-memory
    ```

2. Set up a virtual environment and install the required Python packages:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Configure your MongoDB cluster:
    - Create a cluster (if using MongoDB Atlas)


## Environment Variables

Create a `.env` file in the root of the project and add the following variables:

```plaintext
MONGO=your_mongodb_connection_string
OPENAI_API_KEY=your_chatgpt_api_key
```

- `MONGODB_URI`: Your MongoDB connection string.
- `CHATGPT_API_KEY`: Your API key for accessing ChatGPT.

## Usage

1. Create a Profile:
    ```bash
    python create_profile.py
    ```

2. Interact with the chatbot:
    ```bash
    python app.py
    ```

### Commands

- To check short-term memory (current conversation):
    ```plaintext
    stm
    ```

- To check long-term memory (previous conversations):
    ```plaintext
    ltm
    ```

- To end a conversation and save it to long-term memory:
    ```plaintext
    exit, quit, bye, end, done, thanks
    ```