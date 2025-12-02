import { FileText, Image, Brain, CheckCircle, BarChart3, Layers } from 'lucide-react'

function Features() {
  const features = [
    {
      icon: Brain,
      title: 'Multi-step Reasoning',
      description: 'Advanced cognitive processing for complex queries across documents.',
      color: 'indigo',
      gradient: 'from-indigo-500/20 to-purple-500/20'
    },
    {
      icon: CheckCircle,
      title: 'Context-Aware Retrieval',
      description: 'Understands document structure, not just keywords.',
      color: 'cyan',
      gradient: 'from-cyan-500/20 to-blue-500/20'
    },
    {
      icon: Layers,
      title: 'Multi-Modal Support',
      description: 'Seamlessly integrate and process text, images, and tables.',
      color: 'purple',
      gradient: 'from-purple-500/20 to-pink-500/20'
    }
  ]

  const colorClasses = {
    indigo: {
      iconBg: 'bg-indigo-500/10 border-indigo-500/30',
      iconColor: 'text-indigo-400',
      glow: 'shadow-[0_0_30px_rgba(99,102,241,0.3)]'
    },
    cyan: {
      iconBg: 'bg-cyan-500/10 border-cyan-500/30',
      iconColor: 'text-cyan-400',
      glow: 'shadow-[0_0_30px_rgba(34,211,238,0.3)]'
    },
    purple: {
      iconBg: 'bg-purple-500/10 border-purple-500/30',
      iconColor: 'text-purple-400',
      glow: 'shadow-[0_0_30px_rgba(168,85,247,0.3)]'
    }
  }

  return (
    <section id="features" className="py-32 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-500/5 rounded-full blur-3xl"></div>
        <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-purple-500/5 rounded-full blur-3xl"></div>
      </div>

      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-indigo-500/20 bg-indigo-500/5 text-sm font-medium text-indigo-300 mb-6">
            <span className="flex h-2 w-2 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.8)]"></span>
            Intelligent Features
          </div>
          <h2 className="text-4xl md:text-5xl font-medium text-white tracking-tight mb-5">
            Intelligent Features
          </h2>
          <p className="text-lg text-slate-500 max-w-2xl mx-auto">
            Powered by cutting-edge AI to understand your documents like never before
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            const colors = colorClasses[feature.color]
            return (
              <div 
                key={index}
                className={`group relative p-8 rounded-2xl border border-white/10 bg-gradient-to-br ${feature.gradient} backdrop-blur-sm hover:border-white/20 transition-all duration-500`}
              >
                {/* Decorative Elements */}
                <div className="absolute top-4 right-4 flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-white/20"></div>
                  <div className="w-1.5 h-1.5 rounded-full bg-white/20"></div>
                  <div className="w-1.5 h-1.5 rounded-full bg-white/20"></div>
                </div>

                {/* Icon with Glow */}
                <div className={`relative w-14 h-14 rounded-xl ${colors.iconBg} border flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 ${colors.glow}`}>
                  <Icon className={`w-7 h-7 ${colors.iconColor}`} strokeWidth={1.5} />
                  {/* Glow effect */}
                  <div className={`absolute inset-0 rounded-xl ${colors.iconBg} blur-xl opacity-50 group-hover:opacity-100 transition-opacity`}></div>
                </div>

                {/* Mockup Bar */}
                <div className="flex items-center gap-3 mb-6 p-3 rounded-lg bg-black/20 border border-white/5">
                  <div className={`w-6 h-6 rounded ${colors.iconBg} flex items-center justify-center`}>
                    <Icon className={`w-3 h-3 ${colors.iconColor}`} strokeWidth={2} />
                  </div>
                  <div className="flex-1 space-y-1.5">
                    <div className="h-2 w-3/4 bg-white/10 rounded"></div>
                    <div className="h-1.5 w-1/2 bg-white/5 rounded"></div>
                  </div>
                </div>

                {/* Content */}
                <h3 className="text-xl text-white font-medium mb-3 tracking-tight">{feature.title}</h3>
                <p className="text-base text-slate-400 leading-relaxed">{feature.description}</p>
              </div>
            )
          })}
        </div>

        {/* Bottom Carousel Dots */}
        <div className="flex justify-center gap-2 mt-12">
          <div className="w-8 h-2 rounded-full bg-indigo-500"></div>
          <div className="w-2 h-2 rounded-full bg-white/20"></div>
          <div className="w-2 h-2 rounded-full bg-white/20"></div>
        </div>
      </div>
    </section>
  )
}

export default Features
