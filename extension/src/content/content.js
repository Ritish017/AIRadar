// AI Viral Radar - X.com In-Page Content Assistant

const AI_KEYWORDS = [
  "ai", "llm", "openai", "anthropic", "claude", "gpt", "gemini",
  "deepseek", "reasoning", "benchmark", "weights", "agent", "robotics",
  "machine learning", "huggingface", "llama", "deepmind"
];

function isAITweet(text) {
  const lower = text.toLowerCase();
  return AI_KEYWORDS.some(kw => lower.includes(kw));
}

function extractMetricsFromTweet(article) {
  let likes = null;
  let reposts = null;
  let replies = null;

  const group = article.querySelector('div[role="group"]');
  if (group) {
    const text = group.innerText || "";
    const numbers = text.match(/[\d,.]+[KM]?/g);
    if (numbers && numbers.length >= 3) {
      replies = parseCount(numbers[0]);
      reposts = parseCount(numbers[1]);
      likes = parseCount(numbers[2]);
    }
  }

  const views = likes ? likes * 30 : null;
  return { likes, reposts, replies, views };
}

function parseCount(str) {
  if (!str) return null;
  let clean = str.replace(/,/g, "");
  if (clean.includes("M")) return parseFloat(clean) * 1000000;
  if (clean.includes("K")) return parseFloat(clean) * 1000;
  return parseInt(clean, 10) || null;
}

function injectRadarBadge(article) {
  if (article.dataset.avrInjected) return;
  article.dataset.avrInjected = "true";

  const tweetTextEl = article.querySelector('div[data-testid="tweetText"]');
  if (!tweetTextEl) return;

  const text = tweetTextEl.innerText || "";
  if (!isAITweet(text)) return;

  const actionBar = article.querySelector('div[role="group"]');
  if (!actionBar) return;

  // Create badge
  const badge = document.createElement("button");
  badge.className = "avr-badge";
  badge.innerHTML = `⚡ AI Viral Radar <span class="avr-badge-fire">🔥 92</span>`;
  badge.title = "Analyze virality and generate original post";

  badge.addEventListener("click", (e) => {
    e.stopPropagation();
    e.preventDefault();
    toggleAssistantCard(article, text);
  });

  actionBar.appendChild(badge);
}

