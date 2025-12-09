import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SidebarClose, SidebarOpen, PanelRightClose, PanelRightOpen } from 'lucide-react';

function WorkspaceLayout({ pdfPanel, chatPanel, sourcesPanel }) {
  const [leftOpen, setLeftOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(true);

  return (
    <div className="flex h-screen w-full bg-[#050505] overflow-hidden text-slate-300 relative">

      {/* Left Panel: PDF Viewer */}
      <AnimatePresence initial={false} mode="popLayout">
        {leftOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: "30%", opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="bg-[#0a0a12]/30 backdrop-blur-sm flex flex-col relative shrink-0 mr-1"
          >
            <div className="flex-1 overflow-hidden min-w-[300px]">
              {pdfPanel}
            </div>

            {/* Collapse Trigger (Inside panel) */}
            <button
              onClick={() => setLeftOpen(false)}
              className="absolute top-1/2 -right-3 translate-x-0 z-50 w-6 h-12 bg-[#1a1a23] rounded-r-lg flex items-center justify-center text-slate-500 hover:text-white hover:bg-indigo-500/20 transition-all cursor-pointer shadow-xl border border-white/5"
              title="Collapse PDF Panel"
            >
              <SidebarClose className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Collapsed Left Trigger */}
      <AnimatePresence>
        {!leftOpen && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="absolute top-1/2 left-0 z-40"
          >
            <button
              onClick={() => setLeftOpen(true)}
              className="w-8 h-12 bg-[#1a1a23] border border-white/5 border-l-0 rounded-r-lg flex items-center justify-center text-slate-500 hover:text-indigo-400 hover:bg-indigo-500/10 transition-all shadow-xl"
              title="Expand PDF Panel"
            >
              <SidebarOpen className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Center Panel: Chat Interface */}
      <motion.div
        layout
        className="flex-1 flex flex-col bg-[#050505] relative z-10 min-w-0"
      >
        {chatPanel}
      </motion.div>

      {/* Collapsed Right Trigger */}
      <AnimatePresence>
        {!rightOpen && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="absolute top-1/2 right-0 z-40"
          >
            <button
              onClick={() => setRightOpen(true)}
              className="w-8 h-12 bg-[#1a1a23] border border-white/5 border-r-0 rounded-l-lg flex items-center justify-center text-slate-500 hover:text-indigo-400 hover:bg-indigo-500/10 transition-all shadow-xl"
              title="Expand Sources Panel"
            >
              <PanelRightOpen className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Right Panel: Sources */}
      <AnimatePresence initial={false} mode="popLayout">
        {rightOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: "25%", opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="bg-[#0a0a12]/30 backdrop-blur-sm flex flex-col relative shrink-0 ml-1"
          >
            {/* Collapse Trigger (Inside panel) */}
            <button
              onClick={() => setRightOpen(false)}
              className="absolute top-1/2 -left-6 translate-x-3 z-50 w-6 h-12 bg-[#1a1a23] rounded-l-lg flex items-center justify-center text-slate-500 hover:text-white hover:bg-indigo-500/20 transition-all cursor-pointer shadow-xl border border-white/5"
              title="Collapse Sources Panel"
            >
              <PanelRightClose className="w-4 h-4" />
            </button>

            <div className="flex-1 overflow-hidden min-w-[250px]">
              {sourcesPanel}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default WorkspaceLayout;
