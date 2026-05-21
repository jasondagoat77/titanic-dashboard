import { useState, useEffect } from 'react'
import StatCard from './components/StatCard.jsx'
import ChartGrid from './components/ChartGrid.jsx'
import DataTable from './components/DataTable.jsx'
import SurvivalMatrix from './components/SurvivalMatrix.jsx'
import styles from './App.module.css'

const API = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [stats, setStats]     = useState(null)
  const [charts, setCharts]   = useState([])
  const [sample, setSample]   = useState(null)
  const [matrix, setMatrix]   = useState([])
  const [tab, setTab]         = useState('overview')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/stats`).then(r => r.json()),
      fetch(`${API}/api/charts`).then(r => r.json()),
      fetch(`${API}/api/data/sample`).then(r => r.json()),
      fetch(`${API}/api/data/survived-by-class-sex`).then(r => r.json()),
    ]).then(([s, c, d, m]) => {
      setStats(s); setCharts(c); setSample(d); setMatrix(m)
      setLoading(false)
    }).catch(console.error)
  }, [])

  if (loading) return <Loader />

  return (
    <div className={styles.app}>
      {/* ── Header ── */}
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <div className={styles.headerLeft}>
            <span className={styles.tag}>KAGGLE DATASET</span>
            <h1 className={styles.title}>TITANIC<br /><em>SURVIVAL</em></h1>
            <p className={styles.subtitle}>
              Pandas × Matplotlib × Flask × React
            </p>
          </div>
          <div className={styles.headerStats}>
            <Pill label="passengers" value={stats.total_passengers.toLocaleString()} color="cyan" />
            <Pill label="survived"   value={stats.total_survived.toLocaleString()}   color="gold" />
            <Pill label="survival rate" value={`${stats.survival_rate}%`}            color="red"  />
          </div>
        </div>
        <div className={styles.scanline} />
      </header>

      {/* ── Nav ── */}
      <nav className={styles.nav}>
        {['overview','charts','matrix','data'].map(t => (
          <button
            key={t}
            className={`${styles.navBtn} ${tab === t ? styles.navBtnActive : ''}`}
            onClick={() => setTab(t)}
          >
            {t.toUpperCase()}
          </button>
        ))}
      </nav>

      {/* ── Content ── */}
      <main className={styles.main}>
        {tab === 'overview' && <Overview stats={stats} charts={charts} api={API} />}
        {tab === 'charts'   && <ChartGrid charts={charts} api={API} />}
        {tab === 'matrix'   && <SurvivalMatrix matrix={matrix} />}
        {tab === 'data'     && <DataTable data={sample} />}
      </main>

      <footer className={styles.footer}>
        <span>Built with Flask · Pandas · Matplotlib · React · Vite · Docker · Render</span>
        <span className={styles.footerRight}>Titanic Dataset · Kaggle</span>
      </footer>
    </div>
  )
}

/* ── Overview panel ── */
function Overview({ stats, charts, api }) {
  const cards = [
    { label: 'Total Passengers',  value: stats.total_passengers.toLocaleString(), sub: '891 records',              accent: 'cyan'   },
    { label: 'Survived',          value: stats.total_survived.toLocaleString(),   sub: `${stats.survival_rate}%`,  accent: 'gold'   },
    { label: 'Average Age',       value: `${stats.avg_age} yrs`,                  sub: `${stats.missing_age} missing`, accent: 'purple' },
    { label: 'Average Fare',      value: `£${stats.avg_fare}`,                    sub: 'Pounds Sterling',          accent: 'red'    },
  ]

  return (
    <div>
      <section style={{ marginBottom: '2.5rem' }}>
        <SectionLabel>KEY METRICS</SectionLabel>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))', gap:'1rem' }}>
          {cards.map(c => <StatCard key={c.label} {...c} />)}
        </div>
      </section>

      <section style={{ marginBottom: '2.5rem' }}>
        <SectionLabel>CLASS SURVIVAL RATES</SectionLabel>
        <ClassRateBars rates={stats.class_survival_rates} />
      </section>

      <section>
        <SectionLabel>FEATURED CHARTS</SectionLabel>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(420px,1fr))', gap:'1rem' }}>
          {charts.slice(0,2).map(c => (
            <div key={c.id} style={{
              background:'var(--surface)', border:'1px solid var(--border)',
              borderRadius:'8px', overflow:'hidden',
            }}>
              <div style={{ padding:'0.75rem 1rem', borderBottom:'1px solid var(--border)', fontFamily:'var(--font-mono)', fontSize:'0.7rem', color:'var(--muted)', letterSpacing:'0.1em' }}>
                {c.title.toUpperCase()}
              </div>
              <img src={`${api}${c.url}`} alt={c.title} style={{ width:'100%' }} />
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

function ClassRateBars({ rates }) {
  const colors = { 1: 'var(--cyan)', 2: 'var(--gold)', 3: 'var(--red)' }
  const labels = { 1: '1st Class', 2: '2nd Class', 3: '3rd Class' }
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:'0.75rem' }}>
      {Object.entries(rates).map(([cls, rate]) => (
        <div key={cls}>
          <div style={{ display:'flex', justifyContent:'space-between', marginBottom:'0.3rem' }}>
            <span style={{ fontFamily:'var(--font-mono)', fontSize:'0.8rem', color:'var(--muted)' }}>{labels[cls]}</span>
            <span style={{ fontFamily:'var(--font-mono)', fontSize:'0.8rem', color: colors[cls] }}>{rate}%</span>
          </div>
          <div style={{ height:'6px', background:'var(--surface2)', borderRadius:'3px', overflow:'hidden' }}>
            <div style={{
              height:'100%', width:`${rate}%`,
              background: colors[cls],
              borderRadius:'3px',
              transition: 'width 1s ease',
            }} />
          </div>
        </div>
      ))}
    </div>
  )
}

function Pill({ label, value, color }) {
  const c = { cyan:'var(--cyan)', gold:'var(--gold)', red:'var(--red)' }[color]
  return (
    <div style={{
      background:'var(--surface)', border:`1px solid ${c}33`,
      borderRadius:'6px', padding:'0.75rem 1.25rem', textAlign:'right',
    }}>
      <div style={{ fontFamily:'var(--font-display)', fontSize:'2rem', color:c, lineHeight:1 }}>{value}</div>
      <div style={{ fontFamily:'var(--font-mono)', fontSize:'0.65rem', color:'var(--muted)', letterSpacing:'0.1em', textTransform:'uppercase', marginTop:'2px' }}>{label}</div>
    </div>
  )
}

function SectionLabel({ children }) {
  return (
    <div style={{
      fontFamily:'var(--font-mono)', fontSize:'0.65rem', letterSpacing:'0.18em',
      color:'var(--muted)', borderLeft:'2px solid var(--red)', paddingLeft:'0.75rem',
      marginBottom:'1rem',
    }}>
      {children}
    </div>
  )
}

function Loader() {
  return (
    <div style={{
      height:'100vh', display:'flex', flexDirection:'column',
      alignItems:'center', justifyContent:'center', background:'var(--bg)', gap:'1.5rem',
    }}>
      <div style={{ fontFamily:'var(--font-display)', fontSize:'4rem', color:'var(--red)', letterSpacing:'0.1em' }}>TITANIC</div>
      <div style={{
        width:'200px', height:'2px', background:'var(--surface2)',
        borderRadius:'1px', overflow:'hidden',
      }}>
        <div style={{
          height:'100%', background:'var(--cyan)',
          animation:'loadBar 1.4s ease-in-out infinite',
          borderRadius:'1px',
        }} />
      </div>
      <style>{`@keyframes loadBar{0%{width:0;margin-left:0}50%{width:60%;margin-left:20%}100%{width:0;margin-left:100%}}`}</style>
      <span style={{ fontFamily:'var(--font-mono)', fontSize:'0.75rem', color:'var(--muted)', letterSpacing:'0.15em' }}>LOADING DATA…</span>
    </div>
  )
}
