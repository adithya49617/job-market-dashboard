import { useState, useEffect } from "react";

const API_BASE = "";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0a0a0f; --surface: #111118; --surface2: #1a1a24; --surface3: #22222f;
    --border: rgba(255,255,255,0.07); --border-strong: rgba(255,255,255,0.14);
    --accent: #7c6dfa; --accent2: #6dfabd; --accent3: #fa6d8f; --accent4: #fac96d;
    --text: #f0f0f8; --text2: #9999b5; --text3: #5a5a7a;
    --radius: 14px; --radius-sm: 8px;
  }
  body { background: var(--bg); color: var(--text); font-family: 'DM Mono', monospace; min-height: 100vh; }
  .app { max-width: 1200px; margin: 0 auto; padding: 32px 20px 60px; }

  .header { text-align: center; margin-bottom: 40px; }
  .eyebrow { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--accent); margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px; }
  .eyebrow::before, .eyebrow::after { content: ''; width: 28px; height: 1px; background: var(--accent); opacity: 0.5; }
  .header h1 { font-family: 'Syne', sans-serif; font-size: clamp(28px, 5vw, 52px); font-weight: 800; letter-spacing: -1.5px; background: linear-gradient(135deg, #fff 30%, var(--accent) 70%, var(--accent2) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 10px; }
  .header p { color: var(--text2); font-size: 13px; }

  .search-bar { display: flex; gap: 10px; margin-bottom: 32px; flex-wrap: wrap; }
  .search-input { flex: 1; min-width: 180px; background: var(--surface); border: 1px solid var(--border-strong); border-radius: var(--radius-sm); padding: 11px 16px; color: var(--text); font-family: 'DM Mono', monospace; font-size: 13px; outline: none; transition: border-color 0.2s; }
  .search-input:focus { border-color: var(--accent); }
  .search-input::placeholder { color: var(--text3); }
  .btn { background: var(--accent); color: #fff; border: none; border-radius: var(--radius-sm); padding: 11px 22px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
  .btn:hover { background: #9080ff; }
  .btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .btn-outline { background: transparent; border: 1px solid var(--border-strong); color: var(--text2); }
  .btn-outline:hover { border-color: var(--accent); color: var(--accent); background: transparent; }

  .badge { font-size: 11px; padding: 3px 10px; border-radius: 100px; font-family: 'DM Mono', monospace; }
  .badge-live { background: rgba(109,250,189,0.1); color: var(--accent2); border: 1px solid rgba(109,250,189,0.3); }
  .badge-sample { background: rgba(250,201,109,0.1); color: var(--accent4); border: 1px solid rgba(250,201,109,0.3); }

  .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 28px; }
  .metric { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px; }
  .metric-label { font-size: 11px; color: var(--text3); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .metric-value { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: var(--text); line-height: 1; }
  .metric-sub { font-size: 11px; color: var(--text2); margin-top: 4px; }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  @media (max-width: 900px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }

  .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 22px; }
  .card-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text2); margin-bottom: 18px; }

  /* Bar chart */
  .bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
  .bar-label { font-size: 12px; color: var(--text2); width: 140px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .bar-track { flex: 1; height: 8px; background: var(--surface3); border-radius: 100px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 100px; transition: width 0.8s ease; }
  .bar-count { font-size: 12px; color: var(--text3); width: 30px; text-align: right; flex-shrink: 0; }

  /* Donut chart */
  .donut-wrap { display: flex; align-items: center; gap: 24px; }
  .donut-legend { display: flex; flex-direction: column; gap: 10px; }
  .legend-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text2); }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }

  /* Salary bars */
  .salary-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
  .salary-label { font-size: 11px; color: var(--text2); width: 160px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .salary-bar-track { flex: 1; height: 10px; background: var(--surface3); border-radius: 100px; overflow: hidden; }
  .salary-val { font-size: 11px; color: var(--text3); width: 50px; text-align: right; flex-shrink: 0; }

  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner { width: 32px; height: 32px; border: 3px solid rgba(255,255,255,0.1); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 60px auto; }
  .error-box { background: rgba(250,109,143,0.08); border: 1px solid rgba(250,109,143,0.3); border-radius: var(--radius-sm); padding: 14px 18px; font-size: 13px; color: var(--accent3); margin-bottom: 20px; }
`;

const COLORS = ["#7c6dfa", "#6dfabd", "#fa6d8f", "#fac96d", "#6db8fa", "#fa9b6d", "#c96dfa", "#6dfafa"];
const REMOTE_COLORS = { remote: "#6dfabd", onsite: "#fa6d8f", hybrid: "#7c6dfa" };

function BarChart({ data, labelKey, valueKey, color = "#7c6dfa" }) {
  const max = Math.max(...data.map(d => d[valueKey]));
  return (
    <div>
      {data.map((d, i) => (
        <div key={i} className="bar-row">
          <div className="bar-label" title={d[labelKey]}>{d[labelKey]}</div>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${(d[valueKey] / max) * 100}%`, background: color }} />
          </div>
          <div className="bar-count">{d[valueKey]}</div>
        </div>
      ))}
    </div>
  );
}

