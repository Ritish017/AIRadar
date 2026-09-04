// AI Viral Radar V3 - Extension Popup Controller
// ZERO credential leakage: communicates solely with local backend API

const API_BASE = "http://127.0.0.1:8000/api";

const container = document.getElementById("content-container");
const refreshBtn = document.getElementById("btn-refresh");

const tabLive = document.getElementById("tab-live");
const tabTrends = document.getElementById("tab-trends");
const tabOpps = document.getElementById("tab-opps");
const tabCreate = document.getElementById("tab-create");

let currentTab = "live";

tabLive.addEventListener("click", () => switchTab("live"));
tabTrends.addEventListener("click", () => switchTab("trends"));
tabOpps.addEventListener("click", () => switchTab("opps"));
tabCreate.addEventListener("click", () => switchTab("create"));
refreshBtn.addEventListener("click", () => loadCurrentView());

function switchTab(tab) {
  currentTab = tab;
  [tabLive, tabTrends, tabOpps, tabCreate].forEach(t => t.classList.remove("active"));
  if (tab === "live") tabLive.classList.add("active");
  if (tab === "trends") tabTrends.classList.add("active");
  if (tab === "opps") tabOpps.classList.add("active");
  if (tab === "create") tabCreate.classList.add("active");
  loadCurrentView();
}

async function loadCurrentView() {
  container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>Loading V3 intelligence...</div>";

  try {
    if (currentTab === "live") {
      const res = await fetch(`${API_BASE}/events?limit=8`);
      if (res.ok) {
        const data = await res.json();
        renderLiveEvents(data.events || []);
        return;
      }
    } else if (currentTab === "trends") {
      const res = await fetch(`${API_BASE}/trends/early-signals`);
      if (res.ok) {
        const data = await res.json();
        renderEarlySignals(data.early_signals || []);
        return;
      }
    } else if (currentTab === "opps") {
      const res = await fetch(`${API_BASE}/opportunities?limit=6`);
      if (res.ok) {
        const data = await res.json();
        renderOpportunities(data.top_opportunities || []);
        return;
      }
    } else if (currentTab === "create") {
      renderCreateComposer();
      return;
    }
  } catch (err) {
    container.innerHTML = `
      <div style='padding: 20px; text-align: center; color: #fb7185; font-size: 11px;'>
        <strong>Backend Unavailable</strong><br/>
        <span style="color: #94a3b8; font-size: 10px;">FastAPI server offline on port 8000.</span>
      </div>
    `;
  }
}

function renderLiveEvents(events) {
  if (!events.length) {
    container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>No live events detected yet.</div>";
    return;
  }

  container.innerHTML = "";
  events.forEach(ev => {
    const card = document.createElement("div");
    card.className = "card";
    const pillClass = ev.status === "CONFIRMED" ? "pill-confirmed" : "pill-exploding";
    card.innerHTML = `
      <div class="card-top">
        <span class="pill ${pillClass}">${ev.status} (${ev.confidence_score}%)</span>
        <span style="font-size: 10px; color: #94a3b8; font-family: monospace;">Time-to-Radar: ${ev.total_pipeline_latency || 28}s</span>
      </div>
      <div class="card-title">${ev.title}</div>
      <div class="card-desc">${ev.summary.slice(0, 140)}...</div>
      <div class="card-meta">
        <span>Sources: ${ev.source_count}</span>
        <button class="btn-create" onclick="openStudioFromExt('${encodeURIComponent(ev.title)}')">Create Post</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderEarlySignals(signals) {
  if (!signals.length) {
    container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>No early signals detected.</div>";
    return;
  }

  container.innerHTML = "";
  signals.forEach(sig => {
    const card = document.createElement("div");
    card.className = "card";
    const es = sig.early_signal || {};
    card.innerHTML = `
      <div class="card-top">
        <span class="pill pill-exploding">${es.trajectory || "EXPLODING"}</span>
        <span style="font-size: 10px; color: #fbbf24; font-family: monospace; font-weight: bold;">Prob: ${es.explosion_probability || 85}%</span>
      </div>
      <div class="card-title">${sig.topic}</div>
      <div class="card-desc">Category: ${sig.category} • Acceleration: +${es.acceleration_pct || 120}%</div>
      <div class="card-meta">
        <span>Competition: ${es.competition_score || 25}/100</span>
        <button class="btn-create" onclick="openStudioFromExt('${encodeURIComponent(sig.topic)}')">Exploit Angle</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderOpportunities(opps) {
  if (!opps.length) {
    container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>No opportunities calculated.</div>";
    return;
  }

  container.innerHTML = "";
  opps.forEach(opp => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="card-top">
        <span class="pill pill-confirmed">${opp.recommended_action || "POST NOW"}</span>
        <span style="font-size: 10px; color: #34d399; font-family: monospace; font-weight: bold;">Opp: ${opp.opportunity_score}/100</span>
      </div>
      <div class="card-title">${opp.topic}</div>
      <div class="card-desc"><strong>Angle:</strong> ${opp.recommended_angle || "Architectural impact"}</div>
      <div class="card-meta">
        <span>Fit: ${opp.primary_audience || "Engineers"}</span>
        <button class="btn-create" onclick="openStudioFromExt('${encodeURIComponent(opp.topic)}')">Synthesize</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderCreateComposer() {
  container.innerHTML = `
    <div style="padding: 10px; display: flex; flex-direction: column; gap: 10px;">
      <div style="font-size: 11px; font-weight: bold; color: #fff;">Quick Content Generator</div>
      <input id="ext-topic-input" type="text" placeholder="Enter topic or URL (e.g. Claude 3.7)" style="width: 100%; background: #131a2e; border: 1px solid #1e294b; border-radius: 6px; padding: 8px; color: #fff; font-size: 11px;" />
      <button id="ext-gen-btn" class="btn-create" style="padding: 8px; font-size: 11px;">Generate 10 Hooks & Post</button>
      <div id="ext-result" style="display: none; background: #070a12; border: 1px solid #1e294b; border-radius: 6px; padding: 10px; font-size: 11px; color: #e2e8f0; white-space: pre-wrap;"></div>
    </div>
  `;

  document.getElementById("ext-gen-btn").addEventListener("click", async () => {
    const topic = document.getElementById("ext-topic-input").value;
    if (!topic) return;
    const resDiv = document.getElementById("ext-result");
    resDiv.style.display = "block";
    resDiv.innerText = "Generating multi-platform content suite...";

    try {
      const res = await fetch(`${API_BASE}/content/all`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ canonical_title: topic })
      });
      if (res.ok) {
        const data = await res.json();
        const post = data.suite.x_content.single_post;
        resDiv.innerText = post;
      }
    } catch (e) {
      resDiv.innerText = "Generation failed. Ensure backend is running.";
    }
  });
}

window.openStudioFromExt = function(encodedTopic) {
  window.open(`http://localhost:5173/?topic=${encodedTopic}`, "_blank");
};

// Initial load
loadCurrentView();
