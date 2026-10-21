import { useEffect, useRef, useState } from "react";
import Chatbox from "../components/Chatbox";
import './Chat.css'
import { useLocation, useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type Message = {id: string; role: string; content: string};
interface chatProps{
    chats: { 
        id: string; 
        title: string; 
        messages: Message[];
    }[];
    updateChatMessages: (chatId: string, newMessages: Message[]) => void;
};

function Chat({chats, updateChatMessages}: chatProps){

    // extracting data
    const location = useLocation();
    const firstPrompt = location.state?.firstPrompt;
    const hasSentFirstPrompt = useRef(false);
    const bottomRef = useRef<HTMLDivElement>(null); 
    const {chatId} = useParams();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const apiKey = localStorage.getItem('candela_api_key') || '';
    const proxyUrl = localStorage.getItem('candela_proxy_url') || '';
    const modelName = localStorage.getItem('candela_model') || ' ';

    const currentChat = chats.find(c => c.id === chatId);
    useEffect(() => {
        if(!firstPrompt || hasSentFirstPrompt.current || (currentChat?.messages.length ?? 0) > 0) return;
        hasSentFirstPrompt.current = true;
        sendPrompt(firstPrompt);
    }, [firstPrompt]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [currentChat?.messages]);
    

    useEffect(() => {
        if (!chatId) return;

    async function loadMessages() {
        const response = await fetch(`http://127.0.0.1:5000/api/chats/${chatId}/messages`);
        const data = await response.json();
        
        // This updates App.tsx with the messages from the DB!
        updateChatMessages(chatId!, data); 
    }

    loadMessages();
    }, [chatId])
    async function sendPrompt(message: string) {
        if(!chatId) return;
        setError(null);
        setIsLoading(true);

        try{
            const existingMessages = currentChat?.messages ?? [];
            const userMessage = { id: crypto.randomUUID(), role: 'user', content: message };
            const updatedMessages = [...existingMessages, userMessage];
    
            updateChatMessages(chatId, updatedMessages);
    
            const response = await fetch("http://127.0.0.1:5000/chats", {
                method:"POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    chat_id: chatId,
                    messages: updatedMessages,
                    api_key: apiKey,
                    proxy_url: proxyUrl,
                    model: modelName
                }),
            })
            const data = await response.json();
            const assistantMessage = {
                id: crypto.randomUUID(), 
                role: 'assistant', 
                content: data.response 
            }
            const finalMessages = [...updatedMessages, assistantMessage];
            updateChatMessages(chatId, finalMessages);
        } catch{
            setError("Failed to connect to the server.");
            console.error("Failed to fetch:", error);
        } finally {
            setIsLoading(false)
        }

    }

    const firstUser = currentChat?.title ?? 'New Chat';
    const title = firstUser
    ? firstUser.length > 40 ? firstUser.slice(0, 40) + '…' : firstUser
    : 'New Chat';
    const now = new Date();

    return (


        <div className="chat-content">
            <div className="chat-header">
                <div className="chat-name">{title}</div>
                <div className="chat-controls">
                    <button className="share-btn">{now.toDateString()}</button>
                </div>
            </div>
            <div className="actual-chats">
                {currentChat?.messages.map((msg) => (
                    <div key={msg.id} className={`message ${msg.role}`}>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                        
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>
            {error && (
                <div className="error-banner">
                    -- {error}
                </div>
            )}
            <div className="chat-box-here">
                <Chatbox 
                onSend={sendPrompt}
                isLoading={isLoading}
                /> 
            </div>
        </div>
    )
}

export default Chat;