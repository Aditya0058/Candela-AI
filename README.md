# what is Candela-Agent-MVP
Candela Agent is opensource software where there are lots of tools given to AI which can be used by custom API keys and this project is MVP for that.

# Features 
1. Clean UI with personalized greeting 
2. Local storage of all chats in candela.db
3. Customizable endpoints
4. Good response in formating of tables, break lines, h1, h2, h3, paragraph, links.
5. Create, Delete chat functionality
6. No secretly injected System Prompts except "Name of Candela"

# Screenshots 
![alt text](/Assets/image1.png)

![alt text](/Assets/image2.png)

![alt text](/Assets/image3.png)

# How to run it on your system
### Use following command
```
curl -fsSL https://raw.githubusercontent.com/Aditya0058/Candela-Agent-MVP/main/install.sh | bash

```

## What will above command do
1. It will check requirements
2. Clone this repo
3. Initialize backend with database, and flask (It will wait 8 sec on flask and then move on to next step so please have patience)
4. Run backend on http://127.0.0.1:5000
5. Start React-Vite server on  http://localhost:5173
6. It will open  http://localhost:5173 on default browser automatically

- Now you'll see dasboard of candela agent (MVP)

# How to setup Candela
1. Click on Settings on bottom left sidebar
2. Enter your first name in personal detail section
3. Enter Proxy URL, Model Name, API Key 
4. Click Save
5. Click on New Chat and start chatting.

# From where you'll get Proxy URL, Model Name, API key
1. select model in hackclub ai or any platform you want.
2. You'll find somthing like this (Code Example)

```
 curl https://ai.hackclub.com/proxy/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-3-super-120b-a12b",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }
```

3. Here in this case 
   - Proxy_URL is "https://ai.hackclub.com/proxy/v1/chat/completions"
   - Model name is "nvidia/nemotron-3-super-120b-a12b"
   - API key - you will find this on your api section of any platform you are using

## For developers (If you want to edit something)
1) This project uses React-vite in typescript for frontend and python for backend
2) The Main files to understand are just thee
   - /Frontend/src/App.tsx
   - /src/pages/Chat/tsx
   - /Backend/app.py

3) There is just one system prompt stored in here /Backend/prompts/candela_system.txt

4) Data for chats and messages are stored in /Backend/candela.db --> this database is only generated when /Backend/init_db.py is intialized once.