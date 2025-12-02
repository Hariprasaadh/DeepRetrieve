import { Layers, ArrowRight } from 'lucide-react'

function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-[#050505]/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative w-7 h-7 flex items-center justify-center">
            <div className="absolute inset-0 bg-indigo-500 blur opacity-20 rounded-full"></div>
            <Layers className="w-5 h-5 text-white relative z-10" strokeWidth={1.5} />
          </div>
          <span className="text-base font-medium tracking-tight text-white">DeepRetrieve</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-normal text-slate-400">
          <a href="#features" className="hover:text-white transition-colors">Features</a>
          <a href="#upload" className="hover:text-white transition-colors">Upload</a>
        </div>

        <div className="flex items-center gap-4">
          <a href="#" className="text-sm font-normal text-slate-300 hover:text-white transition-colors px-2">Log in</a>
          <button className="bg-white text-black text-sm font-medium px-4 py-2 rounded-full hover:bg-neutral-200 transition-colors shadow-[0_0_15px_-3px_rgba(255,255,255,0.3)]">
            Sign Up
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
