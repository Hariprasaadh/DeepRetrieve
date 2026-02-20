import { useState } from 'react';
import { FileText, Table2, Image as ImageIcon, Globe, ChevronDown, Copy, Check } from 'lucide-react';

const TYPE_META = {
    text:  { icon: FileText,  label: 'Text',  badge: 'text-sky-400 bg-sky-500/10' },
    table: { icon: Table2,    label: 'Table', badge: 'text-purple-400 bg-purple-500/10' },
    image: { icon: ImageIcon, label: 'Image', badge: 'text-pink-400 bg-pink-500/10' },
    web:   { icon: Globe,     label: 'Web',   badge: 'text-blue-400 bg-blue-500/10' },
};

const CONFIDENCE = {
    high:   { label: 'High',   color: 'text-green-400 bg-green-500/10' },
    medium: { label: 'Medium', color: 'text-yellow-400 bg-yellow-500/10' },
    low:    { label: 'Low',    color: 'text-orange-400 bg-orange-500/10' },
};

/** Humanize source name — strip .pdf, detect temp patterns */
function humanizeName(source, type) {
    if (!source) return 'Document';
    if (type === 'web') {
        try { return new URL(source).hostname; } catch { return source; }
    }
    const base = source.replace(/\.pdf$/i, '');
    // Looks like a temp file: starts with "tmp" followed by random alphanum
    if (/^tmp[a-z0-9_]{4,}$/i.test(base)) return 'Uploaded Document';
    // Capitalize first letter and replace underscores/hyphens with spaces
    return base.replace(/[_-]+/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

/** Cleaned content for display */
function formatContent(content, type) {
    if (!content) return '';
    if (type === 'table') {
        const rows = content.split('\n').filter(r => r.trim());
        return rows.slice(0, 4).map(r => r.trim()).join('\n') || content;
    }
    // Strip old generic fallback text
    if (/^Image from (page \d+ of )?tmp[a-z0-9_]+\.pdf/i.test(content.trim())) {
        return 'Visual content — no caption available for this item.';
    }
    return content;
}

function CopyButton({ text }) {
    const [copied, setCopied] = useState(false);
    const handleCopy = (e) => {
        e.stopPropagation();
        navigator.clipboard.writeText(text).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 1800);
        });
    };
    return (
        <button
            onClick={handleCopy}
            className="flex items-center gap-1 text-[10px] text-slate-500 hover:text-slate-300 transition-colors px-1.5 py-0.5 rounded hover:bg-white/5"
        >
            {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
            {copied ? 'Copied' : 'Copy'}
        </button>
    );
}

function SourceCard({ source, index }) {
    const [expanded, setExpanded] = useState(false);

    const score = source.score || 0;
    const conf = score >= 0.7 ? CONFIDENCE.high : score >= 0.5 ? CONFIDENCE.medium : CONFIDENCE.low;
    const meta = TYPE_META[source.type] || TYPE_META.text;
    const Icon = meta.icon;
    const name = humanizeName(source.source, source.type);
    const content = formatContent(source.content, source.type);

    return (
        <div
            onClick={() => setExpanded(v => !v)}
            className={`group relative border rounded-lg p-3 transition-all duration-200 cursor-pointer select-none
                ${expanded
                    ? 'bg-[#181826] border-indigo-500/30'
                    : 'bg-[#13131f]/50 border-white/5 hover:bg-[#13131f] hover:border-indigo-500/20'
                }`}
        >
            {/* Top row: index badge + type icon + chevron */}
            <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                    {/* Index circle */}
                    <span className="shrink-0 w-5 h-5 rounded-full bg-indigo-500/15 text-indigo-300 text-[10px] font-bold flex items-center justify-center">
                        {index + 1}
                    </span>
                    <div className="min-w-0">
                        {/* Name */}
                        <p className="text-xs font-semibold text-slate-200 truncate" title={source.source}>
                            {name}
                        </p>
                        {/* Meta row */}
                        <div className="flex items-center gap-1.5 mt-0.5 flex-wrap">
                            {source.page && (
                                <span className="text-[10px] text-slate-500 font-medium">p.{source.page}</span>
                            )}
                            <span className={`text-[9px] px-1.5 py-0.5 rounded font-medium ${conf.color}`}>
                                {conf.label}
                            </span>
                            <span className={`text-[9px] px-1.5 py-0.5 rounded font-medium ${meta.badge}`}>
                                {meta.label}
                            </span>
                        </div>
                    </div>
                </div>
                <div className="flex items-center gap-1 shrink-0 mt-0.5">
                    <Icon className="w-3.5 h-3.5 text-slate-600 group-hover:text-indigo-400 transition-colors" />
                    <ChevronDown className={`w-3.5 h-3.5 text-slate-600 transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`} />
                </div>
            </div>

            {/* Collapsed preview */}
            {!expanded && (
                <p className="text-xs text-slate-500 mt-2 line-clamp-2 leading-relaxed">
                    {content}
                </p>
            )}

            {/* Expanded full content */}
            {expanded && (
                <div className="mt-3 pt-3 border-t border-white/5" onClick={e => e.stopPropagation()}>
                    <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-line">
                        {content}
                    </p>
                    <div className="flex items-center justify-between mt-3">
                        {source.source && (
                            <span className="text-[10px] text-slate-600 font-mono truncate max-w-[60%]" title={source.source}>
                                {source.source}
                            </span>
                        )}
                        <CopyButton text={content} />
                    </div>
                </div>
            )}
        </div>
    );
}

function SourcesPanel({ sources = [] }) {
    return (
        <div className="flex flex-col h-full bg-[#0a0a12] border-l border-white/5">
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/5">
                <h3 className="text-sm font-semibold text-slate-200">Retrieval Sources</h3>
                <span className="text-xs text-slate-500">{sources.length} Found</span>
            </div>

            {/* Sources List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-2.5">
                {sources.length > 0 ? (
                    sources.map((source, idx) => (
                        <SourceCard key={idx} source={source} index={idx} />
                    ))
                ) : (
                    <div className="p-4 mt-4 text-center">
                        <p className="text-xs text-slate-600">Sources appear here as you chat.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default SourcesPanel;
