// AI Viral Radar - Background Service Worker (Manifest V3)

const DEFAULT_API_URL = "http://127.0.0.1:8000/api";

chrome.runtime.onInstalled.addListener(() => {
  console.log("AI Viral Radar extension installed.");
  chrome.storage.local.set({
    apiUrl: DEFAULT_API_URL,
    minViralScore: 70,
    preferredTone: "technical"
  });
  updateBadge();
});

// Update badge periodically or on demand
async function updateBadge() {
  try {
    const data = await chrome.storage.local.get(["apiUrl"]);
    const api = data.apiUrl || DEFAULT_API_URL;
    const res = await fetch(`${api}/trending`);
    if (res.ok) {
      const json = await res.json();
      const count = json.trending_items ? json.trending_items.length : 0;
      if (count > 0) {
        chrome.action.setBadgeText({ text: count.toString() });
        chrome.action.setBadgeBackgroundColor({ color: "#f43f5e" });
      } else {
        chrome.action.setBadgeText({ text: "" });
      }
    }
  } catch (err) {
    console.debug("Radar badge fetch error:", err);
  }
}

// Handle messages from content script or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "GET_CONFIG") {
    chrome.storage.local.get(["apiUrl", "minViralScore", "preferredTone"], (res) => {
      sendResponse(res);
    });
    return true;
  }

  if (message.action === "ANALYZE_TWEET") {
    (async () => {
      try {
        const data = await chrome.storage.local.get(["apiUrl"]);
        const api = data.apiUrl || DEFAULT_API_URL;
        const resp = await fetch(`${api}/analyze-custom-tweet`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(message.payload)
        });
        const result = await resp.json();
        sendResponse({ success: true, data: result });
      } catch (err) {
        sendResponse({ success: false, error: err.message });
      }
    })();
    return true;
  }

  if (message.action === "GENERATE_VARIANTS") {
    (async () => {
      try {
        const data = await chrome.storage.local.get(["apiUrl", "preferredTone"]);
        const api = data.apiUrl || DEFAULT_API_URL;
        const tone = message.tone || data.preferredTone || "technical";

        const resp = await fetch(`${api}/content/${message.contentId}/generate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            tones: [tone],
            length: message.length || "medium",
            include_voice_profile: true
          })
        });
        const result = await resp.json();
        sendResponse({ success: true, variants: result });
      } catch (err) {
        sendResponse({ success: false, error: err.message });
      }
    })();
    return true;
  }
});
