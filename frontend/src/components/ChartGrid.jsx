import { useState } from 'react'
import styles from './ChartGrid.module.css'

export default function ChartGrid({ charts, api }) {
  const [active, setActive] = useState(null)

  return (
    <>
      <div className={styles.grid}>
        {charts.map(c => (
          <div
            key={c.id}
            className={styles.card}
            onClick={() => setActive(c)}
          >
            <div className={styles.cardHeader}>
              <span className={styles.cardTitle}>{c.title.toUpperCase()}</span>
              <span className={styles.zoom}>⤢ EXPAND</span>
            </div>
            <img
              src={`${api}${c.url}`}
              alt={c.title}
              className={styles.img}
              loading="lazy"
            />
          </div>
        ))}
      </div>

      {active && (
        <div className={styles.lightbox} onClick={() => setActive(null)}>
          <div className={styles.lightboxInner} onClick={e => e.stopPropagation()}>
            <button className={styles.close} onClick={() => setActive(null)}>✕</button>
            <div className={styles.lightboxTitle}>{active.title.toUpperCase()}</div>
            <img src={`${api}${active.url}`} alt={active.title} style={{ width:'100%', borderRadius:'4px' }} />
          </div>
        </div>
      )}
    </>
  )
}
