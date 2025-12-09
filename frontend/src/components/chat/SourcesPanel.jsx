import { FileText, Table2, Image as ImageIcon, ChevronRight } from 'lucide-react';

function SourcesPanel() {
    const sources = [
        {
            id: 1,
            type: 'text',
            title: 'Cloud Services Section',
            content: 'Enterprise cloud adoption increased by 24% YoY driven by new AI workload integration...',
            page: 12,
            confidence: 'High'
        },
        {
            id: 2,
            type: 'table',
            title: 'Q4 Revenue Breakdown',
            content: 'Table showing regional performance highlights. APAC +15%, EMEA +8%...',
            page: 14,
            confidence: 'Medium'
        },
        {
            id: 3,
            type: 'image',
            title: 'Market Expansion Chart',
            content: 'Bar chart illustrating the projected growth in emerging markets over the next fiscal year.',
            page: 18,
            confidence: 'High'
        }
    ];

    return (
        <div className="flex flex-col h-full bg-[#0a0a12] border-l border-white/5">
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/5">
                <h3 className="text-sm font-semibold text-slate-200">Retrieval Sources</h3>
                <span className="text-xs text-slate-500">3 Found</span>
            </div>

            {/* Sources List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {sources.map((source) => (
                    <div
                        key={source.id}
                        className="group relative bg-[#13131f]/50 border border-white/5 hover:bg-[#13131f] hover:border-indigo-500/20 rounded-lg p-3 transition-all duration-200 cursor-pointer"
                    >
                        {/* Type Icon */}
                        <div className="absolute top-3 right-3 text-slate-600 group-hover:text-indigo-400 transition-colors">
                            {source.type === 'text' && <FileText className="w-3.5 h-3.5" />}
                            {source.type === 'table' && <Table2 className="w-3.5 h-3.5" />}
                            {source.type === 'image' && <ImageIcon className="w-3.5 h-3.5" />}
                        </div>

                        <div className="space-y-1.5">
                            <div className="flex items-center gap-2">
                                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500">
                                    Page {source.page}
                                </span>
                                <span className={`text-[9px] px-1 rounded ${source.confidence === 'High' ? 'text-green-400 bg-green-500/10' : 'text-yellow-400 bg-yellow-500/10'
                                    }`}>
                                    {source.confidence}
                                </span>
                            </div>

                            <h4 className="text-sm font-medium text-slate-300 group-hover:text-indigo-200 transition-colors pr-6">
                                {source.title}
                            </h4>

                            <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed opacity-80 group-hover:opacity-100">
                                {source.content}
                            </p>
                        </div>
                    </div>
                ))}

                {/* Empty State / Hint */}
                <div className="p-4 mt-4 text-center">
                    <p className="text-xs text-slate-600">
                        Sources appear here as you chat.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default SourcesPanel;
