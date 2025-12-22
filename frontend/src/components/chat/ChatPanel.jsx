import { useState, useEffect } from 'react';
import { Send, Bot, User, Paperclip, Sparkles, Plus, ArrowUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = 'http://localhost:8000';

function ChatPanel({ onSourcesUpdate }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [uploadedPdf, setUploadedPdf] = useState(null);
    
    useEffect(() => {
        // Get uploaded PDF name from localStorage
        const pdfName = localStorage.getItem('uploadedPdfName');
        if (pdfName) {
            setUploadedPdf(pdfName);
        }
    }, []);

    // Suggested questions for the Hero section
    const suggestions = [
        "Summarize the key financial highlights",
        "What are the risks mentioned in section 4?",
        "Compare Q4 revenue with Q3",
    ];

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input.trim();
        const newMsg = { id: Date.now(), role: 'user', content: userMessage, timestamp: 'Now' };
        setMessages((prev) => [...prev, newMsg]);
        setInput('');
        setIsTyping(true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: userMessage,
                    top_k: 5
                }),
            });

            if (!response.ok) {
                throw new Error('Query failed');
            }

            const data = await response.json();
            
            setIsTyping(false);
            const aiMsg = {
                id: Date.now() + 1,
                role: 'ai',
                content: data.answer,
                timestamp: 'Just now',
                sources: data.sources || [],
                usedWeb: data.used_web_search || false
            };
            setMessages((prev) => [...prev, aiMsg]);
            
            // Update sources panel
            if (onSourcesUpdate && data.sources) {
                onSourcesUpdate(data.sources, data.used_web_search);
            }
        } catch (error) {
            setIsTyping(false);
            const errorMsg = {
                id: Date.now() + 1,
                role: 'ai',
                content: `Sorry, I encountered an error: ${error.message}. Please make sure the backend is running.`,
                timestamp: 'Just now'
            };
            setMessages((prev) => [...prev, errorMsg]);
        }
    };

    return (
        <div className="flex flex-col h-full relative font-sans">

            {/* Scrollable Message Area */}
            <div className="flex-1 overflow-y-auto px-3 sm:px-6 md:px-10 py-4 sm:py-6 space-y-6 sm:space-y-8 scrollbar-thin scrollbar-thumb-white/5 scrollbar-track-transparent">

                {/* Hero / Empty State */}
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center -mt-10 sm:-mt-20 opacity-0 animate-[fadeIn_0.5s_ease-out_forwards] px-4">
                        <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2 sm:mb-3 tracking-tight text-center">
                            Good evening, Alex
                        </h1>
                        <p className="text-slate-400 text-base sm:text-lg mb-6 sm:mb-10 max-w-md text-center leading-relaxed">
                            {uploadedPdf ? (
                                <>
                                    Ready to analyze <span className="text-slate-200 font-medium">{uploadedPdf}</span>?
                                    Ask me anything about the document.
                                </>
                            ) : (
                                <>
                                    Upload a document to get started.
                                </>
                            )}
                        </p>

                        <div className="grid gap-2 sm:gap-3 w-full max-w-md">
                            {suggestions.map((q, i) => (
                                <button
                                    key={i}
                                    onClick={() => setInput(q)}
                                    className="bg-[#1a1a23]/50 hover:bg-[#1a1a23] border border-white/5 hover:border-indigo-500/30 px-3 sm:px-4 py-2.5 sm:py-3 rounded-lg sm:rounded-xl text-left text-xs sm:text-sm text-slate-300 hover:text-white transition-all flex items-center justify-between group"
                                >
                                    <span className="truncate">{q}</span>
                                    <ArrowUp className="w-3.5 h-3.5 sm:w-4 sm:h-4 opacity-0 group-hover:opacity-100 -rotate-45 transition-all text-slate-500 flex-shrink-0 ml-2" />
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Message List */}
                <AnimatePresence>
                    {messages.map((msg) => (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            key={msg.id}
                            className={`flex gap-3 sm:gap-5 max-w-3xl mx-auto ${msg.role === 'user' ? 'justify-end' : ''}`}
                        >
                            {/* AI Avatar */}
                            {msg.role === 'ai' && (
                                <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex-shrink-0 flex items-center justify-center mt-1">
                                    <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                                </div>
                            )}

                            {/* Content */}
                            <div className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} max-w-[90%] sm:max-w-[85%]`}>
                                <div
                                    className={`text-sm sm:text-[15px] leading-6 sm:leading-7 ${msg.role === 'user'
                                            ? 'bg-[#1a1a23] px-3.5 sm:px-5 py-2.5 sm:py-3 rounded-xl sm:rounded-2xl rounded-tr-sm text-slate-200 border border-white/5'
                                            : 'text-slate-300 px-0 py-1'
                                        }`}
                                >
                                    {msg.role === 'user' ? (
                                        msg.content
                                    ) : (
                                        // Simple Markdown simulation
                                        <div className="prose prose-invert prose-p:leading-7 prose-strong:text-indigo-200">
                                            <div dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, '<br/>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* User Avatar (Hidden for cleaner look, or minimal dot) */}
                            {msg.role === 'user' && (
                                <div className="w-8 h-8 rounded-full bg-slate-700/50 flex flex-col items-center justify-center mt-1 text-xs font-medium text-slate-300">
                                    Me
                                </div>
                            )}
                        </motion.div>
                    ))}

                    {isTyping && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-5 max-w-3xl mx-auto">
                            <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex-shrink-0 flex items-center justify-center">
                                <Sparkles className="w-4 h-4" />
                            </div>
                            <div className="flex gap-1 items-center h-8">
                                <span className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-bounce"></span>
                                <span className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-bounce delay-75"></span>
                                <span className="w-1.5 h-1.5 bg-slate-500 rounded-full animate-bounce delay-150"></span>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Floating Input Area */}
            <div className="p-3 sm:p-6 pt-0 bg-transparent relative z-20 flex justify-center">
                <div className="w-full max-w-3xl relative">
                    <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-indigo-500/20 rounded-xl sm:rounded-2xl opacity-0 focus-within:opacity-100 transition-opacity duration-500 blur-lg"></div>

                    <form onSubmit={handleSend} className="relative bg-[#0e0e16]/80 backdrop-blur-2xl border border-white/10 rounded-xl sm:rounded-2xl shadow-2xl flex items-end p-1.5 sm:p-2 transition-all ring-1 ring-white/0 focus-within:ring-white/5">

                        <button type="button" className="p-2 sm:p-3 text-slate-400 hover:text-white transition-colors hover:bg-white/5 rounded-lg sm:rounded-xl self-end mb-0.5">
                            <Plus className="w-4 h-4 sm:w-5 sm:h-5" />
                        </button>

                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSend(e);
                                }
                            }}
                            placeholder="Ask anything about the document..."
                            rows={1}
                            className="flex-1 bg-transparent border-none focus:ring-0 text-slate-200 placeholder:text-slate-500 px-2 sm:px-3 py-3 sm:py-3.5 text-sm sm:text-base resize-none max-h-32 min-h-[44px] sm:min-h-[52px]"
                            style={{ fieldSizing: 'content' }}
                        />

                        <button
                            type="submit"
                            disabled={!input.trim()}
                            className={`p-2 sm:p-3 rounded-lg sm:rounded-xl transition-all duration-300 self-end mb-0.5 ${input.trim() ? 'bg-indigo-600 text-white shadow-[0_0_15px_rgba(99,102,241,0.5)] hover:bg-indigo-500' : 'bg-white/5 text-slate-500'}`}
                        >
                            <ArrowUp className="w-4 h-4 sm:w-5 sm:h-5" />
                        </button>
                    </form>

                    <p className="text-center text-[9px] sm:text-[10px] text-slate-600 mt-2 sm:mt-3 font-medium tracking-wide">
                        DEEPRETRIEVE AGENT v1.2
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ChatPanel;
