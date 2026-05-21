import styles from './StatCard.module.css'

const ACCENT_MAP = {
  cyan:   'var(--cyan)',
  gold:   'var(--gold)',
  red:    'var(--red)',
  purple: 'var(--purple)',
}

export default function StatCard({ label, value, sub, accent = 'cyan' }) {
  const color = ACCENT_MAP[accent] || ACCENT_MAP.cyan
  return (
    <div className={styles.card} style={{ '--accent': color }}>
      <div className={styles.label}>{label}</div>
      <div className={styles.value}>{value}</div>
      {sub && <div className={styles.sub}>{sub}</div>}
      <div className={styles.bar} />
    </div>
  )
}