function DonutChart({ data, labelKey, valueKey }) {
  const total = data.reduce((s, d) => s + d[valueKey], 0);
  let offset = 0;
  const r = 60, cx = 70, cy = 70, circ = 2 * Math.PI * r;

  return (
    <div className="donut-wrap">
      <svg width="140" height="140" style={{ flexShrink: 0 }}>
        {data.map((d, i) => {
          const pct = d[valueKey] / total;
          const dash = pct * circ;
          const gap = circ - dash;
          const rotate = offset * 360 - 90;
          offset += pct;
          const color = REMOTE_COLORS[d[labelKey]] || COLORS[i % COLORS.length];
          return (
            <circle key={i} cx={cx} cy={cy} r={r} fill="none"
              stroke={color} strokeWidth="18"
              strokeDasharray={`${dash} ${gap}`}
              strokeDashoffset={0}
              transform={`rotate(${rotate} ${cx} ${cy})`}
              style={{ transition: "stroke-dasharray 0.8s ease" }}
            />
          );
        })}
        <text x={cx} y={cy - 6} textAnchor="middle" fill="#f0f0f8" fontSize="22" fontWeight="800" fontFamily="Syne">{total}</text>
        <text x={cx} y={cy + 14} textAnchor="middle" fill="#9999b5" fontSize="10">jobs</text>
      </svg>
      <div className="donut-legend">
        {data.map((d, i) => {
          const color = REMOTE_COLORS[d[labelKey]] || COLORS[i % COLORS.length];
          return (
            <div key={i} className="legend-item">
              <div className="legend-dot" style={{ background: color }} />
              <span>{d[labelKey]}</span>
              <span style={{ color: "#5a5a7a", marginLeft: 4 }}>({Math.round(d[valueKey] / total * 100)}%)</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function SalaryChart({ data }) {
  const max = Math.max(...data.map(d => d.avg_salary));
  return (
    <div>
      {data.map((d, i) => (
        <div key={i} className="salary-row">
          <div className="salary-label" title={d.title}>{d.title}</div>
          <div className="salary-bar-track">
            <div className="bar-fill" style={{ width: `${(d.avg_salary / max) * 100}%`, background: COLORS[i % COLORS.length], height: "100%", borderRadius: "100px", transition: "width 0.8s ease" }} />
          </div>
          <div className="salary-val">${d.avg_salary}k</div>
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState("data scientist");
  const [location, setLocation] = useState("United States");

  const fetchData = async (q = query, loc = location) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/analytics?query=${encodeURIComponent(q)}&location=${encodeURIComponent(loc)}`);
      if (!res.ok) throw new Error("Failed to load analytics");
      setData(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  return (
    <>
      <style>{styles}</style>
      <div className="app">
        <div className="header">
          <div className="eyebrow">Real-time · Analytics</div>
          <h1>Job Market Dashboard</h1>
          <p>Analyze trends in data science & ML job postings — skills, salaries, companies, and more</p>
        </div>

        <div className="search-bar">
          <input className="search-input" value={query} onChange={e => setQuery(e.target.value)}
            placeholder="Job title (e.g. data scientist)" onKeyDown={e => e.key === "Enter" && fetchData()} />
          <input className="search-input" value={location} onChange={e => setLocation(e.target.value)}
            placeholder="Location (e.g. San Francisco)" onKeyDown={e => e.key === "Enter" && fetchData()} />
          <button className="btn" onClick={() => fetchData()} disabled={loading}>
            {loading ? "Loading..." : "Analyze →"}
          </button>
        </div>

        {error && <div className="error-box">⚠️ {error}</div>}

        {loading && <div className="spinner" />}

        {data && !loading && (
          <>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
              <span className={`badge ${data.data_source === "live" ? "badge-live" : "badge-sample"}`}>
                {data.data_source === "live" ? "⚡ Live data" : "📦 Sample data"}
              </span>
              <span style={{ fontSize: 12, color: "var(--text3)" }}>
                Showing {data.total_jobs} jobs for "{data.query}"
              </span>
            </div>

            {/* Summary metrics */}
            <div className="metrics">
              <div className="metric">
                <div className="metric-label">Total Jobs</div>
                <div className="metric-value">{data.summary.total_jobs}</div>
                <div className="metric-sub">postings analyzed</div>
              </div>
              <div className="metric">
                <div className="metric-label">Companies</div>
                <div className="metric-value">{data.summary.total_companies}</div>
                <div className="metric-sub">unique hiring</div>
              </div>
              <div className="metric">
                <div className="metric-label">Avg Salary</div>
                <div className="metric-value">${data.summary.avg_salary}k</div>
                <div className="metric-sub">per year</div>
              </div>
              <div className="metric">
                <div className="metric-label">Remote</div>
                <div className="metric-value">{data.summary.remote_pct}%</div>
                <div className="metric-sub">of postings</div>
              </div>
              <div className="metric">
                <div className="metric-label">Top Skill</div>
                <div className="metric-value" style={{ fontSize: 20 }}>{data.summary.top_skill}</div>
                <div className="metric-sub">most in-demand</div>
              </div>
            </div>

            {/* Top skills + Remote breakdown */}
            <div className="grid-2">
              <div className="card">
                <div className="card-title">🔥 Top In-Demand Skills</div>
                <BarChart data={data.top_skills.slice(0, 10)} labelKey="skill" valueKey="count" color="#7c6dfa" />
              </div>
              <div className="card">
                <div className="card-title">🌐 Remote vs Onsite vs Hybrid</div>
                <DonutChart data={data.remote_breakdown} labelKey="type" valueKey="count" />
              </div>
            </div>

            {/* Salary + Top companies */}
            <div className="grid-2">
              <div className="card">
                <div className="card-title">💰 Avg Salary by Role</div>
                <SalaryChart data={data.salary_distribution} />
              </div>
              <div className="card">
                <div className="card-title">🏢 Top Hiring Companies</div>
                <BarChart data={data.top_companies} labelKey="company" valueKey="count" color="#6dfabd" />
              </div>
            </div>

            {/* Locations + Titles */}
            <div className="grid-2">
              <div className="card">
                <div className="card-title">📍 Top Locations</div>
                <BarChart data={data.top_locations} labelKey="location" valueKey="count" color="#fac96d" />
              </div>
              <div className="card">
                <div className="card-title">📋 Top Job Titles</div>
                <BarChart data={data.top_titles} labelKey="title" valueKey="count" color="#fa6d8f" />
              </div>
            </div>
          </>
        )}
      </div>
    </>
  );
}
