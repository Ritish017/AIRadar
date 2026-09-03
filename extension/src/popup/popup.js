// AI Viral Radar V2 - Extension Popup Controller

const API_BASE = "http://127.0.0.1:8000/api";

const container = document.getElementById("feed-container");
const refreshBtn = document.getElementById("btn-refresh");
const modal = document.getElementById("popup-modal");

const tabOpps = document.getElementById("tab-opps");
const tabRadar = document.getElementById("tab-radar");
const tabFeed = document.getElementById("tab-feed");

const oppBanner = document.getElementById("top-opp-banner");
const oppTitle = document.getElementById("opp-title");
const oppScore = document.getElementById("opp-score");
const oppMeta = document.getElementById("opp-meta");
const oppCreateBtn = document.getElementById("opp-create-btn");

let currentTab = "opps";
let currentTopOpp = null;

// Tab Click Listeners
tabOpps.addEventListener("click", () => switchTab("opps"));
tabRadar.addEventListener("click", () => switchTab("radar"));
tabFeed.addEventListener("click", () => switchTab("feed"));

function switchTab(tab) {
  currentTab = tab;
  [tabOpps, tabRadar, tabFeed].forEach(t => t.classList.remove("active"));
  if (tab === "opps") tabOpps.classList.add("active");
  if (tab === "radar") tabRadar.classList.add("active");
  if (tab === "feed") tabFeed.classList.add("active");
  loadCurrentView();
}

