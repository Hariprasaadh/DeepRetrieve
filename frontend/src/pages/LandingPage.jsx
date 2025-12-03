import { Navbar, Hero, AppMockup, Features, HowItWorks, Comparison, UploadDemo, Footer, ParticleBackground } from '../components/landing'

function LandingPage() {
  return (
    <div className="min-h-screen bg-[#050505] text-slate-400 antialiased overflow-x-hidden selection:bg-indigo-500/30 selection:text-indigo-200">
      <ParticleBackground />
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative pt-36 pb-20 px-6 overflow-hidden min-h-screen flex flex-col items-center">
        {/* Background Elements */}
        <div className="absolute inset-0 grid-bg -z-10 h-[800px]"></div>
        
        <Hero />
        <AppMockup />
      </section>

      <HowItWorks />
      <Comparison />
      <Features />
      <UploadDemo />
      <Footer />
    </div>
  )
}

export default LandingPage
