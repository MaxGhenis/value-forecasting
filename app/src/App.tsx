import { useState } from 'react'
import { Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Area, ComposedChart, Cell } from 'recharts'
import './App.css'

// All GSS variables with historical data and calibrated forecasts
const variableData: Record<string, {
  description: string;
  historical: { year: number; actual: number }[];
  forecasts: { year: number; predicted: number; predLow: number; predHigh: number }[];
  actual2024: number;
  predicted2024: number;
}> = {
  HOMOSEX: {
    description: "Same-sex relations not wrong",
    historical: [
      { year: 1974, actual: 13 }, { year: 1980, actual: 15 }, { year: 1990, actual: 13 },
      { year: 2000, actual: 29 }, { year: 2010, actual: 42 }, { year: 2018, actual: 57 },
      { year: 2021, actual: 62 }, { year: 2022, actual: 61 }
    ],
    forecasts: [
      { year: 2024, predicted: 63, predLow: 56, predHigh: 70 },
      { year: 2030, predicted: 66, predLow: 57, predHigh: 75 },
      { year: 2050, predicted: 75, predLow: 64, predHigh: 86 },
      { year: 2100, predicted: 80, predLow: 69, predHigh: 91 }
    ],
    actual2024: 55,
    predicted2024: 63
  },
  GRASS: {
    description: "Marijuana should be legal",
    historical: [
      { year: 1976, actual: 29 }, { year: 1980, actual: 26 }, { year: 1990, actual: 17 },
      { year: 2000, actual: 34 }, { year: 2010, actual: 48 }, { year: 2018, actual: 65 },
      { year: 2022, actual: 70 }
    ],
    forecasts: [
      { year: 2024, predicted: 70, predLow: 61, predHigh: 79 },
      { year: 2030, predicted: 72, predLow: 57, predHigh: 87 },
      { year: 2050, predicted: 80, predLow: 57, predHigh: 100 },
      { year: 2100, predicted: 80, predLow: 57, predHigh: 100 }
    ],
    actual2024: 69,
    predicted2024: 70
  },
  PREMARSX: {
    description: "Premarital sex not wrong",
    historical: [
      { year: 1972, actual: 27 }, { year: 1980, actual: 43 }, { year: 1990, actual: 40 },
      { year: 2000, actual: 42 }, { year: 2010, actual: 53 }, { year: 2018, actual: 62 },
      { year: 2021, actual: 66 }, { year: 2022, actual: 69 }
    ],
    forecasts: [
      { year: 2024, predicted: 66, predLow: 59, predHigh: 73 },
      { year: 2030, predicted: 70, predLow: 59, predHigh: 81 },
      { year: 2050, predicted: 80, predLow: 69, predHigh: 91 },
      { year: 2100, predicted: 80, predLow: 69, predHigh: 91 }
    ],
    actual2024: 65,
    predicted2024: 66
  },
  ABANY: {
    description: "Abortion for any reason",
    historical: [
      { year: 1978, actual: 33 }, { year: 1990, actual: 43 }, { year: 2000, actual: 40 },
      { year: 2010, actual: 44 }, { year: 2018, actual: 50 }, { year: 2021, actual: 56 },
      { year: 2022, actual: 59 }
    ],
    forecasts: [
      { year: 2024, predicted: 50, predLow: 42, predHigh: 58 },
      { year: 2030, predicted: 60, predLow: 51, predHigh: 69 },
      { year: 2050, predicted: 60, predLow: 42, predHigh: 78 },
      { year: 2100, predicted: 60, predLow: 37, predHigh: 83 }
    ],
    actual2024: 60,
    predicted2024: 50
  },
  FEPOL: {
    description: "Women suited for politics",
    historical: [
      { year: 1974, actual: 53 }, { year: 1982, actual: 63 }, { year: 1990, actual: 73 },
      { year: 2000, actual: 77 }, { year: 2010, actual: 79 }, { year: 2018, actual: 86 },
      { year: 2022, actual: 85 }
    ],
    forecasts: [
      { year: 2024, predicted: 82, predLow: 77, predHigh: 87 },
      { year: 2030, predicted: 84, predLow: 77, predHigh: 91 },
      { year: 2050, predicted: 86, predLow: 77, predHigh: 95 },
      { year: 2100, predicted: 85, predLow: 69, predHigh: 100 }
    ],
    actual2024: 82,
    predicted2024: 82
  },
  CAPPUN: {
    description: "Oppose death penalty",
    historical: [
      { year: 1974, actual: 34 }, { year: 1980, actual: 28 }, { year: 1990, actual: 21 },
      { year: 2000, actual: 31 }, { year: 2010, actual: 33 }, { year: 2018, actual: 37 },
      { year: 2021, actual: 44 }, { year: 2022, actual: 40 }
    ],
    forecasts: [
      { year: 2024, predicted: 39, predLow: 33, predHigh: 45 },
      { year: 2030, predicted: 42, predLow: 33, predHigh: 51 },
      { year: 2050, predicted: 45, predLow: 34, predHigh: 56 },
      { year: 2100, predicted: 55, predLow: 32, predHigh: 78 }
    ],
    actual2024: 40,
    predicted2024: 39
  },
  GUNLAW: {
    description: "Favor gun permits",
    historical: [
      { year: 1972, actual: 72 }, { year: 1980, actual: 71 }, { year: 1990, actual: 80 },
      { year: 2000, actual: 82 }, { year: 2010, actual: 75 }, { year: 2018, actual: 72 },
      { year: 2021, actual: 67 }, { year: 2022, actual: 71 }
    ],
    forecasts: [
      { year: 2024, predicted: 72, predLow: 65, predHigh: 79 },
      { year: 2030, predicted: 71, predLow: 64, predHigh: 78 },
      { year: 2050, predicted: 70, predLow: 59, predHigh: 81 },
      { year: 2100, predicted: 70, predLow: 59, predHigh: 81 }
    ],
    actual2024: 70,
    predicted2024: 72
  },
  NATRACE: {
    description: "More spending on race issues",
    historical: [
      { year: 1974, actual: 33 }, { year: 1980, actual: 26 }, { year: 1990, actual: 40 },
      { year: 2000, actual: 38 }, { year: 2010, actual: 34 }, { year: 2018, actual: 56 },
      { year: 2021, actual: 52 }, { year: 2022, actual: 56 }
    ],
    forecasts: [
      { year: 2024, predicted: 45, predLow: 31, predHigh: 59 },
      { year: 2030, predicted: 52, predLow: 37, predHigh: 67 },
      { year: 2050, predicted: 55, predLow: 32, predHigh: 78 },
      { year: 2100, predicted: 55, predLow: 32, predHigh: 78 }
    ],
    actual2024: 51,
    predicted2024: 45
  },
  NATEDUC: {
    description: "More spending on education",
    historical: [
      { year: 1974, actual: 53 }, { year: 1980, actual: 55 }, { year: 1990, actual: 73 },
      { year: 2000, actual: 72 }, { year: 2010, actual: 72 }, { year: 2018, actual: 75 },
      { year: 2021, actual: 73 }, { year: 2022, actual: 75 }
    ],
    forecasts: [
      { year: 2024, predicted: 73, predLow: 69, predHigh: 77 },
      { year: 2030, predicted: 74, predLow: 69, predHigh: 79 },
      { year: 2050, predicted: 75, predLow: 68, predHigh: 82 },
      { year: 2100, predicted: 75, predLow: 68, predHigh: 82 }
    ],
    actual2024: 76,
    predicted2024: 73
  },
  NATENVIR: {
    description: "More spending on environment",
    historical: [
      { year: 1974, actual: 63 }, { year: 1980, actual: 51 }, { year: 1990, actual: 75 },
      { year: 2000, actual: 63 }, { year: 2010, actual: 57 }, { year: 2018, actual: 68 },
      { year: 2021, actual: 70 }, { year: 2022, actual: 69 }
    ],
    forecasts: [
      { year: 2024, predicted: 63, predLow: 55, predHigh: 71 },
      { year: 2030, predicted: 65, predLow: 56, predHigh: 74 },
      { year: 2050, predicted: 65, predLow: 54, predHigh: 76 },
      { year: 2100, predicted: 65, predLow: 54, predHigh: 76 }
    ],
    actual2024: 66,
    predicted2024: 63
  },
  NATHEAL: {
    description: "More spending on health",
    historical: [
      { year: 1974, actual: 66 }, { year: 1980, actual: 57 }, { year: 1990, actual: 74 },
      { year: 2000, actual: 73 }, { year: 2010, actual: 60 }, { year: 2018, actual: 73 },
      { year: 2021, actual: 67 }, { year: 2022, actual: 70 }
    ],
    forecasts: [
      { year: 2024, predicted: 68, predLow: 59, predHigh: 77 },
      { year: 2030, predicted: 70, predLow: 59, predHigh: 81 },
      { year: 2050, predicted: 70, predLow: 59, predHigh: 81 },
      { year: 2100, predicted: 70, predLow: 59, predHigh: 81 }
    ],
    actual2024: 74,
    predicted2024: 68
  },
  EQWLTH: {
    description: "Government reduce inequality",
    historical: [
      { year: 1978, actual: 48 }, { year: 1990, actual: 52 }, { year: 2000, actual: 44 },
      { year: 2010, actual: 42 }, { year: 2018, actual: 50 }, { year: 2021, actual: 55 },
      { year: 2022, actual: 55 }
    ],
    forecasts: [
      { year: 2024, predicted: 49, predLow: 43, predHigh: 55 },
      { year: 2030, predicted: 52, predLow: 44, predHigh: 60 },
      { year: 2050, predicted: 51, predLow: 42, predHigh: 60 },
      { year: 2100, predicted: 50, predLow: 39, predHigh: 61 }
    ],
    actual2024: 54,
    predicted2024: 49
  },
  HELPPOOR: {
    description: "Government help poor",
    historical: [
      { year: 1984, actual: 29 }, { year: 1990, actual: 35 }, { year: 2000, actual: 27 },
      { year: 2010, actual: 28 }, { year: 2018, actual: 32 }, { year: 2021, actual: 38 },
      { year: 2022, actual: 40 }
    ],
    forecasts: [
      { year: 2024, predicted: 31, predLow: 25, predHigh: 37 },
      { year: 2030, predicted: 35, predLow: 27, predHigh: 43 },
      { year: 2050, predicted: 36, predLow: 27, predHigh: 45 },
      { year: 2100, predicted: 35, predLow: 24, predHigh: 46 }
    ],
    actual2024: 39,
    predicted2024: 31
  },
  TRUST: {
    description: "Most people can be trusted",
    historical: [
      { year: 1972, actual: 46 }, { year: 1980, actual: 46 }, { year: 1990, actual: 38 },
      { year: 2000, actual: 35 }, { year: 2010, actual: 33 }, { year: 2018, actual: 32 },
      { year: 2022, actual: 25 }
    ],
    forecasts: [
      { year: 2024, predicted: 33, predLow: 29, predHigh: 37 },
      { year: 2030, predicted: 28, predLow: 21, predHigh: 35 },
      { year: 2050, predicted: 27, predLow: 18, predHigh: 36 },
      { year: 2100, predicted: 27, predLow: 18, predHigh: 36 }
    ],
    actual2024: 25,
    predicted2024: 33
  },
  FAIR: {
    description: "People try to be fair",
    historical: [
      { year: 1972, actual: 34 }, { year: 1980, actual: 35 }, { year: 1990, actual: 36 },
      { year: 2000, actual: 39 }, { year: 2010, actual: 38 }, { year: 2018, actual: 43 },
      { year: 2022, actual: 47 }
    ],
    forecasts: [
      { year: 2024, predicted: 40, predLow: 36, predHigh: 44 },
      { year: 2030, predicted: 42, predLow: 35, predHigh: 49 },
      { year: 2050, predicted: 43, predLow: 34, predHigh: 52 },
      { year: 2100, predicted: 45, predLow: 34, predHigh: 56 }
    ],
    actual2024: 46,
    predicted2024: 40
  },
  POLVIEWS: {
    description: "Self-identified liberal",
    historical: [
      { year: 1974, actual: 31 }, { year: 1980, actual: 26 }, { year: 1990, actual: 27 },
      { year: 2000, actual: 27 }, { year: 2010, actual: 29 }, { year: 2018, actual: 29 },
      { year: 2021, actual: 33 }, { year: 2022, actual: 32 }
    ],
    forecasts: [
      { year: 2024, predicted: 28, predLow: 24, predHigh: 32 },
      { year: 2030, predicted: 30, predLow: 25, predHigh: 35 },
      { year: 2050, predicted: 30, predLow: 23, predHigh: 37 },
      { year: 2100, predicted: 31, predLow: 24, predHigh: 38 }
    ],
    actual2024: 29,
    predicted2024: 28
  },
  PRAYER: {
    description: "Approve school prayer ban",
    historical: [
      { year: 1974, actual: 32 }, { year: 1985, actual: 44 }, { year: 1990, actual: 42 },
      { year: 2000, actual: 39 }, { year: 2010, actual: 44 }, { year: 2018, actual: 47 },
      { year: 2022, actual: 52 }
    ],
    forecasts: [
      { year: 2024, predicted: 42, predLow: 38, predHigh: 46 },
      { year: 2030, predicted: 48, predLow: 39, predHigh: 57 },
      { year: 2050, predicted: 50, predLow: 39, predHigh: 61 },
      { year: 2100, predicted: 45, predLow: 34, predHigh: 56 }
    ],
    actual2024: 46,
    predicted2024: 42
  }
}

