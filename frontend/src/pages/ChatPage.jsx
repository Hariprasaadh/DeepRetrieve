import WorkspaceLayout from '../components/chat/WorkspaceLayout';
import PdfViewer from '../components/chat/PdfViewer';
import ChatPanel from '../components/chat/ChatPanel';
import SourcesPanel from '../components/chat/SourcesPanel';

function ChatPage() {
    return (
        <WorkspaceLayout
            pdfPanel={<PdfViewer />}
            chatPanel={<ChatPanel />}
            sourcesPanel={<SourcesPanel />}
        />
    );
}

export default ChatPage;
