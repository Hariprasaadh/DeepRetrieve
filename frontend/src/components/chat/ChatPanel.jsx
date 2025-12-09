import { useState } from 'react';
import { Send, Bot, User, Paperclip, Sparkles, Plus, ArrowUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function ChatPanel() {
    const [messages, setMessages] = useState([
        // Empty state initially for demo purposes
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);

    // Suggested questions for the Hero section
    const suggestions = [
        "Summarize the key financial highlights",
        "What are the risks mentioned in section 4?",
        "Compare Q4 revenue with Q3",
    ];

    const handleSend = (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        // Add user message
        const newMsg = { id: Date.now(), role: 'user', content: input, timestamp: 'Now' };
        setMessages((prev) => [...prev, newMsg]);
        setInput('');
        setIsTyping(true);

        // Simulate AI response delay
        setTimeout(() => {
            setIsTyping(false);
            const aiMsg = {
                id: Date.now() + 1,
                role: 'ai',
                content: "Based on the report, **Cloud Services** revenue grew by 24% YoY, driven by strong enterprise adoption. \n\nThere were significant gains in the APAC region.",
                timestamp: 'Just now'
            };
            setMessages((prev) => [...prev, aiMsg]);
        }, 1500);
    };

    return (
        <div className="flex flex-col h-full relative font-sans">

            {/* Scrollable Message Area */}
            <div className="flex-1 overflow-y-auto px-4 sm:px-10 py-6 space-y-8 scrollbar-thin scrollbar-thumb-white/5 scrollbar-track-transparent">

                {/* Hero / Empty State */}
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center -mt-20 opacity-0 animate-[fadeIn_0.5s_ease-out_forwards]">
                        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-500 blur-2xl absolute opacity-20"></div>
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center mb-6 shadow-xl z-10">
                            <Sparkles className="w-6 h-6 text-white" />
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-3 tracking-tight">
                            Good evening, Alex
                        </h1>
                        <p className="text-slate-400 text-lg mb-10 max-w-md text-center leading-relaxed">
                            Ready to analyze <span className="text-slate-200 font-medium">Annual_Report_2024.pdf</span>?
                            Ask me anything about the document.
                        </p>

                        <div className="grid gap-3 w-full max-w-md">
                            {suggestions.map((q, i) => (
                                <button
                                    key={i}
                                    onClick={() => setInput(q)}
                                    className="bg-[#1a1a23]/50 hover:bg-[#1a1a23] border border-white/5 hover:border-indigo-500/30 px-4 py-3 rounded-xl text-left text-sm text-slate-300 hover:text-white transition-all flex items-center justify-between group"
                                >
                                    {q}
                                    <ArrowUp className="w-4 h-4 opacity-0 group-hover:opacity-100 -rotate-45 transition-all text-slate-500" />
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
                            className={`flex gap-5 max-w-3xl mx-auto ${msg.role === 'user' ? 'justify-end' : ''}`}
                        >
                            {/* AI Avatar */}
                            {msg.role === 'ai' && (
                                <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex-shrink-0 flex items-center justify-center mt-1">
                                    <Sparkles className="w-4 h-4" />
                                </div>
                            )}

                            {/* Content */}
                            <div className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} max-w-[85%]`}>
                                <div
                                    className={`text-[15px] leading-7 ${msg.role === 'user'
                                            ? 'bg-[#1a1a23] px-5 py-3 rounded-2xl rounded-tr-sm text-slate-200 border border-white/5'
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
            <div className="p-6 pt-0 bg-transparent relative z-20 flex justify-center">
                <div className="w-full max-w-3xl relative">
                    <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-indigo-500/20 rounded-2xl opacity-0 focus-within:opacity-100 transition-opacity duration-500 blur-lg"></div>

                    <form onSubmit={handleSend} className="relative bg-[#0e0e16]/80 backdrop-blur-2xl border border-white/10 rounded-2xl shadow-2xl flex items-end p-2 transition-all ring-1 ring-white/0 focus-within:ring-white/5">

                        <button type="button" className="p-3 text-slate-400 hover:text-white transition-colors hover:bg-white/5 rounded-xl self-end mb-0.5">
                            <Plus className="w-5 h-5" />
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
                            className="flex-1 bg-transparent border-none focus:ring-0 text-slate-200 placeholder:text-slate-500 px-3 py-3.5 text-base resize-none max-h-32 min-h-[52px]"
                            style={{ fieldSizing: 'content' }}
                        />

                        <button
                            type="submit"
                            disabled={!input.trim()}
                            className={`p-3 rounded-xl transition-all duration-300 self-end mb-0.5 ${input.trim() ? 'bg-indigo-600 text-white shadow-[0_0_15px_rgba(99,102,241,0.5)] hover:bg-indigo-500' : 'bg-white/5 text-slate-500'}`}
                        >
                            <ArrowUp className="w-5 h-5" />
                        </button>
                    </form>

                    <p className="text-center text-[10px] text-slate-600 mt-3 font-medium tracking-wide">
                        DEEPRETRIEVE AGENT v1.2
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ChatPanel;
