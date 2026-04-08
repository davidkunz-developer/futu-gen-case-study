import React, { useState, useEffect, useRef } from 'react';
import { 
  Mic, Play, Square, LayoutDashboard, 
  MessageSquare, Shield, Activity, 
  Wifi, WifiOff, Users, Clock, AlertCircle, Upload, Database
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// ── Components ──
function SourceButton({ icon, label, onClick, disabled, active }: { 
  icon: React.ReactNode, 
  label: string, 
  onClick: () => void, 
  disabled?: boolean,
  active?: boolean 
}) {
  return (
    <motion.button
      whileHover={disabled ? {} : { scale: 1.02, backgroundColor: 'rgba(255,255,255,0.05)' }}
      whileTap={disabled ? {} : { scale: 0.98 }}
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "flex flex-col items-center justify-center gap-2 p-4 rounded-xl border transition-all",
        disabled ? "opacity-30 cursor-not-allowed bg-transparent border-white/5" : "bg-black/20 border-white/10 hover:border-accent/40 text-slate-300",
        active && "border-accent bg-accent/5 text-accent"
      )}
    >
      <div className={cn("p-2 rounded-lg bg-white/5", active && "bg-accent/10")}>
        {icon}
      </div>
      <span className="text-[10px] font-bold uppercase tracking-wider">{label}</span>
    </motion.button>
  );
}

// ── Types ──
interface TranscriptionRecord {
  chunk_id: string;
  speaker_id: string;
  text: string;
  timestamp_start: number;
  timestamp_end: number;
}

interface Classification {
  classification: 'private' | 'topic_based';
  confidence: number;
  topics: string[];
  dominant_topic: string;
  sentiment: string;
  participants_count: number;
}

// ── Configuration ──
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://127.0.0.1:8000' 
  : '';
axios.defaults.baseURL = API_BASE;