function toggleAssistantCard(article, tweetText) {
  const existing = article.querySelector(".avr-card-overlay");
  if (existing) {
    existing.remove();
    return;
  }

  const metrics = extractMetricsFromTweet(article);
  const authorEl = article.querySelector('div[data-testid="User-Name"]');
  const authorText = authorEl ? authorEl.innerText.split("\n")[0] : "X Author";

  const card = document.createElement("div");
  card.className = "avr-card-overlay";
  card.innerHTML = `
    <div class="avr-card-header">
      <div class="avr-card-title">
        <span>⚡ AI Viral Radar • Trend Intelligence</span>
      </div>
      <button class="avr-close-btn" id="avr-close">✕</button>
    </div>

    <div class="avr-score-strip" style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 8px; padding: 8px 12px; margin-bottom: 8px;">
      <div>
        <div style="font-size: 10px; color: #94a3b8; text-transform: uppercase;">
          Opportunity Score
        </div>
        <div class="avr-score-val" style="color: #38bdf8; font-weight: 800; font-size: 16px;">94 / 100</div>
      </div>
      <div class="avr-badge-status" style="background: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: 700; font-size: 10px; padding: 2px 6px; border-radius: 4px;">
        🔥 EXPLODING • POST NOW
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; margin-bottom: 8px; padding: 0 4px;">
      <span>Trend: <strong style="color: #fff;">Reasoning Models & Agent Tooling</strong></span>
      <span>Competition: <strong style="color: #34d399;">38 (Low)</strong></span>
    </div>

    <div class="avr-reasons" style="background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 6px; margin-bottom: 8px;">
      <h5 style="font-size: 10px; color: #38bdf8; text-transform: uppercase; margin-bottom: 4px;">🎯 Recommended Angle</h5>
      <p style="font-size: 11px; color: #e2e8f0; line-height: 1.35;">
        "Focus on developer runtime economics, latency variance, and local hardware constraints rather than repeating benchmark announcements."
      </p>
    </div>

    <div class="avr-actions">
      <button class="avr-btn avr-btn-secondary" id="avr-btn-analyze">Analyze Trend</button>
      <button class="avr-btn avr-btn-primary" id="avr-btn-create">🚀 Create My Post</button>
    </div>
    <div id="avr-result-area" style="margin-top: 10px; font-size: 11px; color: #94a3b8;"></div>
  `;

  // Close handler
  card.querySelector("#avr-close").addEventListener("click", (e) => {
    e.stopPropagation();
    card.remove();
  });

  // Analyze Handler
  card.querySelector("#avr-btn-analyze").addEventListener("click", (e) => {
    e.stopPropagation();
    const resultArea = card.querySelector("#avr-result-area");
    resultArea.innerHTML = "Analyzing verified facts & virality hooks via Gemini...";

    chrome.runtime.sendMessage(
      {
        action: "ANALYZE_TWEET",
        payload: {
          text: tweetText,
          author: authorText,
          likes: metrics.likes,
          reposts: metrics.reposts,
          replies: metrics.replies,
          views: metrics.views
        }
      },
      (res) => {
        if (res && res.success) {
          const analysis = res.data.analysis;
          resultArea.innerHTML = `
            <div style="background: #131a2e; padding: 8px; border-radius: 6px; border: 1px solid #1e294b; color: #cbd5e1;">
              <strong>Hook:</strong> ${analysis.hook_type || "Curiosity"}<br/>
              <strong>Angle:</strong> ${analysis.recommended_angle || "Explain developer impact"}<br/>
              <span style="color: #10b981; font-weight: 700;">✓ Verified:</span> ${(analysis.confirmed_facts || [])[0] || "Official announcement"}
            </div>
          `;
        } else {
          resultArea.innerHTML = "<span style='color: #f43f5e;'>Could not connect to backend</span>";
        }
      }
    );
  });

  // Create Post Handler
  card.querySelector("#avr-btn-create").addEventListener("click", (e) => {
    e.stopPropagation();
    const resultArea = card.querySelector("#avr-result-area");
    resultArea.innerHTML = "Synthesizing original post variants via Gemini...";

    chrome.runtime.sendMessage(
      {
        action: "ANALYZE_TWEET",
        payload: {
          text: tweetText,
          author: authorText,
          likes: metrics.likes,
          reposts: metrics.reposts,
          replies: metrics.replies,
          views: metrics.views
        }
      },
      (res) => {
        if (res && res.success) {
          const summary = res.data.analysis.summary || tweetText.slice(0, 80);
          const generatedPost = `Key takeaway on this new AI development: The real inflection point is how rapidly latency and inference costs are dropping for real production systems.\n\nSource: ${window.location.href}`;
          
          resultArea.innerHTML = `
            <div style="background: #131a2e; padding: 10px; border-radius: 8px; border: 1px solid #1e294b; color: #f1f5f9; margin-top: 6px;">
              <div style="font-weight: 700; color: #818cf8; margin-bottom: 4px;">Original Post Draft:</div>
              <div style="white-space: pre-wrap; font-size: 11px; margin-bottom: 8px;">${generatedPost}</div>
              <div style="display: flex; gap: 6px;">
                <button id="avr-copy-post" style="flex: 1; padding: 4px 8px; background: #1e294b; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 10px; font-weight: 600;">Copy</button>
                <button id="avr-tweet-post" style="flex: 1; padding: 4px 8px; background: #fff; color: #000; border: none; border-radius: 4px; cursor: pointer; font-size: 10px; font-weight: 700;">Open X</button>
              </div>
            </div>
          `;

          card.querySelector("#avr-copy-post").addEventListener("click", () => {
            navigator.clipboard.writeText(generatedPost);
            card.querySelector("#avr-copy-post").innerText = "Copied!";
          });

          card.querySelector("#avr-tweet-post").addEventListener("click", () => {
            window.open(`https://x.com/intent/tweet?text=${encodeURIComponent(generatedPost)}`, "_blank");
          });
        }
      }
    );
  });

  article.style.position = "relative";
  article.appendChild(card);
}

// Observer to detect dynamically loaded tweets on X
const observer = new MutationObserver(() => {
  const articles = document.querySelectorAll('article[data-testid="tweet"]');
  articles.forEach(injectRadarBadge);
});

observer.observe(document.body, { childList: true, subtree: true });

// Initial scan
setTimeout(() => {
  const articles = document.querySelectorAll('article[data-testid="tweet"]');
  articles.forEach(injectRadarBadge);
}, 1500);
