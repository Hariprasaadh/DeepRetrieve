import { useState } from 'react';
import { FileText, ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react';
// import { Document, Page } from 'react-pdf'; // Uncomment when real PDF logic is ready

function PdfViewer() {
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);
    const [scale, setScale] = useState(1.0);

    // Placeholder for real PDF loading
    const isLoading = false;

    return (
        <div className="flex flex-col h-full bg-[#0a0a12]">
            {/* Toolbar */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-white/5 bg-[#0e0e16]/50 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <div className="p-1.5 rounded-md bg-indigo-500/10 text-indigo-400">
                        <FileText className="w-4 h-4" />
                    </div>
                    <span className="text-sm font-medium text-slate-300">Annual_Report_2024.pdf</span>
                </div>

                <div className="flex items-center gap-1 bg-white/5 rounded-lg p-1">
                    <button className="p-1.5 hover:bg-white/5 rounded-md text-slate-400 hover:text-white transition-colors">
                        <ZoomOut className="w-4 h-4" />
                    </button>
                    <span className="text-xs text-slate-400 min-w-[3rem] text-center">100%</span>
                    <button className="p-1.5 hover:bg-white/5 rounded-md text-slate-400 hover:text-white transition-colors">
                        <ZoomIn className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-auto relative flex justify-center p-8 bg-[#050505] dot-pattern">
                {isLoading ? (
                    <div className="flex flex-col items-center justify-center text-slate-500 gap-3">
                        <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
                        <span className="text-sm">Loading document...</span>
                    </div>
                ) : (
                    /* Placeholder for PDF Page */
                    <div className="w-full max-w-[600px] aspect-[1/1.414] bg-white shadow-2xl relative group">
                        {/* Mock PDF Content for Visuals */}
                        <div className="absolute inset-0 bg-slate-50 overflow-hidden">
                            <div className="w-full h-8 bg-slate-100 border-b border-slate-200 mb-8"></div>
                            <div className="px-8 space-y-4">
                                <div className="h-6 w-3/4 bg-slate-200 mb-6"></div>
                                <div className="h-3 w-full bg-slate-200"></div>
                                <div className="h-3 w-full bg-slate-200"></div>
                                <div className="h-3 w-5/6 bg-slate-200 mb-6"></div>

                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div className="h-24 bg-indigo-50/50 border border-indigo-100 rounded-lg p-2">
                                        <div className="h-full w-full bg-indigo-200/20"></div>
                                    </div>
                                    <div className="space-y-2">
                                        <div className="h-2 w-full bg-slate-200"></div>
                                        <div className="h-2 w-full bg-slate-200"></div>
                                        <div className="h-2 w-4/5 bg-slate-200"></div>
                                    </div>
                                </div>

                                <div className="h-3 w-full bg-slate-200"></div>
                                <div className="h-3 w-full bg-slate-200"></div>
                                <div className="h-3 w-5/6 bg-slate-200"></div>
                            </div>

                            {/* Highlight Overlay Example */}
                            <div className="absolute top-[180px] left-[32px] w-[536px] h-[70px] bg-yellow-400/20 border border-yellow-400/40 mix-blend-multiply rounded-sm cursor-pointer hover:bg-yellow-400/30 transition-colors group/highlight">
                                <div className="absolute -top-7 right-0 bg-yellow-500 text-[10px] text-black px-2 py-0.5 rounded opacity-0 group-hover/highlight:opacity-100 transition-opacity font-medium">
                                    Cited Source 1
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Footer / Pagination */}
            <div className="flex items-center justify-between px-4 py-2 border-t border-white/5 bg-[#0e0e16]/50 backdrop-blur-md">
                <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-white/5 text-slate-400 hover:text-white transition-colors text-sm disabled:opacity-50">
                    <ChevronLeft className="w-4 h-4" />
                    Previous
                </button>
                <span className="text-xs text-slate-500">Page 1 of 12</span>
                <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-white/5 text-slate-400 hover:text-white transition-colors text-sm disabled:opacity-50">
                    Next
                    <ChevronRight className="w-4 h-4" />
                </button>
            </div>
        </div>
    );
}

export default PdfViewer;