export default function App() {
  const [messages, setMessages] = useState<TranscriptionRecord[]>([]);
  const [classification, setClassification] = useState<Classification | null>(null);
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'connecting'>('connecting');
  const [isRecording, setIsRecording] = useState(false);
  
  const ws = useRef<WebSocket | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    connectWS();
    return () => ws.current?.close();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const connectWS = () => {
    setStatus('connecting');
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname === 'localhost' ? '127.0.0.1:8000' : window.location.host;
    const socket = new WebSocket(`${protocol}//${host}/ws/stream`);

    socket.onopen = () => setStatus('connected');
    socket.onclose = () => {
      setStatus('disconnected');
      setTimeout(connectWS, 3000);
    };
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.classification) {
        setClassification(data);
      } else if (data.text) {
        setMessages(prev => {
          if (prev.some(m => m.chunk_id === data.chunk_id)) return prev;
          return [...prev, data];
        });
      }
    };

    ws.current = socket;
  };

  const startMic = async () => {
    try {
      await axios.post('/api/start/mic');
      setIsRecording(true);
      setMessages([]);
      setClassification(null);
    } catch (err) {
      console.error("Failed to start mic", err);
    }
  };

  const startMock = async () => {
    try {
      await axios.post('/api/start/mock');
      setIsRecording(true);
      setMessages([]);
      setClassification(null);
    } catch (err) {
       console.error("Failed to start mock", err);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('/api/start/upload', formData);
      setIsRecording(true);
      setMessages([]);
      setClassification(null);
    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  const loadDemoMockData = () => {
    setMessages([
      { chunk_id: 'demo-1', speaker_id: 'S1', text: 'Dobrý den, vítám vás u dnešního dema našeho systému FutuGen.', timestamp_start: 0, timestamp_end: 2.5 },
      { chunk_id: 'demo-2', speaker_id: 'S1', text: 'Tento systém v reálném čase přepisuje audio a analyzuje obsah hovoru.', timestamp_start: 2.5, timestamp_end: 5.5 },
      { chunk_id: 'demo-3', speaker_id: 'S2', text: 'To vypadá skvěle, jakou používáte latenci?', timestamp_start: 5.5, timestamp_end: 7.8 },
      { chunk_id: 'demo-4', speaker_id: 'S1', text: 'Díky Deepgram Nova-2 se pohybujeme pod jednu sekundu.', timestamp_start: 7.8, timestamp_end: 11.2 },
    ]);
    setClassification({
      classification: 'topic_based',
      confidence: 0.98,
      topics: ['technologie', 'demo', 'latence'],
      dominant_topic: 'Product demonstration',
      sentiment: 'positive',
      participants_count: 2
    });
  };

  const stop = async () => {
    try {
      await axios.post('/api/stop');
      setIsRecording(false);
    } catch (err) {
      console.error("Failed to stop", err);
    }
  };

  const speakerColors: Record<string, string> = {
    'S1': 'text-blue-400 bg-blue-400/10 border-blue-400/30',
    'S2': 'text-red-400 bg-red-400/10 border-red-400/30',
    'S3': 'text-emerald-400 bg-emerald-400/10 border-emerald-400/30',
    'S4': 'text-amber-400 bg-amber-400/10 border-amber-400/30',
  };

  return (
    <div className="min-h-screen flex flex-col bg-bg selection:bg-accent/30">
      <header className="px-8 py-5 border-b border-white/5 flex items-center justify-between sticky top-0 bg-bg/80 backdrop-blur-md z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-violet-600 flex items-center justify-center shadow-lg shadow-accent/20">
            <Activity className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">FutuGen <span className="text-accent">Live</span></h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Autonomous Intelligence</p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className={cn(
            "flex items-center gap-2 px-3 py-1.5 rounded-full border text-[11px] font-mono transition-all duration-500",
            status === 'connected' ? "bg-success/10 border-success/20 text-success" : "bg-danger/10 border-danger/20 text-danger"
          )}>
            {status === 'connected' ? <Wifi className="w-3 h-3" /> : <WifiOff className="w-3 h-3 animate-pulse" />}
            {status.toUpperCase()}
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-8 grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-8">
        <section className="flex flex-col gap-6 overflow-hidden">
          <div className="glass p-6">
             <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                   <div className={cn(
                     "w-2 h-2 rounded-full",
                     isRecording ? "bg-danger animate-pulse shadow-[0_0_8px_rgba(248,113,113,0.8)]" : "bg-slate-600"
                   )} />
                   <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                     {isRecording ? "Live Analysis in Progress" : "Select Input Source"}
                   </span>
                </div>
                {isRecording && (
                  <motion.button
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    onClick={stop}
                    className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-danger/10 border border-danger/30 text-danger text-[11px] font-bold hover:bg-danger/20 transition-all uppercase tracking-tight"
                  >
                    <Square className="w-3 h-3 fill-current" />
                    Terminate
                  </motion.button>
                )}
             </div>

             <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <input 
                  type="file" 
                  accept=".wav" 
                  className="hidden" 
                  ref={fileInputRef} 
                  onChange={handleFileUpload} 
                />
                
                <SourceButton 
                  icon={<Mic className="w-4 h-4" />} 
                  label="Microphone" 
                  active={false} 
                  onClick={startMic}
                  disabled={isRecording}
                />
                <SourceButton 
                  icon={<Upload className="w-4 h-4" />} 
                  label="WAV File" 
                  active={false} 
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isRecording}
                />
                <SourceButton 
                  icon={<Play className="w-4 h-4" />} 
                  label="Mock Stream" 
                  active={false} 
                  onClick={startMock}
                  disabled={isRecording}
                />
                <SourceButton 
                  icon={<Database className="w-4 h-4" />} 
                  label="Demo Data" 
                  active={false} 
                  onClick={loadDemoMockData}
                  disabled={isRecording}
                />
             </div>
          </div>

          <div className="glass flex-1 flex flex-col overflow-hidden">
             <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-2">
                   <MessageSquare className="w-4 h-4 text-accent" />
                   <span className="text-sm font-bold">Transcription Feed</span>
                </div>
                <span className="text-[11px] font-mono text-slate-500 bg-white/5 px-2 py-1 rounded-md">
                   {messages.length} chunks processed
                </span>
             </div>

             <div 
               ref={scrollRef}
               className="flex-1 overflow-y-auto p-6 flex flex-col gap-4 scroll-smooth"
             >
                <AnimatePresence initial={false}>
                  {messages.length === 0 && !isRecording && (
                    <motion.div 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex flex-col items-center justify-center h-full gap-4 text-slate-500 py-20"
                    >
                       <LayoutDashboard className="w-12 h-12 opacity-20" />
                       <p className="text-sm font-medium">System idle. Start a stream or load demo data.</p>
                    </motion.div>
                  )}
                  {messages.map((m, i) => (
                    <motion.div
                      key={m.chunk_id + i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="flex items-start gap-4"
                    >
                       <div className={cn(
                         "shrink-0 px-3 py-1 rounded-lg border text-[10px] font-bold font-mono mt-1 w-12 text-center",
                         speakerColors[m.speaker_id] || "text-slate-400 bg-slate-400/10 border-slate-400/30"
                       )}>
                          {m.speaker_id}
                       </div>
                       <div className="flex-1">
                          <p className="text-[15px] leading-relaxed text-slate-200">
                             {m.text}
                          </p>
                          <div className="flex items-center gap-4 mt-2">
                             <div className="flex items-center gap-1 text-[10px] font-mono text-slate-500">
                                <Clock className="w-3 h-3" />
                                {m.timestamp_start.toFixed(1)}s → {m.timestamp_end.toFixed(1)}s
                             </div>
                          </div>
                       </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
             </div>
          </div>
        </section>

        <aside className="flex flex-col gap-6">
           <div className="glass p-6 overflow-hidden relative">
              <div className="absolute top-0 right-0 p-4 opacity-5">
                 <Shield className="w-24 h-24" />
              </div>
              <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-5">AI Classification</h3>
              
              {!classification ? (
                <div className="py-10 flex flex-col items-center gap-3 text-slate-600">
                   <Activity className="w-10 h-10 animate-pulse-slow" />
                   <p className="text-[11px] font-bold">Waiting for processing...</p>
                </div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex flex-col gap-4"
                >
                   <div className={cn(
                     "px-4 py-3 rounded-xl border-2 text-center font-black tracking-tight",
                     classification.classification === 'private' 
                       ? "bg-danger/20 border-danger/40 text-danger shadow-lg shadow-danger/10" 
                       : "bg-success/20 border-success/40 text-success shadow-lg shadow-success/10"
                   )}>
                      {classification.classification === 'private' ? 'PRIVATE' : 'TOPIC-BASED'}
                   </div>
                   
                   <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white/5 p-3 rounded-lg border border-white/5">
                         <span className="block text-[10px] text-slate-500 font-bold uppercase mb-1">Confidence</span>
                         <span className="text-sm font-mono font-bold text-accent">{(classification.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <div className="bg-white/5 p-3 rounded-lg border border-white/5">
                         <span className="block text-[10px] text-slate-500 font-bold uppercase mb-1">Users</span>
                         <div className="flex items-center gap-1.5 text-sm font-bold">
                            <Users className="w-3.5 h-3.5" />
                            {classification.participants_count}
                         </div>
                      </div>
                   </div>

                   <div>
                      <span className="block text-[10px] text-slate-500 font-bold uppercase mb-3 px-1">Detected Topics</span>
                      <div className="flex flex-wrap gap-2">
                         {classification.topics.map(t => (
                           <span key={t} className="px-2.5 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-[11px] font-bold">
                              {t}
                           </span>
                         ))}
                      </div>
                   </div>

                   <div className="mt-2 pt-4 border-t border-white/5">
                       <span className="block text-[10px] text-slate-500 font-bold uppercase mb-1 px-1">Dominant Focus</span>
                       <p className="text-xs font-medium text-slate-300 italic px-1">"{classification.dominant_topic}"</p>
                   </div>
                </motion.div>
              )}
           </div>

           <div className="glass p-6 bg-gradient-to-br from-surface to-accent/5">
              <div className="flex items-center gap-2 mb-4">
                 <AlertCircle className="w-4 h-4 text-slate-400" />
                 <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Live Insights</h3>
              </div>
              <p className="text-xs leading-relaxed text-slate-400">
                System powered by <strong>Deepgram Nova-2</strong> for sub-second latency and 
                <strong>GPT-4o-mini</strong> for real-time semantic analysis.
              </p>
           </div>
        </aside>
      </main>

      <footer className="footer px-8 py-4 border-t border-white/5 text-[10px] font-mono text-slate-600 flex justify-between items-center bg-black/10">
         <span>&copy; 2026 INFINITY SOLUTIONS / FUTUGEN CORE</span>
         <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
               <div className="w-1.5 h-1.5 rounded-full bg-success" />
               SYSTEM OPERATIONAL
            </div>
            <span>V2.5.0-PRO</span>
         </div>
      </footer>
    </div>
  );
}
