import './Home.css';
import Chatbox from '../components/Chatbox';
import { useNavigate } from 'react-router-dom';
// import { useEffect } from 'react';


interface HomeProps{
    onCreateChat: (id: string, firstMessage: string) => void;
}
function Home({onCreateChat}: HomeProps) {
    
    // declaring navigations
    const navigate = useNavigate();
    const userName = localStorage.getItem('user_name')

    // sending prompt to chat.tsx
    async function sendPrompt(message: string) { 
        const newChatId = crypto.randomUUID(); 
        onCreateChat(newChatId, message)
        navigate(`/chat/${newChatId}`, { state: { firstPrompt: message } }); 
    }

// ----- 
    return (
        <div className="main-content">
            <div className="greetings">
                <img src="src/assets/candela_logo.png" alt="logo" className='greeting-logo' />
                <h2 className='greeting'>Welcome Back, {userName}</h2>
            </div>
            <Chatbox 
                onSend={sendPrompt} 
                isLoading={false}
            />
        </div>
    )
}

export default Home;
