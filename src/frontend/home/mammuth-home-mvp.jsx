import { useState } from "react";

const eventiMock = [
  {
    id: "1",
    titolo: "Festa del Cammeo e dei Borghi",
    data: "Oggi",
    orario: "18:00",
    luogo: "Castello Caetani",
    categoria: "Cultura",
    tag: ["borgo", "artigianato"],
    distanza: "0.3 km",
    gratuito: true,
    descrizione: "Mostra mercato del cammeo con artigiani locali nel borgo medievale.",
    colore: "#70D6FF",
    fomo: [
      { label: "🔴 Ultimi 8 posti", color: "#70D6FF", bg: "#EEF9FF" },
      { label: "⚡ Evento unico dell'anno", color: "#FFB830", bg: "#FFF8EE" },
    ],
    badge: "🧑‍🎨 Gestito da un locale",
    badgeColor: "#B5EAD7",
    walkMin: "4 min a piedi dal parcheggio",
  },
  {
    id: "2",
    titolo: "Degustazione Vini nei Vicoli",
    data: "20 Giu",
    orario: "20:30",
    luogo: "Loggia dei Mercanti",
    categoria: "Enogastronomia",
    tag: ["vino", "DOC"],
    distanza: "0.4 km",
    gratuito: false,
    prezzo: "€12",
    descrizione: "Selezione di vini DOC Pontino con produttori della Provincia di Latina.",
    colore: "#FFB830",
    fomo: [
      { label: "🔴 Solo 3 posti rimasti", color: "#FF6B6B", bg: "#FFF0F0" },
      { label: "🍷 Produttori locali DOC", color: "#FFB830", bg: "#FFF8EE" },
    ],
    badge: "🧑‍🌾 Nativo di Sermoneta",
    badgeColor: "#FFD670",
    walkMin: "2 min a piedi dal parcheggio",
  },
  {
    id: "3",
    titolo: "Concerto di Mezza Estate",
    data: "24 Giu",
    orario: "21:00",
    luogo: "Piazza del Comune",
    categoria: "Musica",
    tag: ["live", "classica"],
    distanza: "0.2 km",
    gratuito: true,
    descrizione: "Orchestra da camera sotto le stelle nel cuore del borgo.",
    colore: "#FF70A6",
    fomo: [
      { label: "⚡ Sold out l'anno scorso", color: "#FF70A6", bg: "#FFF0F6" },
      { label: "🌟 Patrocinio Comune", color: "#B5EAD7", bg: "#EEFAF5" },
    ],
    badge: "🎻 Musicisti locali",
    badgeColor: "#C9B1FF",
    walkMin: "1 min a piedi dal parcheggio",
  },
  {
    id: "4",
    titolo: "Sagra della Zuppa di Farro",
    data: "5 Lug",
    orario: "19:30",
    luogo: "Contrada Valle",
    categoria: "Sagra",
    tag: ["sagra", "farro"],
    distanza: "1.2 km",
    gratuito: false,
    prezzo: "€8",
    descrizione: "Piatto simbolo della tradizione contadina lepina, servito in loco.",
    colore: "#B5EAD7",
    fomo: [
      { label: "🌾 Ricetta segreta dal 1962", color: "#B5EAD7", bg: "#EEFAF5" },
      { label: "👨‍👩‍👧 Evento per famiglie", color: "#70D6FF", bg: "#EEF9FF" },
    ],
    badge: "🧑‍🍳 Contadini locali",
    badgeColor: "#B5EAD7",
    walkMin: "8 min a piedi dal parcheggio",
  },
  {
    id: "5",
    titolo: "Visita Guidata Abbazia di Valvisciolo",
    data: "12 Lug",
    orario: "10:00",
    luogo: "Abbazia di Valvisciolo",
    categoria: "Religioso",
    tag: ["abbazia", "patrimonio"],
    distanza: "3.1 km",
    gratuito: false,
    prezzo: "€5",
    descrizione: "Tour guidato dell'abbazia cistercense del XIII secolo con i monaci.",
    colore: "#C9B1FF",
    fomo: [
      { label: "🔴 Solo 12 posti", color: "#C9B1FF", bg: "#F5EEFF" },
      { label: "⚡ Apertura straordinaria", color: "#FF70A6", bg: "#FFF0F6" },
    ],
    badge: "⛪ Guidato dai monaci",
    badgeColor: "#C9B1FF",
    walkMin: "Auto necessaria · 3.1 km",
  },
];

