# AI Viral Radar — Chrome Extension Guide

The **AI Viral Radar Chrome Extension** is built natively on Chrome Manifest V3. It provides both a compact popup radar dashboard and an intelligent in-page assistant when browsing X (Twitter).

---

## 1. How to Load the Extension in Chrome

1. Open Google Chrome.
2. Navigate to `chrome://extensions/` in the URL address bar.
3. In the top-right corner, toggle **Developer mode** to **ON**.
4. Click the **Load unpacked** button in the top-left toolbar.
5. In the file picker, select the directory:
   ```
   c:\ViralConetntCreator\extension
   ```
6. The extension will appear as **AI Viral Radar** with the flame icon.
7. Click the extension puzzle icon in Chrome's toolbar and pin **AI Viral Radar** for fast access.

---

## 2. Extension Components & Architecture

```
extension/
├── manifest.json              # Manifest V3 configuration & permissions
├── icons/                     # 16px, 48px, 128px high-DPI icon assets
└── src/
    ├── background/
    │   └── background.js      # Service worker, badge count, API messaging
    ├── content/
    │   └── content.js         # X.com in-page assistant & DOM observer
    ├── popup/
    │   ├── popup.html         # Compact 380x560px radar popup interface
    │   └── popup.js           # Trending feeds, analyze, post generator
    ├── options/
    │   ├── options.html       # API endpoint, tone, and threshold settings
    │   └── options.js         # Chrome storage sync
    └── styles/
        └── content.css        # Scoped .avr-* styling for injected X widget
```

---

## 3. In-Page Assistant on X (`x.com`)

When you browse `x.com` or `twitter.com`:
1. The content script uses a `MutationObserver` to inspect visible tweets without blocking the page or degrading performance.
2. If a tweet discusses AI breakthroughs, models, or benchmarks, a subtle pill badge appears in the tweet's action bar:
   ```
   [ ⚡ AI Viral Radar  🔥 92 ]
   ```
3. Clicking the badge opens a non-intrusive floating card directly on the post:
   - Displays real-time Viral Score and momentum (`🔥 Exploding`).
   - Bulleted summary of why it's going viral.
   - `[Deep Analyze]` button to fetch structured AI breakdown.
   - `[Create My Post]` button to synthesize original post variants.
4. Clicking `[Open X]` launches X's official tweet composer pre-populated with your original synthesized post.

---

## 4. Security & Permissions

- **No Scraping of Private Endpoints**: Strictly passive DOM observation of already-rendered public text.
- **No Credential Access**: Does not access or store passwords, cookies, or authentication tokens.
- **No Remote Code Execution**: Zero `eval()` or arbitrary dynamic script loading; fully compliant with Google Chrome Web Store Manifest V3 security requirements.
- **Host Permissions**: Limited to `x.com`, `twitter.com`, and `http://127.0.0.1:8000/*` for local backend communication.
