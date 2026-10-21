import './style/Chatbox.css'
import { useState, useEffect, useRef } from 'react';


//defining props
interface ChatboxProps {
    onSend: (message: string) => void;
    isLoading: boolean;
}

function Chatbox({onSend, isLoading} : ChatboxProps) {
    //defining variables
    const[message, setMessage] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const candela_model = localStorage.getItem('candela_model')

    useEffect(() => {
        const el = textareaRef.current;
        if(!el) return;
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px'; 
    }, [message]);
    
    // send Message function
    function sendMessage(){
        onSend(message);
    }
    // entering to send and shift + enter to new line
    function onkeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    
    return (
        <div className="chat-box">
            <textarea 
                placeholder="Enter Something here...." 
                className="user-input" 
                ref={textareaRef} 
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={onkeyDown}
                disabled = {isLoading}
            />
            <div className="chat-box-btns">
                <button className="llm-model">Model:  {candela_model}</button>
                <button className="send-user-input" onClick={sendMessage} disabled={isLoading}>
                    {isLoading ? "Thinking..." : "Send"}
                </button>
            </div>
        </div>
    )
}
export default Chatbox;