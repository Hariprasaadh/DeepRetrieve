import { Check, X, Zap, Database, Image, Table2, Brain, Search, Sparkles } from 'lucide-react'

function Comparison() {
  const features = [
    {
      feature: 'Text extraction & chunking',
      deepRetrieve: true,
      simpleRag: true,
      icon: Search
    },
    {
      feature: 'Image understanding (CLIP)',
      deepRetrieve: true,
      simpleRag: false,
      icon: Image
    },
    {
      feature: 'Table extraction (Camelot)',
      deepRetrieve: true,
      simpleRag: false,
      icon: Table2
    },
    {
      feature: 'Binary Quantization (10x less storage)',
      deepRetrieve: true,
      simpleRag: false,
      icon: Database
    },
    {
      feature: 'Multimodal LLM context',
      deepRetrieve: true,
      simpleRag: false,
      icon: Brain
    },
    {
      feature: 'Visual reasoning on charts',
      deepRetrieve: true,
      simpleRag: false,
      icon: Zap
    }
  ]

  const stats = [
    {
      value: '10x',
      label: 'Less storage with Binary Quantization',
      color: 'indigo'
    },
    {
      value: '3',
      label: 'Content types indexed (text, image, table)',
      color: 'purple'
    },
    {
      value: '512D',
      label: 'CLIP embeddings for semantic search',
      color: 'cyan'
    }
  ]

  const colorClasses = {
    indigo: 'from-indigo-500/20 to-indigo-500/5 border-indigo-500/20 shadow-[0_0_30px_rgba(99,102,241,0.15)]',
    purple: 'from-purple-500/20 to-purple-500/5 border-purple-500/20 shadow-[0_0_30px_rgba(168,85,247,0.15)]',
    cyan: 'from-cyan-500/20 to-cyan-500/5 border-cyan-500/20 shadow-[0_0_30px_rgba(34,211,238,0.15)]'
  }

  return (
    <section className="py-16 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-500/5 rounded-full blur-3xl"></div>
      
      <div className="max-w-5xl mx-auto px-6 relative">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 mb-6">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="text-sm font-medium text-indigo-300">Feature Comparison</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-medium text-white tracking-tight mb-5">
            Why DeepRetrieve?
          </h2>
          <p className="text-lg text-slate-500 max-w-2xl mx-auto">
            Most RAG systems only understand text. DeepRetrieve sees the full picture — 
            text, images, tables, and charts.
          </p>
        </div>

        {/* Comparison Table */}
        <div className="rounded-2xl border border-white/10 overflow-hidden bg-gradient-to-b from-[#0a0a0a] to-[#080808] shadow-2xl overflow-x-auto">
          {/* Table Header */}
          <div className="grid grid-cols-3 gap-2 sm:gap-4 p-4 sm:p-6 bg-gradient-to-r from-[#0c0c0c] via-[#0a0a0a] to-[#0c0c0c] border-b border-white/5 min-w-[500px] sm:min-w-0">
            <div className="text-xs sm:text-sm font-medium text-slate-400 flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-slate-400 hidden sm:block"></div>
              Feature
            </div>
            <div className="text-center">
              <div className="inline-flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 rounded-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 shadow-[0_0_20px_rgba(99,102,241,0.2)]">
                <div className="w-1.5 sm:w-2 h-1.5 sm:h-2 rounded-full bg-indigo-400 shadow-[0_0_8px_rgba(129,140,248,1)] animate-pulse"></div>
                <span className="text-xs sm:text-sm font-medium text-indigo-200">DeepRetrieve</span>
              </div>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 rounded-full bg-white/5 border border-white/10">
                <span className="text-xs sm:text-sm font-medium text-slate-500">Simple RAG</span>
              </div>
            </div>
          </div>

          {/* Table Body */}
          <div className="divide-y divide-white/5">
            {features.map((item, index) => {
              const Icon = item.icon
              return (
                <div 
                  key={index} 
                  className="grid grid-cols-3 gap-2 sm:gap-4 p-4 sm:p-6 hover:bg-white/[0.02] transition-all duration-200 group min-w-[500px] sm:min-w-0"
                >
                  <div className="flex items-center gap-2 sm:gap-3">
                    <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-lg sm:rounded-xl bg-gradient-to-br from-white/10 to-white/5 flex items-center justify-center text-slate-400 group-hover:text-indigo-400 group-hover:from-indigo-500/20 group-hover:to-purple-500/10 transition-all duration-200 border border-white/5 group-hover:border-indigo-500/20 shrink-0">
                      <Icon className="w-3 h-3 sm:w-4 sm:h-4" strokeWidth={1.5} />
                    </div>
                    <span className="text-xs sm:text-sm text-slate-300 group-hover:text-white transition-colors">{item.feature}</span>
                  </div>
                  <div className="flex justify-center items-center">
                    {item.deepRetrieve ? (
                      <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-gradient-to-br from-green-500/20 to-green-500/5 border border-green-500/30 flex items-center justify-center shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                        <Check className="w-3 h-3 sm:w-4 sm:h-4 text-green-400" strokeWidth={2.5} />
                      </div>
                    ) : (
                      <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center">
                        <X className="w-3 h-3 sm:w-4 sm:h-4 text-red-400/70" strokeWidth={2} />
                      </div>
                    )}
                  </div>
                  <div className="flex justify-center items-center">
                    {item.simpleRag ? (
                      <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-green-500/10 border border-green-500/20 flex items-center justify-center">
                        <Check className="w-3 h-3 sm:w-4 sm:h-4 text-green-400/70" strokeWidth={2} />
                      </div>
                    ) : (
                      <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center opacity-50">
                        <X className="w-3 h-3 sm:w-4 sm:h-4 text-red-400" strokeWidth={2} />
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          {stats.map((stat, index) => (
            <div 
              key={index}
              className={`relative p-8 rounded-2xl border bg-gradient-to-b ${colorClasses[stat.color]} text-center group hover:scale-[1.02] transition-all duration-300 overflow-hidden`}
            >
              {/* Decorative glow */}
              <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-20 h-20 bg-current opacity-20 rounded-full blur-2xl"></div>
              
              {/* Decorative corner dots */}
              <div className="absolute top-4 right-4 flex gap-1">
                <div className="w-1 h-1 rounded-full bg-white/20"></div>
                <div className="w-1 h-1 rounded-full bg-white/10"></div>
              </div>

              <div className="relative">
                <div className="text-5xl font-semibold text-white mb-3 tracking-tight">{stat.value}</div>
                <div className="text-sm text-slate-400 leading-relaxed">{stat.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Comparison