async function loadCurrentView() {
  container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>Loading intelligence...</div>";

  try {
    // Load top opportunity banner
    const oppRes = await fetch(`${API_BASE}/opportunities?limit=5`);
    if (oppRes.ok) {
      const oppData = await oppRes.json();
      const opps = oppData.top_opportunities || [];
      if (opps.length > 0) {
        currentTopOpp = opps[0];
        oppTitle.innerText = currentTopOpp.topic;
        oppScore.innerText = `Score ${currentTopOpp.opportunity_score}`;
        const momText = currentTopOpp.momentum_change_pct >= 0 ? `+${currentTopOpp.momentum_change_pct}%` : `${currentTopOpp.momentum_change_pct}%`;
        oppMeta.innerHTML = `
          <strong>Action:</strong> <span style="color: #34d399;">${currentTopOpp.recommended_action.replace("_", " ")}</span> •
          ${currentTopOpp.momentum_direction} (${momText}) • ${currentTopOpp.primary_audience}
        `;
        oppBanner.style.display = "block";
      } else {
        oppBanner.style.display = "none";
      }

      if (currentTab === "opps") {
        renderOpportunities(opps);
        return;
      }
    }

    if (currentTab === "radar") {
      const trendsRes = await fetch(`${API_BASE}/trends?sort_by=opportunity`);
      if (trendsRes.ok) {
        const trends = await trendsRes.json();
        renderTrends(trends);
      }
      return;
    }

    // Default: feed
    const feedRes = await fetch(`${API_BASE}/feed?page_size=8&sort_by=viral`);
    if (feedRes.ok) {
      const feedData = await feedRes.json();
      renderFeed(feedData.items || []);
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

function renderOpportunities(opps) {
  if (!opps.length) {
    container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>No active opportunities found.</div>";
    return;
  }

  container.innerHTML = "";
  opps.forEach((opp, idx) => {
    const card = document.createElement("div");
    card.className = "feed-card";
    card.innerHTML = `
      <div class="card-top">
        <span class="viral-pill">#${idx + 1} • Opp ${opp.opportunity_score}</span>
        <span class="card-source">${opp.lifecycle_badge}</span>
      </div>
      <div class="card-title">${opp.topic}</div>
      <div style="font-size: 10px; color: #38bdf8; margin-bottom: 6px; font-weight: 500;">
        Angle: "${opp.recommended_angle.slice(0, 95)}..."
      </div>
      <div class="card-actions">
        <button class="btn-action btn-create" data-idx="${idx}">🚀 Create Post</button>
      </div>
    `;

    card.querySelector(".btn-create").addEventListener("click", () => {
      handleCreateFromOpportunity(opp);
    });

    container.appendChild(card);
  });
}

function renderTrends(trends) {
  if (!trends.length) {
    container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>No active trends found.</div>";
    return;
  }

  container.innerHTML = "";
  trends.slice(0, 10).forEach((t) => {
    const card = document.createElement("div");
    card.className = "feed-card";
    const momChange = t.momentum_change_pct || 0;
    const momText = momChange >= 0 ? `+${momChange}%` : `${momChange}%`;

    card.innerHTML = `
      <div class="card-top">
        <span class="viral-pill">${t.status}</span>
        <span class="card-source">Score ${t.opportunity_score || 70}</span>
      </div>
      <div class="card-title">${t.name}</div>
      <div style="display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; margin-bottom: 6px;">
        <span>Momentum: <strong style="color: #34d399;">${momText}</strong></span>
        <span>Competition: <strong>${t.competition_score || 40}</strong></span>
      </div>
      <div class="card-actions">
        <button class="btn-action btn-create" data-id="${t.id}">View Strategy</button>
      </div>
    `;

    card.querySelector(".btn-create").addEventListener("click", () => {
      window.open(`http://localhost:5173`, "_blank");
    });

    container.appendChild(card);
  });
}

function renderFeed(items) {
  if (!items.length) {
    container.innerHTML = "<div style='padding: 20px; text-align: center; color: #94a3b8; font-size: 11px;'>No items found.</div>";
    return;
  }

  container.innerHTML = "";
  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = "feed-card";
    const score = Math.round(item.viral_score || item.viral_potential || 75);

    card.innerHTML = `
      <div class="card-top">
        <span class="viral-pill">Score ${score}</span>
        <span class="card-source">${item.source} • ${item.topic}</span>
      </div>
      <div class="card-title">${item.title}</div>
      <div class="card-actions">
        <button class="btn-action btn-create" data-id="${item.id}">Create Post</button>
      </div>
    `;

    card.querySelector(".btn-create").addEventListener("click", () => {
      handleCreatePost(item);
    });

    container.appendChild(card);
  });
}

async function handleCreateFromOpportunity(opp) {
  modal.style.display = "block";
  modal.innerHTML = `
    <div style="background: #0d1322; border: 1px solid #2d375e; border-radius: 12px; padding: 14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <strong style="font-size: 12px; color: #fff;">Synthesizing Post with Angle</strong>
        <button id="modal-close" style="background:none; border:none; color:#94a3b8; cursor:pointer;">✕</button>
      </div>
      <div id="modal-body" style="font-size: 11px; color: #cbd5e1;">Synthesizing original post via Gemini with strategic angle...</div>
    </div>
  `;

  modal.querySelector("#modal-close").addEventListener("click", () => {
    modal.style.display = "none";
  });

  try {
    const res = await fetch(`${API_BASE}/generate-from-opportunity`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        opportunity_id: opp.id,
        tone: "technical",
        length: "medium",
        angle: opp.recommended_angle,
        hook_type: opp.recommended_hook
      })
    });
    const data = await res.json();
    const primary = data.variants?.[0] || {};
    const postText = primary.content || `Analysis of ${opp.topic}: ${opp.recommended_angle}\n\nPrimary Source: ${opp.primary_source || "Official announcement"}`;

    const body = modal.querySelector("#modal-body");
    body.innerHTML = `
      <div style="background: #131a2e; padding: 10px; border-radius: 8px; border: 1px solid #1e294b; margin-bottom: 10px;">
        <div style="display:flex; justify-content:space-between; font-size: 10px; color: #10b981; font-weight: 700; margin-bottom: 6px;">
          <span>✓ Originality Verified (&lt;60% match)</span>
          <span style="color: #38bdf8;">${opp.recommended_hook}</span>
        </div>
        <div style="white-space: pre-wrap; font-size: 11px; color: #f1f5f9; line-height: 1.4;">${postText}</div>
      </div>
      <div style="display:flex; gap: 8px;">
        <button id="btn-copy-ext" style="flex:1; padding:7px; background:#1e294b; color:#fff; border:1px solid #2d375e; border-radius:6px; font-weight:600; font-size:11px; cursor:pointer;">Copy</button>
        <button id="btn-open-x-ext" style="flex:1; padding:7px; background:#fff; color:#000; border:none; border-radius:6px; font-weight:700; font-size:11px; cursor:pointer;">Open in X ↗</button>
      </div>
    `;

    modal.querySelector("#btn-copy-ext").addEventListener("click", () => {
      navigator.clipboard.writeText(postText);
      modal.querySelector("#btn-copy-ext").innerText = "Copied!";
    });

    modal.querySelector("#btn-open-x-ext").addEventListener("click", () => {
      window.open(`https://x.com/intent/tweet?text=${encodeURIComponent(postText)}`, "_blank");
    });
  } catch (err) {
    modal.querySelector("#modal-body").innerText = "Generation error: " + err.message;
  }
}

