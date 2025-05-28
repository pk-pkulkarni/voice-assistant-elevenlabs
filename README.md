# 🗣️ ElevenLabs Voice Assistant (FastAPI + WebSockets)

A conversational AI **voice assistant** built with [ElevenLabs](https://elevenlabs.io), [FastAPI](https://fastapi.tiangolo.com/), and a modern, responsive frontend. Talk to your custom agent in real time, either by **voice** or **text**!

---

## 🚀 Features

- **Natural voice conversations** via ElevenLabs' advanced conversational AI
- Beautiful, responsive UI with speech and text chat
- FastAPI backend with real-time updates (WebSocket)
- Easy to extend: add knowledge bases, tools, or your own agent logic

---

## 📸 Screenshot

![image](https://github.com/user-attachments/assets/d551ef01-4a01-40ee-8f02-4b866fc47bf3)


---

## 🛠️ Prerequisites

1. **ElevenLabs Account**
    - Sign up at [elevenlabs.io](https://elevenlabs.io/)
    - Create a Conversational Agent and set up your knowledgebase/tools if desired
    - Get your API Key and Agent ID

2. **Python 3.10+** (tested on 3.10+)

3. **Install dependencies**
    ```bash
    pip install fastapi uvicorn python-dotenv elevenlabs pydantic
    ```

4. **Environment variables**  
   Create a `.env` file in your project root:
    ```
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    AGENT_ID=your_agent_id
    ```

---

## 🏃‍♂️ Run the App

1. **Start the server:**
    ```bash
    uvicorn main:app --reload --port 8134
    ```

2. **Open your browser:**
    ```
    http://localhost:8134/
    ```

3. **Talk** to your agent! Use the mic button for voice.

---

## 💡 Extending the Assistant

You can easily **extend** this assistant by adding new knowledgebases or integrating additional tools to your ElevenLabs conversational agent. Perfect for creating custom AI experiences for your website, products, or business.

---

## 📄 Project Structure