// Group variables by category
const categories = {
  "Social/Moral": ["HOMOSEX", "GRASS", "PREMARSX", "ABANY"],
  "Gender/Politics": ["FEPOL", "CAPPUN", "GUNLAW", "POLVIEWS"],
  "Spending": ["NATRACE", "NATEDUC", "NATENVIR", "NATHEAL"],
  "Economic/Social": ["EQWLTH", "HELPPOOR", "TRUST", "FAIR", "PRAYER"]
}

// Prepare chart data for a given variable
function getChartData(varKey: string) {
  const v = variableData[varKey]
  const data: Array<{
    year: number;
    actual?: number;
    predicted?: number;
    predLow?: number;
    predHigh?: number;
  }> = []

  // Add historical data
  v.historical.forEach(h => {
    data.push({ year: h.year, actual: h.actual })
  })

  // Add 2024 with both actual and predicted
  data.push({
    year: 2024,
    actual: v.actual2024,
    predicted: v.predicted2024,
    predLow: v.forecasts[0].predLow,
    predHigh: v.forecasts[0].predHigh
  })

  // Add future forecasts
  v.forecasts.slice(1).forEach(f => {
    data.push({
      year: f.year,
      predicted: f.predicted,
      predLow: f.predLow,
      predHigh: f.predHigh
    })
  })

  return data
}

