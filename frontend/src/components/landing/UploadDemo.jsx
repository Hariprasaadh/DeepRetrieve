import { useState, useCallback } from 'react'
import { UploadCloud, FileText, X, Loader2, Sparkles, CheckCircle2 } from 'lucide-react'

function UploadDemo() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && (droppedFile.type === 'application/pdf' || droppedFile.type.startsWith('image/'))) {
      setFile(droppedFile)
    }
  }, [])

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
    }
  }

  const handleUpload = async () => {
    if (!file) return
    
    setIsUploading(true)
    // Simulate upload
    await new Promise(resolve => setTimeout(resolve, 2000))
    setIsUploading(false)
    alert('File uploaded successfully! (Demo)')
    setFile(null)
  }

  const removeFile = () => {
    setFile(null)
  }

  const features = [
    'PDF, DOCX, PNG supported',
    'Max 500MB file size',
    'Instant processing'
  ]

  return (
    <section id="upload" className="pt-8 pb-32 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl"></div>

      <div className="max-w-4xl mx-auto px-6 text-center relative">
        {/* Header with badge */}
        <div className="mb-8 sm:mb-12">
          <div className="inline-flex items-center gap-2 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 mb-4 sm:mb-6">
            <Sparkles className="w-3 h-3 sm:w-4 sm:h-4 text-indigo-400" />
            <span className="text-xs sm:text-sm font-medium text-indigo-300">Try It Now</span>
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-medium text-white tracking-tight mb-4 sm:mb-5">Start by dropping a file</h2>
          <p className="text-base sm:text-lg text-slate-500">No setup required. Just drag and drop.</p>
        </div>

        {!file ? (
          <div 
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`relative w-full h-64 sm:h-80 border-2 border-dashed rounded-2xl sm:rounded-3xl transition-all cursor-pointer flex flex-col items-center justify-center group overflow-hidden ${
              isDragging 
                ? 'border-indigo-500/50 bg-indigo-500/10 shadow-[0_0_50px_rgba(99,102,241,0.2)]' 
                : 'border-white/10 bg-[#080808]/50 hover:bg-[#0a0a0a] hover:border-indigo-500/30'
            }`}
          >
            <input 
              type="file" 
              accept=".pdf,.png,.jpg,.jpeg,.docx"
              onChange={handleFileSelect}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />
            
            {/* Background gradient effect */}
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            {/* Animated border glow */}
            <div className={`absolute inset-0 rounded-3xl transition-opacity duration-300 ${isDragging ? 'opacity-100' : 'opacity-0'}`}>
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-indigo-500/20 blur-xl"></div>
            </div>
            
            <div className="relative z-10 flex flex-col items-center pointer-events-none">
              {/* Upload icon with glow */}
              <div className={`w-16 h-16 sm:w-24 sm:h-24 rounded-xl sm:rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 shadow-[0_0_30px_rgba(99,102,241,0.2)] flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform duration-300 ${isDragging ? 'scale-110' : ''}`}>
                <UploadCloud className={`w-7 h-7 sm:w-10 sm:h-10 text-indigo-400 transition-transform ${isDragging ? 'scale-110' : ''}`} strokeWidth={1.5} />
              </div>
              <span className="text-white font-medium text-base sm:text-lg mb-2">Click to upload or drag and drop</span>
              
              {/* Feature pills */}
              <div className="flex flex-wrap justify-center gap-2 mt-4">
                {features.map((feature, i) => (
                  <div key={i} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/5 border border-white/5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-400" />
                    <span className="text-xs text-slate-400">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="w-full p-8 rounded-3xl border border-white/10 bg-gradient-to-b from-[#0a0a0a] to-[#080808] shadow-2xl">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 flex items-center justify-center shadow-[0_0_20px_rgba(99,102,241,0.2)]">
                  <FileText className="w-8 h-8 text-indigo-400" strokeWidth={1.5} />
                </div>
                <div className="text-left">
                  <div className="text-white font-medium text-lg">{file.name}</div>
                  <div className="text-sm text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB • Ready to analyze</div>
                </div>
              </div>
              <button 
                onClick={removeFile}
                className="p-2.5 text-slate-500 hover:text-white hover:bg-white/5 rounded-xl transition-colors border border-transparent hover:border-white/10"
              >
                <X className="w-5 h-5" strokeWidth={1.5} />
              </button>
            </div>
            
            <button 
              onClick={handleUpload}
              disabled={isUploading}
              className="w-full h-14 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-400 hover:to-purple-400 text-white font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-[0_0_30px_rgba(99,102,241,0.3)] hover:shadow-[0_0_40px_rgba(99,102,241,0.4)]"
            >
              {isUploading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" strokeWidth={2} />
                  Processing your document...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Analyze Document
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </section>
  )
}

export default UploadDemo
