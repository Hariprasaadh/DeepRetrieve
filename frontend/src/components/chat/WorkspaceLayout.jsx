import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PanelRightClose, PanelRightOpen } from 'lucide-react';

function WorkspaceLayout({ chatPanel, sourcesPanel }) {
  const [rightOpen, setRightOpen] = useState(true);

  return (
    <div className="flex h-screen w-full bg-[#050505] overflow-hidden text-slate-300 relative">

      {/* Center Panel: Chat Interface */}
      <motion.div
        layout
        className="flex-1 flex flex-col bg-[#050505] relative z-10 min-w-0"
      >
        {chatPanel}
      </motion.div>

      {/* Collapsed Right Trigger - Hidden on mobile */}
      <AnimatePresence>
        {!rightOpen && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="absolute top-1/2 right-0 z-40 hidden md:block"
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

      {/* Right Panel: Sources - Hidden on mobile, 35% on tablet, 25% on desktop */}
      <AnimatePresence initial={false} mode="popLayout">
        {rightOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: "25%", opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="hidden md:flex bg-[#0a0a12]/30 backdrop-blur-sm flex-col relative shrink-0 ml-1 md:w-[35%] lg:w-[25%]"
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