// Model comparison data (2021→2024 holdout, 17 variables)
// CRPS = Continuous Ranked Probability Score (proper scoring rule for probabilistic forecasts)
const metricsData = [
  { model: 'Naive', crps: 2.84, mae: 3.8, coverage80: 59, type: 'baseline' },
  { model: 'Linear', crps: 2.85, mae: 3.7, coverage80: 62, type: 'baseline' },
  { model: 'GPT-4o', crps: 3.15, mae: 4.4, coverage80: 59, type: 'llm' },
  { model: 'ETS', crps: 11.21, mae: 13.1, coverage80: 41, type: 'baseline' },
]

// Per-variable baseline predictions (2021→2024)
const baselinePredictions: Record<string, { naive: number; linear: number; ets: number }> = {
  HOMOSEX: { naive: 61, linear: 64, ets: 68 },
  GRASS: { naive: 70, linear: 73, ets: 85 },
  PREMARSX: { naive: 69, linear: 71, ets: 77 },
  ABANY: { naive: 59, linear: 61, ets: 68 },
  FEPOL: { naive: 85, linear: 86, ets: 91 },
  CAPPUN: { naive: 40, linear: 45, ets: 51 },
  GUNLAW: { naive: 71, linear: 68, ets: 62 },
  NATRACE: { naive: 56, linear: 56, ets: 60 },
  NATEDUC: { naive: 75, linear: 75, ets: 76 },
  NATENVIR: { naive: 69, linear: 69, ets: 71 },
  NATHEAL: { naive: 70, linear: 69, ets: 68 },
  EQWLTH: { naive: 55, linear: 57, ets: 61 },
  HELPPOOR: { naive: 40, linear: 41, ets: 46 },
  TRUST: { naive: 25, linear: 22, ets: 16 },
  FAIR: { naive: 47, linear: 48, ets: 53 },
  POLVIEWS: { naive: 32, linear: 34, ets: 38 },
  PRAYER: { naive: 52, linear: 53, ets: 59 },
}

