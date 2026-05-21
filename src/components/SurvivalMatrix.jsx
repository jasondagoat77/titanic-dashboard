import styles from './SurvivalMatrix.module.css'

export default function SurvivalMatrix({ matrix }) {
  const classes = [1, 2, 3]
  const sexes   = ['female', 'male']
  const classLabels = { 1:'1st Class', 2:'2nd Class', 3:'3rd Class' }

  const getCell = (cls, sex) =>
    matrix.find(r => r.class === cls && r.sex === sex) || {}

  const maxRate = Math.max(...matrix.map(r => r.rate || 0))

  return (
    <div>
      <div className={styles.intro}>
        <h2 className={styles.heading}>Survival Matrix</h2>
        <p className={styles.desc}>
          Cross-tabulation of survival rates by passenger class and gender.
          Cell colour intensity reflects relative survival probability.
        </p>
      </div>

      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th className={styles.th}>Class / Gender</th>
              {sexes.map(s => (
                <th key={s} className={styles.th}>{s.toUpperCase()}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {classes.map(cls => (
              <tr key={cls}>
                <td className={styles.rowLabel}>{classLabels[cls]}</td>
                {sexes.map(sex => {
                  const cell = getCell(cls, sex)
                  const rate   = cell.rate    || 0
                  const surv   = cell.survived || 0
                  const total  = cell.total    || 0
                  const norm   = maxRate > 0 ? rate / maxRate : 0
                  const isSex  = sex === 'female'
                  const bg = isSex
                    ? `rgba(76,201,240,${norm * 0.5})`
                    : `rgba(230,57,70,${norm * 0.5})`
                  const border = isSex ? 'var(--cyan)' : 'var(--red)'

                  return (
                    <td key={sex} className={styles.cell}>
                      <div
                        className={styles.cellInner}
                        style={{ background: bg, borderColor: border }}
                      >
                        <div
                          className={styles.rate}
                          style={{ color: isSex ? 'var(--cyan)' : 'var(--red)' }}
                        >
                          {rate.toFixed(1)}%
                        </div>
                        <div className={styles.meta}>
                          {surv}/{total} survived
                        </div>
                        <div className={styles.barWrap}>
                          <div
                            className={styles.barFill}
                            style={{
                              width: `${rate}%`,
                              background: isSex ? 'var(--cyan)' : 'var(--red)',
                            }}
                          />
                        </div>
                      </div>
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className={styles.insights}>
        <InsightCard
          color="cyan"
          title="Women & Children First"
          text="First-class women had nearly 97% survival rate — the highest of any group. Gender was the strongest single predictor."
        />
        <InsightCard
          color="gold"
          title="Class Privilege"
          text="Third-class male survival was only ~14%, compared to ~37% for first-class males — a 23-point gap driven by cabin location and lifeboat access."
        />
        <InsightCard
          color="red"
          title="The Starkest Contrast"
          text="First-class female vs. third-class male: ~97% vs ~14% — a survival gap of over 80 percentage points between the most and least privileged groups."
        />
      </div>
    </div>
  )
}

function InsightCard({ color, title, text }) {
  const c = { cyan:'var(--cyan)', gold:'var(--gold)', red:'var(--red)' }[color]
  return (
    <div className={styles.insight} style={{ borderLeftColor: c }}>
      <div className={styles.insightTitle} style={{ color: c }}>{title}</div>
      <div className={styles.insightText}>{text}</div>
    </div>
  )
}
