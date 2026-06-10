'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, useInView } from 'framer-motion';
import { fireEvent, initSectionTracking, trackPlanSelect } from '@/lib/analytics';

const EASE_APPLE  = [0.16, 1, 0.3, 1] as const;
const EASE_SPRING = [0.34, 1.56, 0.64, 1] as const;

const fadeUp = {
  hidden:  { opacity: 0, y: 24 },
  visible: (delay = 0) => ({ opacity: 1, y: 0, transition: { duration: 0.65, ease: EASE_APPLE, delay } }),
};
const staggerGrid = {
  hidden:  {},
  visible: { transition: { staggerChildren: 0.12, delayChildren: 0.05 } },
};
const cardVariant = {
  hidden:  { opacity: 0, y: 28, scale: 0.97 },
  visible: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.7, ease: EASE_APPLE } },
};

function MapViz() {
  const pins = [
    { top:'38%', left:'47%', color:'#8B7CF6', delay:0.5 },
    { top:'55%', left:'31%', color:'#E879A0', delay:0.7 },
    { top:'26%', left:'64%', color:'#34D399', delay:0.9 },
    { top:'63%', left:'59%', color:'#FBBF24', delay:1.1 },
    { top:'44%', left:'20%', color:'#38BDF8', delay:1.3 },
  ];
  return (
    <div className="mt-5 h-32 w-full rounded-xl overflow-hidden relative flex-shrink-0"
         role="img" aria-label="Mappa ATLAS•EVENTA™">
      <div className="absolute inset-0 bg-gradient-to-br from-[#0d0d1a] to-[#12122e]" />
      <div aria-hidden="true" className="absolute inset-0 opacity-[.12]"
           style={{ backgroundImage:'linear-gradient(rgba(139,124,246,.8) .5px,transparent .5px),linear-gradient(90deg,rgba(139,124,246,.8) .5px,transparent .5px)', backgroundSize:'32px 32px' }} />
      {pins.map(({ top, left, color, delay }, i) => (
        <motion.span key={i} aria-hidden="true"
          initial={{ scale:0, opacity:0 }} animate={{ scale:1, opacity:1 }}
          transition={{ delay, duration:0.4, ease:[0.34,1.56,0.64,1] }}
          className="absolute w-2 h-2 rounded-full -translate-x-1/2 -translate-y-1/2"
          style={{ top, left, background:color }} />
      ))}
      <p className="absolute bottom-2 left-0 right-0 text-center text-[9px] tracking-[.12em] uppercase text-white/30 font-medium">ATLAS•EVENTA™ Live Map</p>
    </div>
  );
}

