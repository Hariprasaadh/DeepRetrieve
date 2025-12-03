import { Plus, FileText, Image, UploadCloud, Share, MoreHorizontal, Sparkles, PlusCircle, ArrowUp } from 'lucide-react'

function AppMockup() {
  return (
    <div className="w-full max-w-7xl relative group perspective-1000 px-2 sm:px-0">
      {/* Glow effect behind */}
      <div className="absolute -inset-1 bg-gradient-to-t from-indigo-500/10 via-purple-500/10 to-transparent rounded-2xl opacity-50 blur-3xl group-hover:opacity-75 transition-opacity duration-1000"></div>
      
      {/* Main Window */}
      <div className="relative glass-panel rounded-xl overflow-hidden flex flex-col md:flex-row h-[500px] sm:h-[600px] md:h-[700px] lg:h-[800px] w-full border border-white/10 shadow-2xl">
        
        {/* SIDEBAR: Files */}
        <div className="hidden md:flex flex-col w-56 lg:w-72 border-r border-white/5 bg-[#080808]/50 p-3 lg:p-5">
          <div className="flex items-center justify-between mb-6 lg:mb-8">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500/20 border border-red-500/50"></span>
              <span className="w-2 h-2 rounded-full bg-yellow-500/20 border border-yellow-500/50"></span>
              <span className="w-2 h-2 rounded-full bg-green-500/20 border border-green-500/50"></span>
            </div>
            <button className="p-1.5 hover:bg-white/5 rounded transition-colors text-slate-500 hover:text-white">
              <Plus className="w-4 h-4" strokeWidth={1.5} />
            </button>
          </div>

          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-4 px-1">Library</div>

          {/* File List */}
          <div className="space-y-2 flex-1 overflow-hidden">
            {/* Active File */}
            <div className="group flex items-center gap-2 lg:gap-3 p-2 lg:p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20 cursor-pointer">
              <div className="w-8 h-8 lg:w-9 lg:h-9 rounded-md bg-indigo-500/20 flex items-center justify-center text-indigo-400 shrink-0">
                <FileText className="w-4 h-4 lg:w-5 lg:h-5" strokeWidth={1.5} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs lg:text-sm font-medium text-white truncate">Q3_Financial_Report.pdf</div>
                <div className="text-xs text-indigo-300/70 hidden lg:block">Processing complete</div>
              </div>
            </div>

            {/* Image File */}
            <div className="group flex items-center gap-2 lg:gap-3 p-2 lg:p-3 rounded-lg hover:bg-white/5 border border-transparent hover:border-white/5 cursor-pointer transition-colors">
              <div className="w-8 h-8 lg:w-9 lg:h-9 rounded-md bg-white/5 flex items-center justify-center text-slate-500 group-hover:text-slate-300 shrink-0">
                <Image className="w-4 h-4 lg:w-5 lg:h-5" strokeWidth={1.5} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs lg:text-sm font-medium text-slate-400 group-hover:text-slate-200 truncate">App_Architecture_v2.png</div>
                <div className="text-xs text-slate-600 hidden lg:block">Added 2h ago</div>
              </div>
            </div>
          </div>

          {/* Upload Zone Mini */}
          <div className="mt-4 lg:mt-6 pt-4 lg:pt-6 border-t border-white/5">
            <div className="border border-dashed border-white/10 rounded-xl p-3 lg:p-5 text-center hover:border-indigo-500/30 hover:bg-indigo-500/5 transition-all cursor-pointer group/drop">
              <UploadCloud className="w-5 h-5 lg:w-6 lg:h-6 text-slate-600 group-hover/drop:text-indigo-400 mx-auto mb-2 lg:mb-3 transition-colors" strokeWidth={1.5} />
              <div className="text-xs font-medium text-slate-500 group-hover/drop:text-slate-300">Drop files to upload</div>
            </div>
          </div>
        </div>

        {/* MAIN AREA: Split View */}
        <div className="flex-1 flex flex-col bg-[#030303]/40 relative">
          {/* Top Bar */}
          <div className="h-12 sm:h-14 lg:h-16 border-b border-white/5 flex items-center justify-between px-3 sm:px-4 lg:px-8 bg-[#030303]/60 backdrop-blur-md">
            <div className="flex items-center gap-2 sm:gap-4">
              <span className="text-xs sm:text-sm font-medium text-white truncate max-w-[120px] sm:max-w-none">Q3_Financial_Report.pdf</span>
              <span className="px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-md text-[10px] sm:text-xs bg-green-500/10 text-green-400 border border-green-500/20 font-medium tracking-wide">Analyzed</span>
            </div>
            <div className="flex items-center gap-2 sm:gap-4">
              <div className="hidden sm:flex items-center gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full bg-white/5 border border-white/5 text-xs font-medium text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-purple-400 shadow-[0_0_6px_rgba(192,132,252,0.8)]"></span>
                Gemini 2.0
              </div>
              <button className="text-slate-500 hover:text-white transition-colors p-1"><Share className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} /></button>
              <button className="text-slate-500 hover:text-white transition-colors p-1"><MoreHorizontal className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} /></button>
            </div>
          </div>

          <div className="flex-1 flex overflow-hidden relative">
            {/* PDF Viewer Mock */}
            <div className="hidden lg:block w-1/2 p-8 overflow-hidden border-r border-white/5 bg-[#0a0a0a]">
              <div className="w-full bg-white rounded shadow-2xl p-12 min-h-[900px] relative overflow-hidden group/pdf transform transition-transform hover:scale-[1.002] duration-500">
                {/* Fake Document Content */}
                <div className="h-6 w-2/3 bg-slate-200 rounded mb-10"></div>
                <div className="space-y-4 mb-12">
                  <div className="h-3 w-full bg-slate-100 rounded"></div>
                  <div className="h-3 w-full bg-slate-100 rounded"></div>
                  <div className="h-3 w-5/6 bg-slate-100 rounded"></div>
                  <div className="h-3 w-full bg-slate-100 rounded"></div>
                </div>
                
                {/* Chart Highlight */}
                <div className="relative rounded-lg border border-indigo-500/40 p-6 bg-indigo-50/50 mb-12 transition-all">
                  {/* Sidebar marker */}
                  <div className="absolute -left-4 top-1/2 -translate-y-1/2 w-1.5 h-16 bg-indigo-500 rounded-r shadow-[0_0_10px_rgba(99,102,241,0.5)]"></div>
                  
                  <div className="h-48 w-full bg-slate-50/50 rounded flex items-end justify-around gap-4 px-6 pb-4">
                    <div className="w-10 h-[35%] bg-indigo-200 rounded-t-sm"></div>
                    <div className="w-10 h-[45%] bg-indigo-300 rounded-t-sm"></div>
                    <div className="w-10 h-[40%] bg-indigo-200 rounded-t-sm"></div>
                    <div className="w-10 h-[75%] bg-indigo-500 rounded-t-sm shadow-[0_0_20px_rgba(99,102,241,0.4)] relative group-hover/pdf:brightness-110 transition-all"></div>
                    <div className="w-10 h-[60%] bg-indigo-300 rounded-t-sm"></div>
                  </div>
                  {/* Scan Line Animation */}
                  <div className="scan-line top-1/2"></div>
                </div>

                <div className="space-y-4">
                  <div className="h-3 w-full bg-slate-100 rounded"></div>
                  <div className="h-3 w-full bg-slate-100 rounded"></div>
                  <div className="h-3 w-3/4 bg-slate-100 rounded"></div>
                </div>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="flex-1 flex flex-col relative z-10 bg-[#050505]">
              {/* Chat History */}
              <div className="flex-1 p-4 sm:p-6 lg:p-8 space-y-4 sm:space-y-6 lg:space-y-8 overflow-hidden">
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="chat-bubble bg-[#1a1a1a] border border-white/5 text-slate-200 text-xs sm:text-sm px-3 sm:px-4 lg:px-5 py-3 sm:py-4 rounded-2xl rounded-tr-sm max-w-[90%] sm:max-w-[85%] shadow-sm leading-relaxed">
                    Analyze the revenue growth in Q3 compared to the previous quarter based on the chart.
                  </div>
                </div>

                {/* AI Message */}
                <div className="flex items-start gap-2 sm:gap-3 lg:gap-4">
                  <div className="w-7 h-7 sm:w-8 sm:h-8 lg:w-9 lg:h-9 rounded-lg lg:rounded-xl bg-indigo-600 flex items-center justify-center shrink-0 shadow-[0_0_15px_-3px_rgba(79,70,229,0.4)]">
                    <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-white" strokeWidth={1.5} />
                  </div>
                  <div className="space-y-2 sm:space-y-3 max-w-[90%]">
                    <div className="chat-bubble bg-gradient-to-br from-indigo-900/10 to-[#0F0F0F] border border-indigo-500/20 text-slate-300 text-xs sm:text-sm px-4 sm:px-5 lg:px-6 py-3 sm:py-4 lg:py-5 rounded-2xl rounded-tl-sm shadow-md">
                      <p className="mb-3 sm:mb-4 lg:mb-5 leading-relaxed text-slate-200">Based on the chart on page 3, Q3 revenue shows a significant upward trend.</p>
                      
                      <div className="grid grid-cols-2 gap-2 sm:gap-3 lg:gap-4 mb-3 sm:mb-4 lg:mb-5">
                        <div className="bg-black/40 border border-white/5 p-2 sm:p-3 lg:p-4 rounded-lg lg:rounded-xl">
                          <div className="text-[10px] sm:text-xs text-slate-500 uppercase tracking-wider font-medium mb-1 sm:mb-1.5">Q2 Revenue</div>
                          <div className="text-base sm:text-lg lg:text-xl font-medium text-white">$2.4M</div>
                        </div>
                        <div className="bg-indigo-500/10 border border-indigo-500/30 p-2 sm:p-3 lg:p-4 rounded-lg lg:rounded-xl relative overflow-hidden group/stat">
                          <div className="absolute inset-0 bg-indigo-500/5 blur-xl group-hover/stat:bg-indigo-500/10 transition-all"></div>
                          <div className="text-[10px] sm:text-xs text-indigo-300 uppercase tracking-wider font-medium mb-1 sm:mb-1.5 relative z-10">Q3 Revenue</div>
                          <div className="text-base sm:text-lg lg:text-xl font-medium text-white relative z-10 flex items-center gap-1 sm:gap-2 flex-wrap">
                            $3.8M 
                            <span className="text-[10px] sm:text-xs font-medium text-green-400 bg-green-400/10 px-1 sm:px-1.5 py-0.5 rounded border border-green-400/20">↑ 58%</span>
                          </div>
                        </div>
                      </div>
                      
                      <p className="text-slate-400 text-[10px] sm:text-xs leading-relaxed">The spike in the 4th month suggests the new product launch was the primary driver.</p>
                    </div>
                    <div className="flex gap-2 sm:gap-2.5">
                      <button className="text-[10px] sm:text-xs font-medium text-slate-500 hover:text-white border border-white/5 bg-white/5 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full transition-colors hover:bg-white/10">Copy</button>
                      <button className="text-[10px] sm:text-xs font-medium text-slate-500 hover:text-white border border-white/5 bg-white/5 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full transition-colors hover:bg-white/10">Generate Chart</button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Input Area */}
              <div className="p-3 sm:p-4 lg:p-6 bg-[#050505] border-t border-white/5">
                <div className="relative group/input">
                  <div className="absolute left-2 sm:left-3 top-2 sm:top-3 flex gap-2">
                    <button className="p-1.5 sm:p-2 text-slate-500 hover:text-indigo-400 hover:bg-indigo-500/10 rounded-lg transition-colors" title="Upload File">
                      <PlusCircle className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} />
                    </button>
                  </div>
                  <textarea 
                    placeholder="Ask anything about your documents..." 
                    className="w-full bg-[#111] text-white text-xs sm:text-sm rounded-lg sm:rounded-xl pl-10 sm:pl-14 pr-10 sm:pr-14 py-3 sm:py-4 border border-white/10 focus:outline-none focus:border-indigo-500/40 focus:ring-1 focus:ring-indigo-500/20 placeholder:text-slate-600 resize-none h-11 sm:h-14 min-h-[44px] sm:min-h-[56px] transition-all"
                  ></textarea>
                  <button className="absolute right-1.5 sm:right-2 top-1.5 sm:top-2 p-2 sm:p-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors shadow-lg shadow-indigo-900/20">
                    <ArrowUp className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} />
                  </button>
                </div>
                <div className="text-[10px] sm:text-xs text-center text-slate-600 mt-2 sm:mt-3 font-medium">
                  DeepRetrieve can make mistakes. Please verify important information.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AppMockup
