import { useState } from 'react'
import styles from './DataTable.module.css'

export default function DataTable({ data }) {
  const [page, setPage] = useState(0)
  if (!data) return null

  const { columns, rows, total_rows } = data
  const perPage = 10
  const pages   = Math.ceil(rows.length / perPage)
  const visible = rows.slice(page * perPage, page * perPage + perPage)

  const formatVal = (col, val) => {
    if (val === null || val === undefined) return <span className={styles.null}>—</span>
    if (col === 'Survived') return (
      <span className={styles.badge} style={{ background: val ? '#4cc9f020' : '#e6394620', color: val ? 'var(--cyan)' : 'var(--red)', borderColor: val ? 'var(--cyan)' : 'var(--red)' }}>
        {val ? '✓ YES' : '✗ NO'}
      </span>
    )
    if (col === 'Pclass') return `Class ${val}`
    if (col === 'Fare')   return typeof val === 'number' ? `£${val.toFixed(2)}` : val
    if (col === 'Age')    return typeof val === 'number' ? val.toFixed(1) : val
    return String(val)
  }

  return (
    <div>
      <div className={styles.header}>
        <div>
          <h2 className={styles.heading}>Raw Dataset</h2>
          <p className={styles.desc}>
            Showing {rows.length} of {total_rows} records · Titanic passenger manifest
          </p>
        </div>
        <div className={styles.pagination}>
          <button className={styles.pgBtn} disabled={page === 0} onClick={() => setPage(p => p - 1)}>← PREV</button>
          <span className={styles.pgInfo}>{page + 1} / {pages}</span>
          <button className={styles.pgBtn} disabled={page >= pages - 1} onClick={() => setPage(p => p + 1)}>NEXT →</button>
        </div>
      </div>

      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <thead>
            <tr>
              {columns.map(col => (
                <th key={col} className={styles.th}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visible.map((row, i) => (
              <tr key={i} className={styles.tr}>
                {row.map((val, j) => (
                  <td key={j} className={styles.td}>
                    {formatVal(columns[j], val)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className={styles.footer}>
        <span>Source: Kaggle · Titanic: Machine Learning from Disaster</span>
        <span style={{ color:'var(--red)' }}>891 rows × 9 columns</span>
      </div>
    </div>
  )
}