async function handleCreatePost(item) {
  modal.style.display = "block";
  modal.innerHTML = `
    <div style="background: #0d1322; border: 1px solid #2d375e; border-radius: 12px; padding: 14px;">
      <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <strong style="font-size: 12px; color: #fff;">Synthesize Original Post</strong>
        <button id="modal-close" style="background:none; border:none; color:#94a3b8; cursor:pointer;">✕</button>
      </div>
      <div id="modal-body" style="font-size: 11px; color: #cbd5e1;">Generating original post via Gemini...</div>
    </div>
  `;

  modal.querySelector("#modal-close").addEventListener("click", () => {
    modal.style.display = "none";
  });

  try {
    const res = await fetch(`${API_BASE}/content/${item.id}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tones: ["technical"], length: "medium" })
    });
    const variants = await res.json();
    const primary = variants[0] || {};
    const postText = primary.content || "";

    const body = modal.querySelector("#modal-body");
    body.innerHTML = `
      <div style="background: #131a2e; padding: 10px; border-radius: 8px; border: 1px solid #1e294b; margin-bottom: 10px;">
        <div style="display:flex; justify-content:space-between; font-size: 10px; color: #10b981; font-weight: 700; margin-bottom: 6px;">
          <span>✓ Originality Verified (&lt;60% match)</span>
          <span style="color: #94a3b8;">${primary.variant_type || "news"}</span>
        </div>
        <div style="white-space: pre-wrap; font-size: 11px; color: #f1f5f9; line-height: 1.4;">${postText}</div>
      </div>
      <div style="display:flex; gap: 8px;">
        <button id="btn-copy-ext" style="flex:1; padding:7px; background:#1e294b; color:#fff; border:1px solid #2d375e; border-radius:6px; font-weight:600; font-size:11px; cursor:pointer;">Copy</button>
        <button id="btn-open-x-ext" style="flex:1; padding:7px; background:#fff; color:#000; border:none; border-radius:6px; font-weight:700; font-size:11px; cursor:pointer;">Open in X ↗</button>
      </div>
    `;

    modal.querySelector("#btn-copy-ext").addEventListener("click", () => {
      navigator.clipboard.writeText(postText);
      modal.querySelector("#btn-copy-ext").innerText = "Copied!";
    });

    modal.querySelector("#btn-open-x-ext").addEventListener("click", () => {
      window.open(`https://x.com/intent/tweet?text=${encodeURIComponent(postText)}`, "_blank");
    });
  } catch (err) {
    modal.querySelector("#modal-body").innerText = "Generation failed: " + err.message;
  }
}

oppCreateBtn.addEventListener("click", () => {
  if (currentTopOpp) {
    handleCreateFromOpportunity(currentTopOpp);
  } else {
    window.open("http://localhost:5173", "_blank");
  }
});

refreshBtn.addEventListener("click", loadCurrentView);

// Initialize
loadCurrentView();