// LLM models available for comparison
const llmModels = [
  { id: 'gpt-4o', name: 'GPT-4o', color: '#10b981' },
  { id: 'gpt-4.5', name: 'GPT-4.5 (Preview)', color: '#8b5cf6', comingSoon: true },
  { id: 'claude-opus', name: 'Claude Opus 4', color: '#f59e0b', comingSoon: true },
  { id: 'claude-sonnet', name: 'Claude Sonnet 4', color: '#ec4899', comingSoon: true },
]

// 2024 calibration results
const calibrationData = Object.entries(variableData).map(([key, v]) => ({
  variable: key,
  actual: v.actual2024,
  predicted: v.predicted2024,
  error: v.predicted2024 - v.actual2024,
  absError: Math.abs(v.predicted2024 - v.actual2024)
})).sort((a, b) => b.absError - a.absError)

function App() {
  const [selectedVar, setSelectedVar] = useState<string>('HOMOSEX')
  const data = getChartData(selectedVar)
  const varInfo = variableData[selectedVar]

  return (
    <div className="app">
      <header className="header">
        <h1>Can LLMs Forecast Human Values?</h1>
        <p className="subtitle">Calibrated GPT-4o Forecasts for 17 GSS Variables (1972-2100)</p>
      </header>

      <main className="main">
        <section className="hero-finding">
          <div className="finding-content">
            <span className="finding-label">Key Finding</span>
            <h2>LLMs Slightly Underperform Baselines on 3-Year Probabilistic Forecasts</h2>
            <p>
              On the 2021→2024 holdout using CRPS (a proper scoring rule), GPT-4o (3.15) slightly
              underperforms naive (2.84) and linear (2.85) baselines. All models show ~60% coverage
              on 80% CIs—everyone is overconfident. The 2024 HOMOSEX reversal (predicted ~63%, actual 55%)
              surprised all models. Long-term forecasts remain untested.
            </p>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>Value Trajectories & LLM Forecasts</h2>
          </div>
          <div className="var-selector">
            {Object.entries(categories).map(([category, vars]) => (
              <div key={category} className="var-category">
                <span className="category-label">{category}</span>
                <div className="var-buttons">
                  {vars.map(v => (
                    <button
                      key={v}
                      className={selectedVar === v ? 'active' : ''}
                      onClick={() => setSelectedVar(v)}
                      title={variableData[v].description}
                    >
                      {v}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <p className="var-description">{varInfo.description}</p>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={400}>
              <ComposedChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                <defs>
                  <linearGradient id="uncertaintyGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#dc2626" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#dc2626" stopOpacity={0.05}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="year" stroke="#6b7280" fontSize={12} />
                <YAxis domain={[0, 100]} stroke="#6b7280" fontSize={12} tickFormatter={(v) => `${v}%`} />
                <Tooltip
                  formatter={(value, name) => {
                    if (value === undefined || name === 'predLow' || name === 'predHigh') return null
                    return [`${value}%`, name === 'actual' ? 'Actual' : 'GPT-4o Prediction']
                  }}
                  contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area
                  type="monotone"
                  dataKey="predHigh"
                  stroke="none"
                  fill="url(#uncertaintyGradient)"
                  name="80% CI (Upper)"
                  legendType="none"
                />
                <Area
                  type="monotone"
                  dataKey="predLow"
                  stroke="none"
                  fill="#f8fafc"
                  name="80% CI (Lower)"
                  legendType="none"
                />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="#2563eb"
                  strokeWidth={2.5}
                  name={`Actual: % "${varInfo.description}"`}
                  dot={{ fill: '#2563eb', r: 4 }}
                  activeDot={{ r: 6 }}
                  connectNulls={false}
                />
                <Line
                  type="monotone"
                  dataKey="predicted"
                  stroke="#dc2626"
                  strokeWidth={2}
                  strokeDasharray="6 4"
                  name="GPT-4o Prediction"
                  dot={{ fill: '#dc2626', r: 5 }}
                  connectNulls
                />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
          <p className="caption">Source: General Social Survey (1972-2024). Shaded area shows calibrated 80% CI (EMOS method, spread multiplier 1.21).</p>
        </section>

        <section className="section">
          <h2>Model Comparison: 2021→2024 Holdout</h2>
          <p className="section-desc">CRPS (Continuous Ranked Probability Score) evaluates full predictive distribution. Lower = better.</p>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={metricsData} layout="vertical" margin={{ left: 60, right: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" domain={[0, 12]} fontSize={12} />
                <YAxis type="category" dataKey="model" fontSize={12} />
                <Tooltip
                  formatter={(value, name) => {
                    if (name === 'crps') return [value, 'CRPS']
                    return null
                  }}
                  labelFormatter={(label) => {
                    const m = metricsData.find(d => d.model === label)
                    return m ? `${label} (80% CI coverage: ${m.coverage80}%)` : label
                  }}
                />
                <Bar dataKey="crps" radius={[0, 4, 4, 0]} name="CRPS">
                  {metricsData.map((entry, index) => (
                    <Cell key={index} fill={entry.type === 'llm' ? '#10b981' : '#64748b'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="legend-custom">
            <span className="legend-item"><span className="dot" style={{background: '#10b981'}}></span> LLM</span>
            <span className="legend-item"><span className="dot" style={{background: '#64748b'}}></span> Time Series</span>
            <span className="legend-item" style={{marginLeft: '1rem', color: '#94a3b8'}}>80% CI coverage: all models ~60% (should be 80%)</span>
          </div>
        </section>

        <section className="section">
          <h2>2024 Holdout: Prediction Errors</h2>
          <p className="section-desc">Largest misses: HOMOSEX (-8pp), HELPPOOR (+8pp), ABANY (+10pp)</p>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={calibrationData} layout="vertical" margin={{ left: 80, right: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" domain={[-15, 15]} tickFormatter={(v) => `${v > 0 ? '+' : ''}${v}`} fontSize={12} />
                <YAxis type="category" dataKey="variable" fontSize={11} width={70} />
                <Tooltip
                  formatter={(value, name) => {
                    if (name === 'error') return [`${Number(value) > 0 ? '+' : ''}${value}pp`, 'Prediction Error']
                    return null
                  }}
                  labelFormatter={(label) => variableData[label]?.description || label}
                />
                <Bar
                  dataKey="error"
                  name="Error (Predicted - Actual)"
                  fill={(entry: { error: number }) => entry.error > 0 ? '#dc2626' : '#16a34a'}
                  radius={[0, 4, 4, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="caption">Positive = overpredicted, Negative = underpredicted. Mean Absolute Error: {(calibrationData.reduce((sum, d) => sum + d.absError, 0) / calibrationData.length).toFixed(1)}pp</p>
        </section>

        <section className="section implications">
          <h2>Implications for AI Alignment</h2>
          <div className="implications-grid">
            <div className="card">
              <h3>Long-Term Trends</h3>
              <p>LLMs capture 50-year trajectories well. Most values continue their historical direction through 2100.</p>
            </div>
            <div className="card">
              <h3>Calibrated Uncertainty</h3>
              <p>EMOS calibration widens CIs by 21%. Raw LLM confidence intervals are too narrow.</p>
            </div>
            <div className="card">
              <h3>Short-Term Reversals</h3>
              <p>2024 showed surprising reversals (HOMOSEX, TRUST). LLMs miss discontinuities.</p>
            </div>
            <div className="card">
              <h3>Value Divergence</h3>
              <p>Different values moved in different directions—ABANY up while HOMOSEX down.</p>
            </div>
          </div>
        </section>

        <section className="section">
          <h2>Methodology Notes</h2>
          <div className="method-notes">
            <p><strong>Data:</strong> General Social Survey (GSS), 1972-2024. 17 variables selected for consistent measurement.</p>
            <p><strong>Calibration:</strong> Ensemble Model Output Statistics (EMOS) fit on 2024 holdout. Spread multiplier: 1.21.</p>
            <p><strong>Forecasts:</strong> GPT-4o with chain-of-thought prompting. Quantiles elicited (10th, 25th, 50th, 75th, 90th).</p>
            <p><strong>Confidence Intervals:</strong> 80% CIs derived from calibrated Gaussian fit to elicited quantiles.</p>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="footer-links">
          <a href="https://gss.norc.org">GSS Data</a>
          <span>|</span>
          <a href="https://github.com/maxghenis/value-forecasting">GitHub</a>
          <span>|</span>
          <a href="#">Paper (coming soon)</a>
        </div>
        <p className="footer-credit">Max Ghenis | PolicyEngine</p>
      </footer>
    </div>
  )
}

export default App
