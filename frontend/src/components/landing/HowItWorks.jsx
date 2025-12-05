import { Upload, Brain, MessageSquare, ArrowRight } from 'lucide-react'

function HowItWorks() {
  const steps = [
    {
      step: 1,
      icon: Upload,
      title: 'Upload your documents',
      description: 'Simply upload PDFs, images, or diagrams. DeepRetrieve extracts text, tables, and visual content automatically.',
      color: 'cyan',
      mockup: (
        <div className="relative">
          {/* Floating document cards */}
          <div className="absolute -top-4 -right-4 w-20 h-24 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 transform rotate-6 opacity-60"></div>
          <div className="absolute -top-2 -right-2 w-20 h-24 rounded-lg bg-gradient-to-br from-cyan-500/30 to-blue-500/30 border border-cyan-500/40 transform rotate-3 opacity-80"></div>
          
          <div className="relative bg-[#0a0a0a] rounded-xl p-5 border border-white/10">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center">
                <div className="w-5 h-5 rounded bg-cyan-400/50"></div>
              </div>
              <div>
                <div className="h-2.5 w-28 bg-white/20 rounded mb-1.5"></div>
                <div className="h-2 w-20 bg-white/10 rounded"></div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="h-2 w-full bg-white/5 rounded"></div>
              <div className="h-2 w-4/5 bg-white/5 rounded"></div>
              <div className="h-2 w-full bg-white/5 rounded"></div>
            </div>
            <div className="flex gap-2 mt-5">
              <div className="h-8 w-24 bg-cyan-500 rounded-lg shadow-[0_0_20px_rgba(34,211,238,0.3)]"></div>
              <div className="h-8 w-28 bg-white/5 rounded-lg border border-white/10"></div>
            </div>
          </div>
        </div>
      )
    },
    {
      step: 2,
      icon: Brain,
      title: 'AI indexes everything',
      description: 'CLIP embeds text, images & tables into vectors. Qdrant stores them with Binary Quantization for fast retrieval.',
      color: 'indigo',
      mockup: (
        <div className="relative">
          {/* Connection lines effect */}
          <div className="absolute inset-0 overflow-hidden rounded-xl">
            <div className="absolute top-1/4 left-0 w-full h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent animate-pulse"></div>
            <div className="absolute top-2/4 left-0 w-full h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent animate-pulse" style={{ animationDelay: '0.5s' }}></div>
            <div className="absolute top-3/4 left-0 w-full h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent animate-pulse" style={{ animationDelay: '1s' }}></div>
          </div>
          
          <div className="relative bg-[#0a0a0a] rounded-xl p-5 border border-white/10">
            <div className="grid grid-cols-2 gap-3">
              {[
                { color: 'indigo', label: 'Text' },
                { color: 'green', label: 'Image' },
                { color: 'orange', label: 'Table' },
                { color: 'purple', label: 'Vector' }
              ].map((item, i) => (
                <div key={i} className="group/card bg-white/5 rounded-lg p-3 border border-white/5 hover:border-white/20 transition-colors cursor-pointer">
                  <div className="flex items-center gap-2 mb-2">
                    <div className={`w-5 h-5 rounded bg-${item.color}-500/30 flex items-center justify-center`}>
                      <div className={`w-2 h-2 rounded-full bg-${item.color}-400`}></div>
                    </div>
                    <div className={`h-2 w-12 bg-${item.color}-500/40 rounded`}></div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-1.5 w-full bg-white/10 rounded"></div>
                    <div className="h-1.5 w-3/4 bg-white/10 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    },
    {
      step: 3,
      icon: MessageSquare,
      title: 'Ask & get answers',
      description: 'Query your documents naturally. Gemini 2.0 synthesizes answers from text, tables, and images with citations.',
      color: 'purple',
      mockup: (
        <div className="relative">
          {/* Glow effect */}
          <div className="absolute -inset-2 bg-gradient-to-r from-purple-500/10 via-indigo-500/10 to-purple-500/10 rounded-2xl blur-xl"></div>
          
          <div className="relative bg-[#0a0a0a] rounded-xl p-5 border border-white/10">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-lg bg-purple-500/20 border border-purple-500/30 flex items-center justify-center">
                  <div className="w-2 h-2 rounded-full bg-purple-400"></div>
                </div>
                <div className="h-2 w-20 bg-white/20 rounded"></div>
              </div>
              <div className="w-3 h-3 rounded-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.8)] animate-pulse"></div>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-gradient-to-br from-purple-500/10 to-indigo-500/10 rounded-lg p-2 border border-purple-500/20 hover:border-purple-500/40 transition-colors">
                  <div className="w-full h-5 bg-purple-500/20 rounded mb-1.5"></div>
                  <div className="h-1.5 w-full bg-white/10 rounded"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )
    }
  ]

  const colorClasses = {
    cyan: {
      badge: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-300',
      glow: 'shadow-[0_0_30px_rgba(34,211,238,0.2)]'
    },
    indigo: {
      badge: 'border-indigo-500/30 bg-indigo-500/10 text-indigo-300',
      glow: 'shadow-[0_0_30px_rgba(99,102,241,0.2)]'
    },
    purple: {
      badge: 'border-purple-500/30 bg-purple-500/10 text-purple-300',
      glow: 'shadow-[0_0_30px_rgba(168,85,247,0.2)]'
    }
  }

  return (
    <section className="pt-32 pb-16 relative overflow-hidden">
      {/* Background gradient orbs */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl"></div>

      <div className="max-w-7xl mx-auto px-6 relative">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center gap-3 sm:gap-4 mb-12 sm:mb-20">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-medium text-white tracking-tight">
            How it works.
          </h2>
          <div className="hidden md:block w-px h-12 bg-gradient-to-b from-transparent via-white/30 to-transparent mx-4"></div>
          <p className="text-base sm:text-lg text-slate-500">Three simple steps to query smarter</p>
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          {steps.map((step, index) => {
            const Icon = step.icon
            const colors = colorClasses[step.color]
            return (
              <div key={step.step} className="group relative">
                {/* Connector Arrow (hidden on mobile and last item) */}
                {index < steps.length - 1 && (
                  <div className="hidden md:flex absolute top-1/3 -right-4 z-10 w-8 items-center justify-center">
                    <ArrowRight className="w-5 h-5 text-white/20" strokeWidth={1.5} />
                  </div>
                )}

                {/* Step Badge */}
                <div className={`inline-flex items-center px-3 sm:px-4 py-1 sm:py-1.5 rounded-full border ${colors.badge} text-xs font-medium mb-4 sm:mb-6 backdrop-blur-sm`}>
                  <span className="mr-2 w-1.5 h-1.5 rounded-full bg-current"></span>
                  STEP {step.step}
                </div>

                {/* Mockup Card */}
                <div className={`rounded-xl sm:rounded-2xl border border-white/5 bg-[#080808]/80 p-4 sm:p-5 mb-4 sm:mb-6 group-hover:border-white/10 transition-all duration-300 ${colors.glow} group-hover:scale-[1.02]`}>
                  {step.mockup}
                </div>

                {/* Content */}
                <h3 className="text-xl sm:text-2xl font-medium text-white mb-2 sm:mb-3 tracking-tight">
                  {step.title}
                </h3>
                <p className="text-sm sm:text-base text-slate-500 leading-relaxed">
                  {step.description}
                </p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default HowItWorks
