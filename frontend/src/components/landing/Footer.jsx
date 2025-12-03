import { Layers, Twitter, Github } from 'lucide-react'

function Footer() {
  return (
    <footer className="border-t border-white/5 bg-[#020202] pt-12 sm:pt-20 pb-8 sm:pb-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 sm:gap-10 mb-10 sm:mb-16">
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-3 mb-6">
              <Layers className="w-6 h-6 text-indigo-500" strokeWidth={1.5} />
              <span className="text-white font-medium text-lg tracking-tight">DeepRetrieve</span>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed">
              AI-powered workspace for modern teams.
              Designed for multimodal understanding.
            </p>
          </div>
          <div>
            <h4 className="text-white text-sm font-medium mb-5">Product</h4>
            <ul className="space-y-3 text-sm text-slate-500">
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Changelog</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white text-sm font-medium mb-5">Company</h4>
            <ul className="space-y-3 text-sm text-slate-500">
              <li><a href="#" className="hover:text-white transition-colors">About</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white text-sm font-medium mb-5">Legal</h4>
            <ul className="space-y-3 text-sm text-slate-500">
              <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-white/5 pt-6 sm:pt-10 flex flex-col md:flex-row justify-between items-center gap-4 sm:gap-6">
          <p className="text-xs text-slate-600 text-center md:text-left">© 2025 DeepRetrieve Inc.</p>
          <div className="flex gap-6">
            <Twitter className="w-5 h-5 text-slate-600 hover:text-white cursor-pointer transition-colors" strokeWidth={1.5} />
            <Github className="w-5 h-5 text-slate-600 hover:text-white cursor-pointer transition-colors" strokeWidth={1.5} />
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
