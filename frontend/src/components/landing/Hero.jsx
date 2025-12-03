import { ArrowRight, Sparkles, FileText, Image, Table2, ChevronRight } from 'lucide-react'

function Hero() {
  return (
    <div className="relative z-10 mb-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
          
          {/* Left Content */}
          <div className="text-center lg:text-left">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-sm font-medium text-indigo-300 mb-8 backdrop-blur-sm shadow-[0_0_20px_rgba(99,102,241,0.15)]">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>New: Visual Reasoning for Charts &amp; Graphs</span>
              <ArrowRight className="w-4 h-4 text-indigo-400/50" />
            </div>

            {/* Headline */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold tracking-tight mb-6 leading-[1.1]">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400">DeepRetrieve</span>
              <br />
              <span className="text-white/90">The Next Generation</span>
              <br />
              <span className="text-white/70">of Agentic RAG</span>
            </h1>
            
            {/* Description */}
            <p className="text-base md:text-lg text-slate-400 max-w-xl mx-auto lg:mx-0 mb-8 leading-relaxed">
              Upload PDFs and diagrams. DeepRetrieve understands context, reads fine print, and helps you work <span className="text-white font-medium">10x faster</span> with visual reasoning.
            </p>

            {/* CTA Button */}
            <div className="flex flex-col sm:flex-row items-center lg:items-start justify-center lg:justify-start gap-4">
              <a 
                href="#upload"
                className="group h-14 px-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-base font-medium transition-all shadow-[0_0_40px_-5px_rgba(99,102,241,0.5)] hover:shadow-[0_0_50px_-5px_rgba(99,102,241,0.7)] flex items-center gap-3 border border-indigo-400/20"
              >
                Start Retrieving
                <div className="flex items-center">
                  <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" strokeWidth={2} />
                  <ChevronRight className="w-4 h-4 -ml-2 group-hover:translate-x-0.5 transition-transform delay-75" strokeWidth={2} />
                </div>
              </a>
            </div>

            {/* Trust indicators */}
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 mt-10 text-sm text-slate-500">
              <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_6px_rgba(34,197,94,0.8)]"></div>
                <span>No credit card required</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_6px_rgba(34,197,94,0.8)]"></div>
                <span>Powered by Gemini 2.0</span>
              </div>
            </div>
          </div>

          {/* Right Side - 3D Illustration */}
          <div className="relative h-[400px] md:h-[500px] lg:h-[550px]">
            {/* Main glow effects */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-purple-500/20 rounded-full blur-[100px] animate-pulse"></div>
            <div className="absolute top-1/3 right-1/4 w-60 h-60 bg-indigo-500/20 rounded-full blur-[80px] animate-pulse" style={{ animationDelay: '1s' }}></div>
            <div className="absolute bottom-1/4 left-1/3 w-40 h-40 bg-cyan-500/15 rounded-full blur-[60px] animate-pulse" style={{ animationDelay: '2s' }}></div>

            {/* Floating connection lines */}
            <svg className="absolute inset-0 w-full h-full" style={{ filter: 'blur(0.5px)' }}>
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="rgba(129, 140, 248, 0.3)" />
                  <stop offset="50%" stopColor="rgba(168, 85, 247, 0.5)" />
                  <stop offset="100%" stopColor="rgba(34, 211, 238, 0.3)" />
                </linearGradient>
              </defs>
              {/* Animated flowing lines */}
              <path d="M 50 250 Q 150 200 250 280 T 450 220" stroke="url(#lineGradient)" strokeWidth="2" fill="none" className="animate-pulse" />
              <path d="M 100 350 Q 200 300 300 320 T 400 280" stroke="url(#lineGradient)" strokeWidth="1.5" fill="none" className="animate-pulse" style={{ animationDelay: '0.5s' }} />
              <path d="M 80 180 Q 180 220 280 180 T 420 200" stroke="url(#lineGradient)" strokeWidth="1" fill="none" className="animate-pulse" style={{ animationDelay: '1s' }} />
            </svg>

            {/* Central floating documents stack */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 transform perspective-1000">
              {/* Back document */}
              <div className="absolute -top-20 -left-16 w-48 h-60 rounded-xl bg-gradient-to-br from-slate-800/80 to-slate-900/80 border border-white/10 shadow-2xl transform rotate-[-15deg] translate-z-[-40px] backdrop-blur-sm animate-float" style={{ animationDelay: '0.5s' }}>
                <div className="p-4 space-y-3">
                  <div className="h-3 w-3/4 bg-white/10 rounded"></div>
                  <div className="h-2 w-full bg-white/5 rounded"></div>
                  <div className="h-2 w-5/6 bg-white/5 rounded"></div>
                  <div className="h-16 w-full bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-lg border border-purple-500/20 mt-4"></div>
                </div>
              </div>

              {/* Middle document */}
              <div className="absolute -top-10 -left-6 w-52 h-64 rounded-xl bg-gradient-to-br from-indigo-900/60 to-purple-900/60 border border-indigo-500/30 shadow-2xl transform rotate-[-5deg] backdrop-blur-md animate-float" style={{ animationDelay: '0.25s' }}>
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 rounded-xl"></div>
                <div className="p-5 space-y-3 relative">
                  <div className="h-3 w-2/3 bg-white/20 rounded"></div>
                  <div className="h-2 w-full bg-white/10 rounded"></div>
                  <div className="h-2 w-4/5 bg-white/10 rounded"></div>
                  <div className="h-20 w-full bg-gradient-to-br from-indigo-500/30 to-purple-500/30 rounded-lg border border-indigo-400/30 mt-4 flex items-end justify-around p-2">
                    <div className="w-4 h-6 bg-indigo-400/50 rounded-t"></div>
                    <div className="w-4 h-10 bg-indigo-400/70 rounded-t"></div>
                    <div className="w-4 h-8 bg-indigo-400/60 rounded-t"></div>
                    <div className="w-4 h-14 bg-purple-400/80 rounded-t shadow-[0_0_10px_rgba(168,85,247,0.5)]"></div>
                    <div className="w-4 h-9 bg-indigo-400/60 rounded-t"></div>
                  </div>
                </div>
              </div>

              {/* Front document - Main focus */}
              <div className="relative w-56 h-68 rounded-xl bg-gradient-to-br from-[#1a1a2e] to-[#0f0f1a] border border-indigo-500/40 shadow-[0_0_60px_-15px_rgba(99,102,241,0.5)] transform rotate-[5deg] backdrop-blur-lg animate-float">
                <div className="absolute -inset-px bg-gradient-to-br from-indigo-500/20 via-transparent to-purple-500/20 rounded-xl"></div>
                <div className="p-5 space-y-3 relative">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg">
                      <FileText className="w-4 h-4 text-white" />
                    </div>
                    <div className="h-3 w-24 bg-white/30 rounded"></div>
                  </div>
                  <div className="h-2 w-full bg-white/15 rounded"></div>
                  <div className="h-2 w-3/4 bg-white/10 rounded"></div>
                  <div className="h-2 w-5/6 bg-white/10 rounded"></div>
                  
                  {/* Highlighted chart area */}
                  <div className="h-24 w-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-lg border border-indigo-400/40 mt-4 relative overflow-hidden">
                    <div className="absolute inset-0 flex items-end justify-around p-3">
                      <div className="w-5 h-8 bg-gradient-to-t from-indigo-500 to-indigo-400 rounded-t opacity-60"></div>
                      <div className="w-5 h-12 bg-gradient-to-t from-indigo-500 to-indigo-400 rounded-t opacity-70"></div>
                      <div className="w-5 h-10 bg-gradient-to-t from-indigo-500 to-indigo-400 rounded-t opacity-60"></div>
                      <div className="w-5 h-16 bg-gradient-to-t from-purple-500 to-purple-400 rounded-t shadow-[0_0_15px_rgba(168,85,247,0.6)]"></div>
                      <div className="w-5 h-11 bg-gradient-to-t from-indigo-500 to-indigo-400 rounded-t opacity-70"></div>
                    </div>
                    {/* Scan line effect */}
                    <div className="absolute inset-0 bg-gradient-to-b from-cyan-400/20 via-cyan-400/5 to-transparent h-8 animate-scan"></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Floating particles/nodes */}
            <div className="absolute top-16 right-20 w-3 h-3 rounded-full bg-indigo-400 shadow-[0_0_15px_rgba(129,140,248,0.8)] animate-float"></div>
            <div className="absolute top-32 right-8 w-2 h-2 rounded-full bg-purple-400 shadow-[0_0_12px_rgba(168,85,247,0.8)] animate-float" style={{ animationDelay: '0.5s' }}></div>
            <div className="absolute bottom-32 right-16 w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.8)] animate-float" style={{ animationDelay: '1s' }}></div>
            <div className="absolute top-24 left-8 w-2 h-2 rounded-full bg-indigo-300 shadow-[0_0_10px_rgba(165,180,252,0.8)] animate-float" style={{ animationDelay: '1.5s' }}></div>
            <div className="absolute bottom-24 left-12 w-3 h-3 rounded-full bg-purple-300 shadow-[0_0_12px_rgba(216,180,254,0.8)] animate-float" style={{ animationDelay: '0.75s' }}></div>

            {/* Floating icon badges */}
            <div className="absolute top-20 left-4 p-3 rounded-xl bg-gradient-to-br from-slate-800/90 to-slate-900/90 border border-white/10 shadow-xl backdrop-blur-sm animate-float" style={{ animationDelay: '0.3s' }}>
              <FileText className="w-5 h-5 text-indigo-400" />
            </div>
            <div className="absolute bottom-28 left-0 p-3 rounded-xl bg-gradient-to-br from-slate-800/90 to-slate-900/90 border border-white/10 shadow-xl backdrop-blur-sm animate-float" style={{ animationDelay: '0.8s' }}>
              <Image className="w-5 h-5 text-purple-400" />
            </div>
            <div className="absolute top-40 right-0 p-3 rounded-xl bg-gradient-to-br from-slate-800/90 to-slate-900/90 border border-white/10 shadow-xl backdrop-blur-sm animate-float" style={{ animationDelay: '1.2s' }}>
              <Table2 className="w-5 h-5 text-cyan-400" />
            </div>

            {/* Data flow lines connecting to center */}
            <div className="absolute top-24 left-16 w-32 h-px bg-gradient-to-r from-indigo-500/50 to-transparent transform rotate-[30deg]"></div>
            <div className="absolute bottom-32 left-12 w-40 h-px bg-gradient-to-r from-purple-500/50 to-transparent transform rotate-[-20deg]"></div>
            <div className="absolute top-44 right-12 w-28 h-px bg-gradient-to-l from-cyan-500/50 to-transparent transform rotate-[-25deg]"></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero
