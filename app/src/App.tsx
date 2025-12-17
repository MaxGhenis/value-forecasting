import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'
import './App.css'

const homosexData = [
  { year: 1973, actual: 11 },
  { year: 1980, actual: 14 },
  { year: 1990, actual: 13 },
  { year: 2000, actual: 27 },
  { year: 2010, actual: 42 },
  { year: 2018, actual: 57 },
  { year: 2021, actual: 62 },
  { year: 2022, actual: 61 },
  { year: 2024, actual: 55, predicted: 69 },
]

const grassData = [
  { year: 1973, actual: 19 },
  { year: 1980, actual: 25 },
  { year: 1990, actual: 16 },
  { year: 2000, actual: 31 },
  { year: 2010, actual: 48 },
  { year: 2018, actual: 65 },
  { year: 2022, actual: 70 },
  { year: 2024, actual: 69, predicted: 73 },
]

const multiVarData = [
  { variable: 'HOMOSEX', v2021: 62, v2024: 55, change: -7 },
  { variable: 'PREMARSX', v2021: 66, v2024: 65, change: -1 },
  { variable: 'NATRACE', v2021: 52, v2024: 51, change: -1 },
  { variable: 'ABANY', v2021: 56, v2024: 60, change: 4 },
  { variable: 'GUNLAW', v2021: 67, v2024: 70, change: 3 },
]

const partyData = [
  { party: 'Democrat', v2021: 76, v2024: 71, change: -5 },
  { party: 'Independent', v2021: 59, v2024: 57, change: -2 },
  { party: 'Republican', v2021: 43, v2024: 36, change: -7 },
]

const metricsData = [
  { model: 'Naive', mae: 31.4 },
  { model: 'Linear', mae: 30.2 },
  { model: 'ARIMA', mae: 31.4 },
  { model: 'ETS', mae: 28.1 },
  { model: 'LLM', mae: 12.5 },
]

function App() {
  const [selectedVar, setSelectedVar] = useState<'homosex' | 'grass'>('homosex')
  const data = selectedVar === 'homosex' ? homosexData : grassData
  const varLabel = selectedVar === 'homosex' ? 'Same-sex Relations OK' : 'Marijuana Legal'

  return (
    <div className="app">
      <header className="header">
        <h1>Can LLMs Forecast Human Values?</h1>
        <p className="subtitle">Evidence from the General Social Survey (1972-2024)</p>
      </header>

      <main className="main">
        <section className="hero-finding">
          <div className="finding-content">
            <span className="finding-label">Key Finding</span>
            <h2>LLMs Miss Value Reversals</h2>
            <p>
              GPT-4o predicted <strong className="predicted">69%</strong> acceptance
              of same-sex relationships for 2024.
              The actual value was <strong className="actual">55%</strong> —
              the first reversal in 30+ years.
            </p>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>Value Trajectories</h2>
            <div className="var-toggle">
              <button
                className={selectedVar === 'homosex' ? 'active' : ''}
                onClick={() => setSelectedVar('homosex')}
              >
                Same-sex Relations
              </button>
              <button
                className={selectedVar === 'grass' ? 'active' : ''}
                onClick={() => setSelectedVar('grass')}
              >
                Marijuana
              </button>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="year" stroke="#6b7280" fontSize={12} />
                <YAxis domain={[0, 100]} stroke="#6b7280" fontSize={12} tickFormatter={(v) => `${v}%`} />
                <Tooltip
                  formatter={(value: number) => [`${value}%`]}
                  contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="#2563eb"
                  strokeWidth={2.5}
                  name={`Actual: % "${varLabel}"`}
                  dot={{ fill: '#2563eb', r: 4 }}
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="predicted"
                  stroke="#dc2626"
                  strokeWidth={2}
                  strokeDasharray="6 4"
                  name="GPT-4o Prediction"
                  dot={{ fill: '#dc2626', r: 5 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <p className="caption">Source: General Social Survey. GSS 2024 data collected Apr-Dec 2024.</p>
        </section>

        <section className="section">
          <h2>Model Comparison (Historical)</h2>
          <p className="section-desc">LLM outperforms time series baselines by 2.2× on MAE</p>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={metricsData} layout="vertical" margin={{ left: 50, right: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" domain={[0, 35]} tickFormatter={(v) => `${v}%`} fontSize={12} />
                <YAxis type="category" dataKey="model" fontSize={12} />
                <Tooltip formatter={(value: number) => [`${value}%`, 'MAE']} />
                <Bar dataKey="mae" fill="#2563eb" radius={[0, 4, 4, 0]} name="Mean Absolute Error" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="section">
          <h2>2024: Values Diverged</h2>
          <p className="section-desc">HOMOSEX reversed while ABANY continued rising</p>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={multiVarData} margin={{ left: 10, right: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="variable" fontSize={11} />
                <YAxis domain={[0, 80]} tickFormatter={(v) => `${v}%`} fontSize={12} />
                <Tooltip formatter={(value: number) => [`${value}%`]} />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar dataKey="v2021" fill="#93c5fd" name="2021" radius={[4, 4, 0, 0]} />
                <Bar dataKey="v2024" fill="#2563eb" name="2024" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="section">
          <h2>HOMOSEX Reversal by Party</h2>
          <p className="section-desc">Republicans dropped 7 points; reversal hit all groups</p>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={partyData} margin={{ left: 10, right: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="party" fontSize={12} />
                <YAxis domain={[0, 100]} tickFormatter={(v) => `${v}%`} fontSize={12} />
                <Tooltip formatter={(value: number) => [`${value}%`]} />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar dataKey="v2021" fill="#93c5fd" name="2021" radius={[4, 4, 0, 0]} />
                <Bar dataKey="v2024" fill="#2563eb" name="2024" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="section implications">
          <h2>Implications for AI Alignment</h2>
          <div className="implications-grid">
            <div className="card">
              <div className="card-icon">📈</div>
              <h3>Extrapolation ≠ Forecasting</h3>
              <p>LLMs learn trends but miss inflection points where progress triggers backlash.</p>
            </div>
            <div className="card">
              <div className="card-icon">📊</div>
              <h3>Uncertainty is High</h3>
              <p>90% CIs should be wider. The 2024 actual fell outside GPT-4o's range.</p>
            </div>
            <div className="card">
              <div className="card-icon">🔀</div>
              <h3>Heterogeneity Matters</h3>
              <p>Values moved in different directions. Alignment targets should be distributions.</p>
            </div>
            <div className="card">
              <div className="card-icon">⚡</div>
              <h3>Backlash Dynamics</h3>
              <p>Models need to predict counter-mobilization, not just trend continuation.</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="footer-links">
          <a href="https://gss.norc.org">GSS Data</a>
          <span>•</span>
          <a href="https://github.com/maxghenis/value-forecasting">GitHub</a>
          <span>•</span>
          <a href="#">Paper (arXiv)</a>
        </div>
        <p className="footer-credit">Max Ghenis • PolicyEngine</p>
      </footer>
    </div>
  )
}

export default App
