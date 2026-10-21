import { useState } from 'react';
import './Settings.css'

function Settings() {

    const [apiKey, setApiKey] = useState(() => localStorage.getItem('candela_api_key') || '');
    const [proxyUrl, setProxyUrl] = useState(() => localStorage.getItem('candela_proxy_url') || '');
    const [modelName, setModelName] = useState(() => localStorage.getItem('candela_model') || '');  
    const [userName, setUserName] = useState(() => localStorage.getItem('user_name') || '');  

    const saveSettings = () => {
        localStorage.setItem('candela_api_key', apiKey);
        localStorage.setItem('candela_model', modelName);
        localStorage.setItem('candela_proxy_url', proxyUrl)
        localStorage.setItem('user_name', userName)
        alert("Settings saved successfully!");
    }

    return(
        <>
            <h1 className='settings-heading'>Settings</h1>
            <div className="personal-info">
                <div className="personal-info-heading">Personal Info</div>
                <div className="input-group">
                    <label>Your Name</label>
                    <input 
                        type="text" 
                        placeholder="e.g., Tommy" 
                        value={userName}
                        onChange={(e) => setUserName(e.target.value)}
                    />
                </div>
            </div>
            <div className="credentials">
                <div className="credentials-heading">Credentials</div>
                <div className="input-group">
                    <label>Proxy URL</label>
                    <input 
                        type="text" 
                        placeholder="e.g., https://api.openai.com/v1/chat/completions" 
                        value={proxyUrl}
                        onChange={(e) => setProxyUrl(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label>Model Name</label>
                    <input 
                        type="text" 
                        placeholder="e.g., gpt-4o-mini" 
                        value={modelName}
                        onChange={(e) => setModelName(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label>API Key</label>
                    <input 
                        type="password" 
                        placeholder="Leave blank if using local Ollama" 
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                    />
                </div>
                <div className="save-btn-div">
                    <button onClick={saveSettings} className="save-btn">Save Settings</button>
                </div>
            </div>
        </>
    )
}
export default Settings;