import { useState } from 'react';
import WorkspaceLayout from '../components/chat/WorkspaceLayout';
import ChatPanel from '../components/chat/ChatPanel';
import SourcesPanel from '../components/chat/SourcesPanel';

function ChatPage() {
    const [sources, setSources] = useState([]);
    const [usedWeb, setUsedWeb] = useState(false);
    
    const handleSourcesUpdate = (newSources, webUsed) => {
        setSources(newSources || []);
        setUsedWeb(webUsed || false);
    };
    
    return (
        <WorkspaceLayout
            chatPanel={<ChatPanel onSourcesUpdate={handleSourcesUpdate} />}
            sourcesPanel={<SourcesPanel sources={sources} usedWeb={usedWeb} />}
        />
    );
}

export default ChatPage;
