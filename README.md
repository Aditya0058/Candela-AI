# what is Candela-AI
Candela Agent is opensource software where there are lots of tools given to AI which can be used by custom API keys and this project is built on top of that Candela-Agent-MVP (its there in my repo list)

# What is there in this new version
1. (most imp) access to tools 
    - now candela has access to multiple tools just ask "what tools do u have"
2. now candela can send messages to you on your telegram 
3. You can schedule any tool you want to execute
4. I know llms are terrible at long math calculations so there is tool for calculation too which makes it easier for LLMs
5. Candela has access to current time and date 
6. Candlela can do web_search now
7. Just say "gimme latest news on ai on telegram tomorrow at 8 AM"
8. Candela can call multiple tools in one chat processing and recieve the return value and again decide whether to call any other tool or not (this goes on as i have set while loop for this and max tool candela can call in one processsing is ig 20)

# HOW to connect telegram 
1. Go to @botfather on telegram and create your bot, name it
2. paste your bot token id in the settings and save it
3. go to any chatid helper (you can go to @ChatIdInfoBot )bot on telegram and get you telegram chat id
4. paste that chat id into settings and save it again 
5. and wollaa your telegram is now connected to candela just say "Send test message to my telegram"

# How to set web_search
1. Go to https://ollama.com/settings/keys
2. create your api key 
3. paste that into web_search api key and save it
4. Don't worry, ollama has single key which is used for web_search as well as for chats just the proxy url is different 
5. don't worry - Proxy url for this candela's backend will automatically get as it has standard format 

# What was in MVP Features 
1. Clean UI with personalized greeting 
2. Local storage of all chats in candela.db
3. Customizable endpoints
4. Good response in formating of tables, break lines, h1, h2, h3, paragraph, links.
5. Create, Delete chat functionality
6. No secretly injected System Prompts except "Name of Candela"

# How to add your own new custom tools that u want to give to candela
1. go to /Backend/agent/tools 
2. you'll see __init__.py and other tools.py
3. that init python file is registery for all tools present because this registry is what gets forwarded to llm in each chat request so it is must to register you tool here after creating one
4. Create your new (tool_name.py)  and write python funtion to it 
5. You can see that in end of each tool python file there is TOOL_SCHEMA
6. This tool schema is what that gets imported into registry later so please fill this in exact format (open ai format)
7. you have to define description, pramerters and thier types, properties, and at last requred parameter constraint(optional). So please write accordingly. all the best 
8. I reccommend just paste this section of readme to ai and he'll do it.

# Screenshots 
chat with candela
![alt text](/Assets/image4.png)
candela on telegram
![alt text](/Assets/image5.png)
settings ui updated
![alt text](/Assets/image6.png)

# How to run it on your system
### Use following command
```
curl -fsSL https://raw.githubusercontent.com/Aditya0058/Candela-AI/main/install.sh | bash

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