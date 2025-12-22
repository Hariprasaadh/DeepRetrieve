import { FileText, Table2, Image as ImageIcon, Globe } from 'lucide-react';

function SourcesPanel({ sources = [], usedWeb = false }) {
    const getTypeIcon = (type) => {
        switch(type) {
            case 'text': return <FileText className="w-3.5 h-3.5" />;
            case 'table': return <Table2 className="w-3.5 h-3.5" />;
            case 'image': return <ImageIcon className="w-3.5 h-3.5" />;
            case 'web': return <Globe className="w-3.5 h-3.5" />;
            default: return <FileText className="w-3.5 h-3.5" />;
        }
    };
    
    const getConfidenceLevel = (score) => {
        if (score >= 0.7) return { label: 'High', color: 'text-green-400 bg-green-500/10' };
        if (score >= 0.5) return { label: 'Medium', color: 'text-yellow-400 bg-yellow-500/10' };
        return { label: 'Low', color: 'text-orange-400 bg-orange-500/10' };
    };

    return (
        <div className="flex flex-col h-full bg-[#0a0a12] border-l border-white/5">
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/5">
                <h3 className="text-sm font-semibold text-slate-200">Retrieval Sources</h3>
                <span className="text-xs text-slate-500">{sources.length} Found</span>
            </div>

            {/* Sources List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {sources.length > 0 ? (
                    sources.map((source, idx) => {
                        const confidence = getConfidenceLevel(source.score || 0);
                        return (
                            <div
                                key={idx}
                                className="group relative bg-[#13131f]/50 border border-white/5 hover:bg-[#13131f] hover:border-indigo-500/20 rounded-lg p-3 transition-all duration-200 cursor-pointer"
                            >
                                {/* Type Icon */}
                                <div className="absolute top-3 right-3 text-slate-600 group-hover:text-indigo-400 transition-colors">
                                    {getTypeIcon(source.type)}
                                </div>

                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-2">
                                        {source.page && (
                                            <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500">
                                                Page {source.page}
                                            </span>
                                        )}
                                        <span className={`text-[9px] px-1 rounded ${confidence.color}`}>
                                            {confidence.label}
                                        </span>
                                    </div>

                                    {source.source && (
                                        <h4 className="text-sm font-medium text-slate-300 group-hover:text-indigo-200 transition-colors pr-6 truncate">
                                            {source.type === 'web' ? new URL(source.source).hostname : source.source}
                                        </h4>
                                    )}

                                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed opacity-80 group-hover:opacity-100">
                                        {source.content}
                                    </p>
                                </div>
                            </div>
                        );
                    })
                ) : (
                    <div className="p-4 mt-4 text-center">
                        <p className="text-xs text-slate-600">
                            Sources appear here as you chat.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default SourcesPanel;
