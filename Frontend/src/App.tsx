import { Routes, Route, Navigate } from 'react-router-dom';
import './App.css'
import Sidebar from './components/Sidebar.tsx'
import Home from './pages/Home.tsx';
import Chat from './pages/Chat.tsx';
import Settings from './pages/Settings.tsx';
import './components/style/variables.css'
import { useEffect, useState } from 'react';


type Message = {id: string; role: string; content: string};
type ChatSession = {
    id: string;
    title: string;
    messages: Message[];
};


function App() {
  const [chats, setChats] = useState<ChatSession[]>([]);

  useEffect(() => {
    async function loadChats() {
        const response = await fetch("http://127.0.0.1:5000/api/chats");
        const data = await response.json();
        
        // The backend returns chats without the 'messages' array, so we add an empty one to match our type
        const formattedChats = data.map((chat: any) => ({
            ...chat,
            messages: [] 
        }));
        
        setChats(formattedChats);
    }
    
    loadChats();
  }, []);

  const createChat = async (newId: string, firstMessage: string) => {
    const title = firstMessage.length > 30 ? firstMessage.slice(0, 20) + '...' : firstMessage;
    
    await fetch("http://127.0.0.1:5000/api/chats", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: newId, 
          title: title 
        })
    });

    const newChat = {
      id: newId,
      title: firstMessage.length > 30 ? firstMessage.slice(0, 20) + '...' : firstMessage,
      messages: [] 
    };
    
    setChats(prev => [newChat, ...prev]); 
  }

  const updateChatMessages = (chatId: string, newMessages: Message[]) => {
    setChats(prevChats => 
        prevChats.map(chat => {
            if (chat.id === chatId) {
                return { ...chat, messages: newMessages };
            }
            return chat;
        })
    );
  }
  
  const deleteChat = async (chatId: string) => {
    await fetch(`http://127.0.0.1:5000/api/chats/${chatId}`, {
      method: "DELETE"
    })
    const updatedChat = chats.filter(chat => chat.id !== chatId);
    setChats(updatedChat);
  }

  return (
    <>
      <div className="main">
        <Sidebar chats={chats} deleteChat={deleteChat}/>
        <main className="app-content">
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<Home onCreateChat={createChat} />} />
            <Route path="/chat/:chatId" element={<Chat chats={chats} updateChatMessages={updateChatMessages}/>} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<div>404 — Not Found <a href="/home"><button>Navigate to Home Page</button></a></div>}/> 
          </Routes>
        </main>
      </div>
    </>
  )
}

export default App;