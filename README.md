
# Agent Bot & RAG Bot

This project consists of two main components: an **Agent Bot** and a **RAG Bot**, with separate folders for the **Frontend** and the **API**.

## Table of Contents
- [Project Structure](#project-structure)
- [Frontend](#frontend)
- [API](#api)
- [Models Used](#models-used)
- [Usage](#usage)
- [Installation](#installation)

## Project Structure
```
.
├── frontend
│   └── React application with Text-to-Voice integration
└── API
    └── FastAPI application with two routes: `rag/query` and `agent/query`
```

## Frontend
The frontend is built using **React** and integrates the browser's **Text-to-Voice** functionality. This was used because the **Sarvam API** was not functioning properly in English.

### Key Features
- React-based UI for user interaction
- Text-to-Voice conversion using the browser's built-in capabilities to handle English language processing
- Smart API calling from agent to use Sarvam translate APi to translate text to any indiam language 

### How to Run the Frontend
1. Navigate to the `frontend` folder.
2. Install the required packages:
    ```bash
    npm install
    ```
3. Start the frontend application:
    ```bash
    npm start
    ```
The frontend will be served at `http://localhost:3000/`.

## API
The backend API is powered by **FastAPI** and is structured in the `app.py` file. It supports two main routes for handling requests from the frontend.

### Routes
- `/rag/query`: Handles requests for the **RAG Bot**, which retrieves and processes relevant data.
- `/agent/query`: Handles requests for the **Agent Bot**, which provides zero-shot answers using an agent model.

### How to Run the API
To start the API, navigate to the `API` folder and run:

```bash
uvicorn app:app --reload
```

This will start the FastAPI server, and the endpoints can be accessed at `http://127.0.0.1:8000/`.

### Models Used
1. **LLaMA 70B**: A large pre-trained language model that is used for various NLP tasks and queries.
2. **Gemma 2 9B**: Another model integrated for enhanced natural language understanding and response generation.
3. **LangChain Zero-Shot Agent**: Employed to handle zero-shot learning tasks, enabling the bot to answer queries without explicit prior examples.

## Usage
1. **Frontend**: Users can interact with the bot via the frontend React application. It uses Text-to-Voice for feedback.
2. **API**: The frontend sends requests to the backend through the `/rag/query` and `/agent/query` routes to retrieve answers.

### Example Query Flow:
1. A user types a question in the frontend.
2. The frontend sends the question to the `/agent/query` or `/rag/query` route.
3. The API processes the query using the appropriate model and returns a response.
4. The browser's Text-to-Voice feature may vocalize the response.

## Installation

### Prerequisites
- **Node.js** and **npm** for the frontend
- **Python** and **pip** for the API
- FastAPI for the backend and Uvicorn for running the API

### Frontend
1. Navigate to the `frontend` folder:
    ```bash
    cd frontend
    ```
2. Install the required dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm start
    ```

### API
1. Navigate to the `API` folder:
    ```bash
    cd API
    ```
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Start the FastAPI server:
    ```bash
    uvicorn app:app --reload
    ```

---

Feel free to explore and extend the capabilities of this project as needed!
