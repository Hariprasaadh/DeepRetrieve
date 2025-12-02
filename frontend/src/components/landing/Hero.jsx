import { ArrowRight, Sparkles } from 'lucide-react'

function Hero() {
  return (
    <div className="max-w-4xl mx-auto text-center relative z-10 mb-20">
      {/* Badge */}
      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 text-sm font-medium text-indigo-300 mb-8 backdrop-blur-sm shadow-[0_0_20px_rgba(99,102,241,0.15)]">
        <Sparkles className="w-4 h-4 text-indigo-400" />
        <span>New: Visual Reasoning for Charts &amp; Graphs</span>
        <ArrowRight className="w-4 h-4 text-indigo-400/50" />
      </div>

      {/* Headline */}
      <h1 className="text-5xl md:text-7xl lg:text-8xl font-medium tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-white/40 mb-8 leading-[1.05]">
        Your second brain,<br />
        <span>
          built for documents
        </span>
      </h1>
      
      {/* Description */}
      <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
        Upload PDFs and diagrams. DeepRetrieve understands context, reads fine print, and helps you work <span className="text-white font-medium">10x faster</span> with visual reasoning.
      </p>

      {/* CTA Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
        <a 
          href="#upload"
          className="group h-12 px-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-400 hover:to-purple-400 text-white text-base font-medium transition-all shadow-[0_0_30px_-5px_rgba(99,102,241,0.5)] hover:shadow-[0_0_40px_-5px_rgba(99,102,241,0.7)] flex items-center gap-2"
        >
          Try for free 
          <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" strokeWidth={2} />
        </a>
        <a 
          href="#comparison"
          className="h-12 px-8 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-white text-base font-medium transition-all flex items-center gap-2"
        >
          See how it works
        </a>
      </div>

      {/* Trust indicators */}
      <div className="flex items-center justify-center gap-8 mt-12 text-sm text-slate-500">
        <div className="flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_6px_rgba(34,197,94,0.8)]"></div>
          <span>No credit card required</span>
        </div>
        <div className="hidden sm:block w-px h-4 bg-white/10"></div>
        <div className="hidden sm:flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_6px_rgba(34,197,94,0.8)]"></div>
          <span>Powered by Gemini 2.0</span>
        </div>
      </div>
    </div>
  )
}

export default Hero