const FILTRI = [
  { label: "Tutti", emoji: "✦", colore: "#1A1A1E", bg: "#E9FF70" },
  { label: "Borghi", emoji: "🏰", colore: "#1A1A1E", bg: "#70D6FF" },
  { label: "Sapori", emoji: "🍷", colore: "#1A1A1E", bg: "#FFB830" },
  { label: "Musica", emoji: "🎵", colore: "#1A1A1E", bg: "#FF70A6" },
  { label: "Sagre", emoji: "🌾", colore: "#1A1A1E", bg: "#B5EAD7" },
  { label: "Spirituale", emoji: "⛪", colore: "#1A1A1E", bg: "#C9B1FF" },
];

function FomoBadge({ label, color, bg }) {
  return (
    <div style={{
      background: bg, border: `1.5px solid ${color}`,
      borderRadius: "20px", padding: "4px 10px",
      fontSize: 11, fontWeight: 700, color: "#1A1A1E", whiteSpace: "nowrap",
    }}>
      {label}
    </div>
  );
}

function EventCard({ evento, index }) {
  const [pressed, setPressed] = useState(false);
  return (
    <div
      onMouseDown={() => setPressed(true)} onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)} onTouchStart={() => setPressed(true)}
      onTouchEnd={() => setPressed(false)}
      style={{
        background: "#FFFFFF", borderRadius: "20px", overflow: "hidden",
        border: `1.5px solid ${pressed ? evento.colore : "#EDE8E0"}`,
        boxShadow: pressed ? `4px 4px 0px ${evento.colore}` : "3px 3px 0px #D8D4CC",
        transform: pressed ? "translate(2px,2px)" : "translate(0,0)",
        transition: "all 0.1s ease", cursor: "pointer",
        animation: "fadeUp 0.3s ease both",
        animationDelay: `${index * 0.07}s`,
      }}
    >
      <div style={{ height: 4, background: evento.colore, width: "100%" }} />
      <div style={{ padding: "14px 16px 16px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
          <div style={{
            background: evento.colore, color: "#1A1A1E", borderRadius: "8px",
            padding: "4px 12px", fontSize: 11, fontWeight: 800,
            letterSpacing: "0.04em", textTransform: "uppercase",
          }}>
            {evento.categoria}
          </div>
          <div style={{
            background: evento.data === "Oggi" ? "#1A1A1E" : "#F5F3EF",
            color: evento.data === "Oggi" ? "#FFF" : "#888",
            border: `1.5px solid ${evento.data === "Oggi" ? "#1A1A1E" : "#E8E4DC"}`,
            borderRadius: "8px", padding: "3px 10px", fontSize: 11, fontWeight: 700,
          }}>
            {evento.data === "Oggi" ? "🔴 Oggi" : evento.data} · {evento.orario}
          </div>
        </div>
        <div style={{ fontSize: 17, fontWeight: 800, color: "#1A1A1E", lineHeight: 1.25, marginBottom: 6, letterSpacing: "-0.02em" }}>
          {evento.titolo}
        </div>
        <div style={{ fontSize: 13, color: "#888", lineHeight: 1.5, marginBottom: 12 }}>
          {evento.descrizione}
        </div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 12 }}>
          {evento.fomo.map((f, i) => <FomoBadge key={i} {...f} />)}
        </div>
        <div style={{
          display: "inline-flex", alignItems: "center",
          background: evento.badgeColor + "33", border: `1.5px solid ${evento.badgeColor}`,
          borderRadius: "20px", padding: "4px 12px",
          fontSize: 11, fontWeight: 700, color: "#1A1A1E", marginBottom: 12,
        }}>
          {evento.badge}
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
          <div>
            <div style={{ fontSize: 12, color: "#333", fontWeight: 600, marginBottom: 2 }}>📍 {evento.luogo}</div>
            <div style={{ fontSize: 11, color: "#AAA" }}>🚶 {evento.walkMin}</div>
          </div>
          <div style={{
            background: evento.gratuito ? "#B5EAD7" : evento.colore,
            color: "#1A1A1E", borderRadius: "12px", padding: "7px 16px",
            fontSize: 15, fontWeight: 900, boxShadow: `2px 2px 0px ${evento.colore}88`,
          }}>
            {evento.gratuito ? "🎉 FREE" : `Da ${evento.prezzo}`}
          </div>
        </div>
        <div style={{ display: "flex", gap: 6, marginTop: 12, flexWrap: "wrap" }}>
          {evento.tag.map(t => (
            <span key={t} style={{
              background: "#F5F3EF", color: "#999", borderRadius: "6px",
              padding: "2px 8px", fontSize: 10, fontWeight: 500,
            }}>#{t}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [filtro, setFiltro] = useState("Tutti");
  const [cerca, setCerca] = useState("");

  const eventiFiltrati = eventiMock.filter(e => {
    const matchCat = filtro === "Tutti" || e.categoria === filtro ||
      (filtro === "Borghi" && e.categoria === "Cultura") ||
      (filtro === "Sapori" && e.categoria === "Enogastronomia") ||
      (filtro === "Sagre" && e.categoria === "Sagra") ||
      (filtro === "Spirituale" && e.categoria === "Religioso");
    const matchSearch = cerca === "" ||
      e.titolo.toLowerCase().includes(cerca.toLowerCase()) ||
      e.luogo.toLowerCase().includes(cerca.toLowerCase()) ||
      e.tag.some(t => t.includes(cerca.toLowerCase()));
    return matchCat && matchSearch;
  });

  return (
    <div style={{ minHeight: "100vh", background: "#FAF8F5", maxWidth: "430px", margin: "0 auto" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@300;400&display=swap');
        @keyframes fadeUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
        * { box-sizing:border-box; margin:0; padding:0; font-family:'DM Sans',system-ui,sans-serif; }
        ::-webkit-scrollbar{display:none}
        input:focus{outline:none}
        input::placeholder{color:#C8C0B4}
      `}</style>

      {/* HEADER */}
      <div style={{
        position: "sticky", top: 0, zIndex: 10,
        background: "rgba(250,248,245,0.96)", backdropFilter: "blur(16px)",
        padding: "48px 20px 16px", borderBottom: "1.5px solid #EDE8E0",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
          <div>
            {/* Soprattitolo micro-territorio */}
            <div style={{ fontSize: 9, color: "#B8B0A4", fontWeight: 600, letterSpacing: "0.14em", textTransform: "uppercase", marginBottom: 4 }}>
              Borghi · Valli · Sentieri
            </div>
            {/* Logo */}
            <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 5 }}>
              <span style={{ fontSize: 22 }}>🦣</span>
              <div style={{ display: "flex", alignItems: "center" }}>
                <span style={{ fontSize: 20, fontWeight: 300, letterSpacing: "0.16em", color: "#1A1A1E", textTransform: "uppercase" }}>MAMMUTH</span>
                <span style={{ width: 6, height: 6, background: "#E8221A", borderRadius: "50%", margin: "0 3px" }} />
                <span style={{ fontSize: 20, fontWeight: 300, letterSpacing: "0.16em", color: "#1A1A1E", textTransform: "uppercase" }}>EV</span>
              </div>
            </div>
            {/* Divider */}
            <div style={{ height: 1, background: "#D8D4CC", marginBottom: 5 }} />
            {/* Hero tagline — Apple */}
            <div style={{ fontSize: 12, fontWeight: 700, color: "#1A1A1E", letterSpacing: "-0.01em", marginBottom: 2 }}>
              Il territorio come non l'hai mai visto.
            </div>
            {/* Sub tagline — GYG */}
            <div style={{ fontSize: 9, fontFamily: "'DM Mono',monospace", fontWeight: 300, letterSpacing: "0.16em", color: "#B8B0A4", textTransform: "uppercase" }}>
              Where Communities Come Alive™
            </div>
          </div>
          <div style={{
            background: "#E8221A", color: "#FFF",
            borderRadius: "10px", padding: "5px 11px",
            fontSize: 11, fontWeight: 700, marginTop: 20,
          }}>
            {eventiFiltrati.length} eventi
          </div>
        </div>

        {/* Search */}
        <div style={{
          background: "#FFF", border: "1.5px solid #EDE8E0", borderRadius: "13px",
          padding: "10px 16px", display: "flex", alignItems: "center", gap: 8,
          marginBottom: 14, boxShadow: "2px 2px 0 #D8D4CC",
        }}>
          <span style={{ fontSize: 14, color: "#C0BCB4" }}>🔍</span>
          <input
            value={cerca} onChange={e => setCerca(e.target.value)}
            placeholder="Cosa succede oggi intorno a te..."
            style={{ background: "transparent", border: "none", color: "#1A1A1E", fontSize: 14, width: "100%", fontWeight: 400 }}
          />
        </div>

        {/* Filtri — micro-territorio taxonomy */}
        <div style={{ display: "flex", gap: 7, overflowX: "auto", paddingBottom: 2 }}>
          {FILTRI.map(f => {
            const attivo = filtro === f.label;
            return (
              <button key={f.label} onClick={() => setFiltro(f.label)} style={{
                background: attivo ? f.bg : "#FFF",
                border: `1.5px solid ${attivo ? f.bg : "#EDE8E0"}`,
                borderRadius: "20px", padding: "6px 14px",
                fontSize: 11, fontWeight: attivo ? 800 : 500,
                color: attivo ? "#1A1A1E" : "#888",
                cursor: "pointer", whiteSpace: "nowrap",
                transition: "all 0.12s ease",
                display: "flex", alignItems: "center", gap: 4,
              }}>
                {f.emoji} {f.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Lista */}
      <div style={{ padding: "20px 20px 60px", display: "flex", flexDirection: "column", gap: 14 }}>

        {/* Banner urgenza */}
        <div style={{
          display: "flex", alignItems: "center", gap: 8,
          background: "#FFF0F0", border: "1.5px solid #FFB3B3",
          borderRadius: "12px", padding: "10px 14px",
          fontSize: 12, fontWeight: 700, color: "#CC3333",
        }}>
          🔥 Memorie che durano più del weekend — 2 eventi si esauriscono oggi
        </div>

        {/* Section label — GYG style */}
        <div style={{ fontSize: 10, fontFamily: "'DM Mono',monospace", color: "#B8B0A4", fontWeight: 300, letterSpacing: "0.1em", textTransform: "uppercase" }}>
          Quello che i locali amano davvero · {eventiFiltrati.length} esperienze
        </div>

        {eventiFiltrati.length === 0
          ? <div style={{ textAlign: "center", padding: "60px 20px", color: "#C8C0B4", fontSize: 15 }}>
              Nessuna esperienza trovata
            </div>
          : eventiFiltrati.map((e, i) => <EventCard key={e.id} evento={e} index={i} />)
        }
      </div>

      {/* Footer */}
      <div style={{ background: "#1A1A1E", padding: "32px 20px", display: "flex", flexDirection: "column", gap: 20 }}>
        {/* Headline Apple */}
        <div style={{ fontSize: 18, fontWeight: 800, color: "#FFF", letterSpacing: "-0.02em", lineHeight: 1.3 }}>
          Piccoli comuni.<br/>Storie enormi.
        </div>
        {[
          { emoji: "🗺️", titolo: "Vivi il territorio", desc: "Prenota in 30 secondi. Nessun download." },
          { emoji: "🤝", titolo: "100% locale", desc: "Ogni esperienza è verificata da chi ci abita." },
          { emoji: "⚡", titolo: "Real-time spontaneo", desc: "I borghi che meritano il viaggio — oggi." },
        ].map(item => (
          <div key={item.titolo} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
            <span style={{ fontSize: 22 }}>{item.emoji}</span>
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#FFF", marginBottom: 2 }}>{item.titolo}</div>
              <div style={{ fontSize: 12, color: "#5A5A54", lineHeight: 1.5 }}>{item.desc}</div>
            </div>
          </div>
        ))}
        <div style={{ height: 1, background: "#2A2A24" }} />
        {/* Più cercato ora — GYG */}
        <div style={{ fontSize: 10, fontFamily: "'DM Mono',monospace", color: "#4A4A40", letterSpacing: "0.1em", textTransform: "uppercase" }}>
          Più cercato ora: Sagre · Artigianato · Visite guidate
        </div>
        <div style={{ fontSize: 7, fontFamily: "'DM Mono',monospace", color: "#2A2A20", letterSpacing: "0.12em", textTransform: "uppercase", textAlign: "center" }}>
          KREATIO UNIVERSAL SYSTEM™ · CODE 3620 · ATLAS·EVENTA™
        </div>
      </div>
    </div>
  );
}
