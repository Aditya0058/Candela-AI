import { useState } from 'react';
import './Settings.css'

function Settings() {

    const [apiKey, setApiKey] = useState(() => localStorage.getItem('candela_api_key') || '');
    const [proxyUrl, setProxyUrl] = useState(() => localStorage.getItem('candela_proxy_url') || '');
    const [modelName, setModelName] = useState(() => localStorage.getItem('candela_model') || '');  
    const [userName, setUserName] = useState(() => localStorage.getItem('user_name') || '');  
    const [websearchapikey, setwebsearchapikey] = useState(() => localStorage.getItem('web_search_api_key') || '');  
    const [telegrambottoken, settelegrambottoken] = useState(() => localStorage.getItem('telegram_bot_token') || '');  
    const [telegramchatid, settelegrachatid] = useState(() => localStorage.getItem('telegram_chat_id') || '');  

    const saveSettings = () => {
        localStorage.setItem('candela_api_key', apiKey);
        localStorage.setItem('candela_model', modelName);
        localStorage.setItem('candela_proxy_url', proxyUrl)
        localStorage.setItem('web_search_api_key', websearchapikey)
        localStorage.setItem('user_name', userName)
        localStorage.setItem('telegram_bot_token', telegrambottoken)
        localStorage.setItem('telegram_chat_id', telegramchatid)
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
                
            </div>
            <div className="tools-credentials">
                <div className="tools-credential-heading">Tools Credentials</div>
                <div className="input-group">
                    <label>Web Search API Key</label>
                    <input 
                        type="password" 
                        placeholder='put you ollama-web-searchapikey'
                        value={websearchapikey}
                        onChange={(e) => setwebsearchapikey(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label>Telegram Bot Token</label>
                    <input 
                        type="text"
                        placeholder='go to @botfather and create ur token'
                        value={telegrambottoken}
                        onChange={(e) => settelegrambottoken(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label>Telegram Chat ID</label>
                    <input 
                        type="text"
                        placeholder='go to any helper bot and find yours'
                        value={telegramchatid}
                        onChange={(e) => settelegrachatid(e.target.value)}
                    />
                </div>

            </div>
            <div className="save-btn-div">
                    <button onClick={saveSettings} className="save-btn">Save Settings</button>
            </div>
        </>
    )
}
export default Settings;