function SafetyViz() {
  const los = [{ id:'A', label:'Libero', pct:95 },{ id:'B', label:'Scorrevole', pct:78 },{ id:'C', label:'Stabile', pct:55 },{ id:'D', label:'Critico', pct:34 }];
  return (
    <div className="mt-auto pt-5 flex flex-col gap-3" role="group" aria-label="Fruin LOS">
      {los.map(({ id, label, pct }, i) => (
        <div key={id}>
          <div className="flex justify-between items-baseline mb-1.5">
            <span className="font-mono text-[10px] font-semibold text-neutral-500 tracking-wide">LOS {id}</span>
            <span className="text-[10px] text-neutral-400">{label}</span>
          </div>
          <div className="h-[3px] w-full rounded-full bg-neutral-100 overflow-hidden">
            <motion.div className="h-full rounded-full"
              initial={{ width:0 }} whileInView={{ width:`${pct}%` }} viewport={{ once:true }}
              transition={{ delay:0.3+i*0.08, duration:0.8, ease:EASE_APPLE }}
              style={{ background:'linear-gradient(90deg,#34D399,#38BDF8)' }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function PipelineViz() {
  const steps = [{ label:'WhatsApp', color:'#34D399', icon:'💬' },{ label:'Twilio', color:'#38BDF8', icon:'📡' },{ label:'Claude', color:'#8B7CF6', icon:'✦' },{ label:'ATLAS', color:'#E879A0', icon:'🗂' }];
  return (
    <div className="mt-5 h-28 rounded-xl bg-gradient-to-r from-neutral-50 to-neutral-100 border border-neutral-200/40 flex items-center justify-center px-5 flex-shrink-0"
         role="img" aria-label="Pipeline TO FILL THE VOID™">
      <div className="flex items-center w-full justify-center">
        {steps.map(({ label, color, icon }, i) => (
          <div key={label} className="flex items-center">
            <motion.div initial={{ opacity:0, x:-8 }} whileInView={{ opacity:1, x:0 }} viewport={{ once:true }}
              transition={{ delay:0.4+i*0.1, duration:0.4, ease:EASE_APPLE }}
              className="flex flex-col items-center gap-1.5">
              <div className="w-9 h-9 rounded-full flex items-center justify-center text-base border"
                   style={{ background:`${color}18`, borderColor:`${color}40` }}>{icon}</div>
              <span className="text-[9px] font-semibold text-neutral-400 tracking-wide">{label}</span>
            </motion.div>
            {i < steps.length-1 && <div className="flex items-center mx-1.5 mb-4 text-neutral-300 text-[10px]">›</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

function CodexViz() {
  const grades = [{ latin:'Peregrinus', level:'I', color:'#8B7CF6' },{ latin:'Explorator Borgi', level:'II', color:'#E879A0' },{ latin:'Custos Traditionis', level:'III', color:'#38BDF8' },{ latin:'Legenda Sermonetae', level:'IV', color:'#34D399' }];
  return (
    <div className="mt-5 grid grid-cols-2 gap-2" role="list" aria-label="Gradi Codex Itineris™">
      {grades.map(({ latin, level, color }, i) => (
        <motion.div key={latin} role="listitem"
          initial={{ opacity:0, scale:0.88 }} whileInView={{ opacity:1, scale:1 }} viewport={{ once:true }}
          transition={{ delay:0.3+i*0.07, duration:0.35, ease:EASE_SPRING }}
          className="flex items-center gap-2 px-2.5 py-2 rounded-xl bg-neutral-50 border border-neutral-100 overflow-hidden">
          <span className="font-mono text-[10px] font-bold flex-shrink-0" style={{ color }}>{level}</span>
          <span className="text-[11px] font-medium text-neutral-800 truncate leading-tight">{latin}</span>
        </motion.div>
      ))}
    </div>
  );
}
function BentoCard({ span = 1, tall = false, children, className = '' }: { span?: 1|2|3; tall?: boolean; children: React.ReactNode; className?: string }) {
  return (
    <motion.article role="listitem" variants={cardVariant}
      whileHover={{ y:-5, scale:1.016, boxShadow:'0 4px 8px rgba(0,0,0,.06),0 20px 56px rgba(0,0,0,.10),0 0 0 .5px rgba(0,0,0,.05)', transition:{ duration:0.2, ease:EASE_SPRING } }}
      className={['relative bg-white rounded-[28px] p-8 flex flex-col overflow-hidden','shadow-[0_2px_4px_rgba(0,0,0,.04),_0_8px_24px_rgba(0,0,0,.06),_0_0_0_.5px_rgba(0,0,0,.05)]','will-change-transform', span===2?'md:col-span-2':'', span===3?'md:col-span-3':'', tall?'md:row-span-2':'', 'min-h-[300px]', className].filter(Boolean).join(' ')}>
      {children}
    </motion.article>
  );
}

function BentoSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once:true, margin:'0px 0px -80px 0px' });
  return (
    <section id="features" ref={ref} data-track-section="Funzionalità" aria-labelledby="bento-title" className="bg-[#F5F5F7] py-28 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <motion.p custom={0} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="text-eyebrow text-[#8B7CF6] mb-3">Funzionalità</motion.p>
          <motion.h2 id="bento-title" custom={0.1} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="text-[clamp(32px,5vw,56px)] font-extrabold tracking-tightest leading-[1.06] text-neutral-950 text-balance mb-4">Ingegneria <span className="text-iri">invisibile.</span></motion.h2>
          <motion.p custom={0.2} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="text-[19px] font-light text-neutral-500 max-w-xl mx-auto text-balance">Ogni modulo costruito su un principio: la cultura locale merita la stessa cura tecnologica dei grandi brand globali.</motion.p>
        </div>
        <motion.div role="list" aria-label="Funzionalità MAMMUTH•EVENTS™" variants={staggerGrid} initial="hidden" animate={inView?'visible':'hidden'} className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <BentoCard span={2}>
            <p className="text-eyebrow text-[#8B7CF6]">ATLAS•EVENTA™</p>
            <h3 className="mt-2 text-[clamp(18px,2vw,24px)] font-bold tracking-tight text-neutral-900 text-balance mb-2">Una mappa viva<br/>di ogni territorio.</h3>
            <p className="text-[14px] text-neutral-500 leading-relaxed text-balance">Ogni borgo, ogni sagra, ogni tradizione — certificata con codice ISTAT e coordinata PostGIS.</p>
            <MapViz />
          </BentoCard>
          <BentoCard tall>
            <p className="text-eyebrow text-[#E879A0]">Safety Engine</p>
            <h3 className="mt-2 text-[clamp(18px,2vw,24px)] font-bold tracking-tight text-neutral-900 text-balance mb-2">Sicuro.<br/>Senza<br/>bloccare.</h3>
            <p className="text-[14px] text-neutral-500 leading-relaxed text-balance">Fruin Level of Service in tempo reale. Output sempre consultivo.</p>
            <SafetyViz />
          </BentoCard>
          <BentoCard>
            <p className="text-eyebrow text-[#34D399]">T.C.F.™</p>
            <h3 className="mt-2 text-[clamp(18px,2vw,24px)] font-bold tracking-tight text-neutral-900 text-balance mb-2">Zero rumore.<br/>Solo verità.</h3>
            <p className="text-[14px] text-neutral-500 leading-relaxed text-balance">Total Coherence Framework: quattro pilastri per la qualità del database.</p>
            <div className="mt-auto pt-4 text-[56px] font-bold tracking-tightest text-neutral-100 text-right leading-none select-none" aria-label="4 pilastri">4×</div>
          </BentoCard>
          <BentoCard span={2}>
            <p className="text-eyebrow text-[#38BDF8]">TO FILL THE VOID™</p>
            <h3 className="mt-2 text-[clamp(18px,2vw,24px)] font-bold tracking-tight text-neutral-900 text-balance mb-2">La notizia arriva da sola.</h3>
            <p className="text-[14px] text-neutral-500 leading-relaxed text-balance">WhatsApp → Twilio → Claude Vision → ATLAS. Una foto diventa un evento certificato in meno di 60 secondi.</p>
            <PipelineViz />
          </BentoCard>
          <BentoCard>
            <p className="text-eyebrow text-[#FBBF24]">Codex Itineris™</p>
            <h3 className="mt-2 text-[clamp(18px,2vw,24px)] font-bold tracking-tight text-neutral-900 text-balance mb-2">Da visitatore<br/>a leggenda.</h3>
            <p className="text-[14px] text-neutral-500 leading-relaxed text-balance">Quattro gradi latini di esplorazione del territorio.</p>
            <CodexViz />
          </BentoCard>
        </motion.div>
      </div>
    </section>
  );
}

const TIERS = [
  { id:'free', name:'Esploratore', desc:'Per chi vuole scoprire il territorio.', priceM:0, priceY:0, accent:'#8B7CF6', featured:false, cta:'Inizia gratis', ctaHref:'#', features:['Mappa interattiva eventi','23+ eventi certificati Sermoneta','Ricerca per comune e categoria','Codex Itineris™ — Grado I'] },
  { id:'pro', name:'Pro', desc:'Per organizzatori e appassionati.', priceM:9, priceY:79, accent:'#FFFFFF', featured:true, cta:'Accesso anticipato', ctaHref:'#', features:['Tutto di Esploratore','Caricamento eventi illimitato','TO FILL THE VOID™ pipeline','API REST 10.000 req/mese','Codex Itineris™ — tutti i gradi','Dashboard organizzatore'] },
  { id:'enterprise', name:'Enterprise', desc:'Per comuni e istituzioni culturali.', priceM:null, priceY:null, accent:'#E879A0', featured:false, cta:'Contattaci', ctaHref:'mailto:mammuth.ev@gmail.com', features:['Tutto di Pro','API illimitate + SLA 99.9%','ATLAS•EVENTA™ white-label','T.C.F.™ audit mensile','Supporto dedicato','GDPR DPA incluso'] },
] as const;

function PricingSection() {
  const [annual, setAnnual] = useState(false);
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once:true, margin:'0px 0px -60px 0px' });
  return (
    <section id="pricing" ref={ref} data-track-section="Pricing" aria-labelledby="pricing-title" className="bg-white py-28 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-14">
          <motion.p custom={0} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="text-eyebrow text-[#8B7CF6] mb-3">Accesso Anticipato</motion.p>
          <motion.h2 id="pricing-title" custom={0.1} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="text-[clamp(32px,5vw,56px)] font-extrabold tracking-tightest leading-[1.06] text-neutral-950 text-balance mb-10">Scegli il tuo <span className="text-iri">livello.</span></motion.h2>
          <motion.div custom={0.2} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="inline-flex items-center gap-3 text-[13px] font-medium text-neutral-500">
            <button onClick={() => setAnnual(false)} className={`transition-colors duration-150 ${!annual?'text-neutral-900':''}`} aria-pressed={!annual}>Mensile</button>
            <button role="switch" aria-checked={annual} onClick={() => setAnnual(v=>!v)} className="relative w-10 h-6 rounded-full cursor-pointer transition-colors duration-200" style={{ background:annual?'#1D1D1F':'#D2D2D4' }} aria-label="Fatturazione annuale">
              <motion.span layout transition={{ type:'spring', stiffness:500, damping:35 }} className="absolute top-[3px] w-[18px] h-[18px] rounded-full bg-white shadow-sm" style={{ left:annual?'calc(100% - 21px)':'3px' }} />
            </button>
            <button onClick={() => setAnnual(true)} className={`transition-colors duration-150 ${annual?'text-neutral-900':''}`} aria-pressed={annual}>
              Annuale
              <motion.span animate={{ opacity:annual?1:0, scale:annual?1:0.8 }} transition={{ duration:0.18 }} className="ml-1.5 inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-[#34D399]/15 text-[#059669]">−30%</motion.span>
            </button>
          </motion.div>
        </div>
        <motion.div variants={staggerGrid} initial="hidden" animate={inView?'visible':'hidden'} role="list" aria-label="Piani MAMMUTH•EVENTS™" className="grid grid-cols-1 md:grid-cols-3 gap-5 items-start">
          {TIERS.map((tier) => {
            const price = tier.priceM===null ? null : annual ? tier.priceY : tier.priceM;
            const isFeatured = tier.featured;
            return (
              <motion.article key={tier.id} role="listitem" variants={cardVariant} aria-selected={isFeatured}
                whileHover={{ y:-5, scale:1.012, transition:{ duration:0.2, ease:EASE_SPRING } }}
                className={['relative flex flex-col rounded-[28px] p-7 overflow-hidden', isFeatured?'bg-[#1D1D1F] text-white shadow-[0_2px_4px_rgba(0,0,0,.12),_0_16px_48px_rgba(0,0,0,.22)]':'bg-[#F5F5F7] text-neutral-900 shadow-apple'].join(' ')}>
                {isFeatured && <div className="absolute top-0 left-0 right-0 h-[2px] rounded-t-[28px]" style={{ background:'linear-gradient(90deg,#8B7CF6,#E879A0,#38BDF8)' }} aria-hidden="true" />}
                <p className={`text-eyebrow mb-2 ${isFeatured?'text-white/50':''}`} style={!isFeatured?{ color:tier.accent }:undefined}>{tier.name}</p>
                <p className={`text-[13px] mb-6 ${isFeatured?'text-white/55':'text-neutral-500'}`}>{tier.desc}</p>
                <div className="mb-7 min-h-[52px] flex flex-col justify-end">
                  <AnimatePresence mode="wait">
                    {tier.priceM===null ? (
                      <motion.p key="label" initial={{ opacity:0, y:6 }} animate={{ opacity:1, y:0 }} exit={{ opacity:0, y:-6 }} transition={{ duration:0.2 }} className={`text-[20px] font-semibold ${isFeatured?'text-white':'text-neutral-900'}`}>Su richiesta</motion.p>
                    ) : (
                      <motion.div key={annual?'annual':'monthly'} initial={{ opacity:0, y:8 }} animate={{ opacity:1, y:0 }} exit={{ opacity:0, y:-8 }} transition={{ duration:0.22 }} className="flex items-baseline gap-1">
                        {price===0 ? <span className={`text-[38px] font-extrabold tracking-tightest leading-none ${isFeatured?'text-white':'text-neutral-900'}`}>Gratis</span> : (<><span className={`text-[13px] self-start mt-1 ${isFeatured?'text-white/55':'text-neutral-400'}`}>€</span><span className={`text-[38px] font-extrabold tracking-tightest leading-none ${isFeatured?'text-white':'text-neutral-900'}`}>{price}</span><span className={`text-[12px] self-end mb-0.5 ${isFeatured?'text-white/45':'text-neutral-400'}`}>/{annual?'anno':'mese'}</span></>)}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
                <motion.a href={tier.ctaHref} whileHover={{ scale:1.02 }} whileTap={{ scale:0.97 }} transition={{ duration:0.15, ease:EASE_SPRING }}
                  onClick={() => { trackPlanSelect(tier.name); fireEvent('cta_click',`CTA Pricing: ${tier.name}`,{ planName:tier.id }); }}
                  className={['flex items-center justify-center gap-2 w-full py-3 rounded-xl mb-7 text-[13px] font-semibold transition-opacity duration-150', isFeatured?'bg-white text-[#1D1D1F] hover:opacity-90':'bg-[#1D1D1F] text-white hover:opacity-85'].join(' ')}
                  aria-label={`${tier.cta} — piano ${tier.name}`}>{tier.cta}</motion.a>
                <div className={`w-full h-px mb-6 ${isFeatured?'bg-white/10':'bg-neutral-200'}`} aria-hidden="true" />
                <ul className="flex flex-col gap-2.5" role="list">
                  {tier.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-[13px]">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" className="mt-[2px] flex-shrink-0" aria-hidden="true"><circle cx="12" cy="12" r="10" fill={isFeatured?'rgba(255,255,255,.10)':`${tier.accent}18`}/><path d="M8 12.5l3 3 5-5" stroke={isFeatured?'#FFFFFF':tier.accent} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/></svg>
                      <span className={isFeatured?'text-white/75':'text-neutral-700'}>{f}</span>
                    </li>
                  ))}
                </ul>
              </motion.article>
            );
          })}
        </motion.div>
        <motion.p custom={0.5} variants={fadeUp} initial="hidden" animate={inView?'visible':'hidden'} className="text-center text-[12px] text-neutral-400 mt-10">Tutti i piani includono GDPR compliance, dati certificati ISTAT e supporto via email.</motion.p>
      </div>
    </section>
  );
}

function NavBar() {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 2);
    window.addEventListener('scroll', onScroll, { passive:true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  return (
    <nav role="navigation" aria-label="Navigazione principale"
      className={['fixed top-0 left-0 right-0 z-50 h-[52px] flex items-center justify-between px-7 transition-[background-color,border-color] duration-[280ms]', scrolled?'bg-white/80 backdrop-blur-[20px] saturate-150 border-b border-neutral-200/60':'bg-transparent border-b border-transparent'].join(' ')}>
      <a href="/" className="text-[13px] font-bold tracking-snug text-neutral-900" aria-label="MAMMUTH EVENTS Home">MAMMUTH<span className="text-iri">•</span>EVENTS™</a>
      <ul className="hidden md:flex items-center list-none" role="list">
        {[{ label:'Funzionalità', href:'#features' },{ label:'Pricing', href:'#pricing' },{ label:'Developer', href:'https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/', ext:true }].map(({ label, href, ext }) => (
          <li key={label}><a href={href} onClick={() => fireEvent('nav_click', label, { label })} className="flex items-center h-[52px] px-[14px] text-[12px] text-neutral-600 hover:text-neutral-900 transition-colors duration-150" {...(ext?{ target:'_blank', rel:'noopener noreferrer' }:{})}>{label}</a></li>
        ))}
      </ul>
      <a href="#pricing" onClick={() => fireEvent('cta_click','Nav CTA',{})} className="text-[12px] text-neutral-600 hover:text-neutral-900 transition-colors duration-150 flex items-center gap-1 group">Esplora
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="transition-transform duration-150 group-hover:translate-x-0.5" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </a>
    </nav>
  );
}

function HeroSection() {
  return (
    <section id="hero" data-track-section="Hero" aria-labelledby="hero-headline" className="relative min-h-screen flex flex-col items-center justify-center text-center px-6 pt-28 pb-20 overflow-hidden bg-white">
      <div aria-hidden="true" className="pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-[60%] -translate-y-[55%] w-[600px] h-[600px] rounded-full opacity-[.13]" style={{ background:'radial-gradient(circle, #8B7CF6, transparent 70%)', filter:'blur(1px)' }} />
        <div className="absolute top-1/2 left-1/2 translate-x-[5%] -translate-y-[40%] w-[450px] h-[450px] rounded-full opacity-[.09]" style={{ background:'radial-gradient(circle, #E879A0, transparent 70%)', filter:'blur(1px)' }} />
      </div>
      <div aria-hidden="true" className="absolute inset-0 opacity-[.04]" style={{ backgroundImage:'linear-gradient(rgba(139,124,246,1) .5px,transparent .5px),linear-gradient(90deg,rgba(139,124,246,1) .5px,transparent .5px)', backgroundSize:'52px 52px' }} />
      <div className="relative z-10 max-w-4xl mx-auto">
        <motion.p custom={0} variants={fadeUp} initial="hidden" animate="visible" className="text-eyebrow text-neutral-400 mb-5">Sermoneta · Provincia di Latina · Lazio</motion.p>
        <motion.h1 id="hero-headline" custom={0.1} variants={fadeUp} initial="hidden" animate="visible" className="text-[clamp(52px,8vw,96px)] font-extrabold tracking-tightest leading-[1.02] text-neutral-950 text-balance mb-5">Radicato.<br/><span className="text-iri">Eterno.</span><br/>Vivo.</motion.h1>
        <motion.p custom={0.22} variants={fadeUp} initial="hidden" animate="visible" className="text-[clamp(17px,2.2vw,22px)] font-light text-neutral-500 max-w-2xl mx-auto text-balance mb-10 leading-relaxed">Il primo database certificato degli eventi culturali del territorio italiano. Borgo per borgo.</motion.p>
        <motion.div custom={0.34} variants={fadeUp} initial="hidden" animate="visible" className="flex flex-wrap items-center justify-center gap-8">
          <motion.a href="#features" onClick={() => fireEvent('cta_click','Hero CTA — Scopri',{ elementId:'hero-cta-primary' })} id="hero-cta-primary" whileHover={{ opacity:0.75 }} whileTap={{ scale:0.97 }} className="text-[17px] font-medium text-[#8B7CF6] flex items-center gap-1.5 group">
            Scopri come funziona
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="transition-transform duration-150 group-hover:translate-x-1" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </motion.a>
          <motion.a href="https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/" target="_blank" rel="noopener noreferrer" onClick={() => fireEvent('cta_click','Hero CTA — Developer',{})} whileHover={{ opacity:0.7 }} className="text-[17px] font-medium text-neutral-500 flex items-center gap-1.5 group">
            Developer Portal
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className="transition-transform duration-150 group-hover:translate-x-1" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </motion.a>
        </motion.div>
      </div>
    </section>
  );
}

function SiteFooter() {
  return (
    <footer role="contentinfo" className="bg-[#F5F5F7] border-t border-neutral-200/60 px-6 py-10">
      <div className="max-w-5xl mx-auto flex flex-col sm:flex-row justify-between items-start gap-8 flex-wrap">
        <div>
          <p className="text-[13px] font-bold text-neutral-900 mb-1">MAMMUTH<span className="text-iri">•</span>EVENTS™</p>
          <p className="text-[11px] text-neutral-400">Where Communities Come Alive™</p>
        </div>
        <div className="flex gap-10 flex-wrap">
          {[{ title:'Prodotto', links:[['Funzionalità','#features'],['Pricing','#pricing']] },{ title:'Developer', links:[['API Docs','https://adrianochtribo-dot.github.io/MAMMUTH-EV/developer/'],['GitHub','https://github.com/adrianochtribo-dot/MAMMUTH-EV']] },{ title:'Legale', links:[['Privacy','#'],['GDPR','#']] }].map(({ title, links }) => (
            <div key={title}>
              <p className="text-eyebrow text-neutral-400 mb-3">{title}</p>
              <ul className="flex flex-col gap-2">{links.map(([label, href]) => <li key={label}><a href={href} className="text-[13px] text-neutral-600 hover:text-neutral-900 transition-colors duration-150">{label}</a></li>)}</ul>
            </div>
          ))}
        </div>
      </div>
      <div className="max-w-5xl mx-auto mt-8 pt-6 border-t border-neutral-200/60 flex flex-col sm:flex-row justify-between gap-2 text-[11px] text-neutral-400">
        <span>Copyright © 2025 KREATIO UNIVERSAL SYSTEM™ — Code 3620. Tutti i diritti riservati.</span>
        <span>Sermoneta · Provincia di Latina · Lazio · Italia</span>
      </div>
    </footer>
  );
}

export default function Page() {
  useEffect(() => {
    const cleanup = initSectionTracking();
    return cleanup;
  }, []);
  return (
    <main>
      <NavBar />
      <HeroSection />
      <BentoSection />
      <PricingSection />
      <SiteFooter />
    </main>
  );
}
