import { Link } from 'react-router-dom';
import './style/Sidebar.css'



interface SidebarProps {
    chats: { id: string; title: string }[];
    deleteChat: (id: string) => void;
}
function Sidebar({chats, deleteChat}: SidebarProps) {
  console.log("Sidebar received chats:", chats); //temp
  return (
    <>
        <div className="sidebar">
            <div className="sidebar-header">
              <Link to="/home">
                <div className="logo"> <img src="src/assets/candela_logo.png" alt="" />Candela</div>
              </Link>
              <Link to="/home" className='new-chat-btn'>New Chat</Link>

            </div>
            <div className="recents-chats-heading">Recents</div>
            <nav className='sidebar-navigation'>
              <ul>
                {chats.map(chat => (
                  <li key={chat.id} className='chat-items'>
                    <Link to={`/chat/${chat.id}`}>{chat.title}</Link>
                    <button 
                    className='delete-btn'
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      deleteChat(chat.id);
                    }}
                    >
                      delete
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
            <div className="sidebar-footer">
              <Link to="/settings" className='settings-btn'>Settings</Link>
            </div>
        </div>
    </>
  )
}

export default Sidebar;
