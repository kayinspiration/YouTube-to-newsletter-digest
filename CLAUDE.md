# Learn From Youtube

One-command pipeline: paste a YouTube URL, get a publication-ready HTML newsletter.

## Primary Workflow

Use `/digest <youtube-url>` to generate a newsletter. See `.claude/commands/digest.md`.

## Transcript Extraction

`scripts/extract-transcript.py` requires `youtube-transcript-api` (install via `scripts/install-dependencies.sh`).

## Output

Newsletters are saved to `output/YYYY-MM-DD/{slug}-newsletter.html`.

---

## Newsletter Design System

This is the complete design spec for all generated newsletters. Every HTML newsletter MUST use these exact styles and structure.

### Design Tokens

```
/* Claude palette — header */
--header-bg: linear-gradient(135deg, #141413 0%, #1c1410 55%, #251b0e 100%)
--header-dot: #d97757
--header-accent: #d97757
--header-btn-border: #c4623e
--header-text: #ffffff
--header-text-dim: rgba(255,255,255,0.6)
--header-chip-bg: rgba(255,255,255,0.08)
--header-chip-border: rgba(255,255,255,0.14)

/* Notion palette — body */
--bg: #ffffff
--bg-soft: #f7f6f3
--bg-hover: #efeeeb
--border: #e8e7e3
--text-primary: #37352f
--text-secondary: #787774
--text-muted: #b5b3ad

/* Body accent colors */
--accent-blue: #2383e2 / --accent-blue-light: #e8f1fb
--accent-orange: #d9730d / --accent-orange-light: #fbecdd
--accent-green: #0f7b6c / --accent-green-light: #dcf3ef
--accent-purple: #6940a5 / --accent-purple-light: #f3effe
```

### Fonts

- Google Fonts: `Inter` (300–700) for UI, `Lora` (400, 600, italic 400) for headings and quotes
- Body: `'Inter', -apple-system, sans-serif`
- Header h1 and pull quotes: `'Lora', Georgia, serif`
- Font link: `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap`

### Page Structure

```html
<body>                         <!-- bg: #f2f1ed, padding: 40px 20px 80px -->
  <div class="page">           <!-- max-width: 720px, bg: white, border-radius: 14px -->
    <div class="header"> ... </div>
    <div class="body"> ... </div>
  </div>
</body>
```

### Header Block

```html
<div class="header">
  <div class="header-tag">
    <span class="header-dot"></span>
    AI UX WEEKLY
  </div>
  <h1>[Title with <em>key phrase</em> italicized]</h1>
  <p class="header-subtitle">[2-sentence subtitle]</p>
  <div class="header-meta">
    <div class="meta-chips">
      <span class="meta-chip">[guest SVG] [Guest x Host]</span>
      <span class="meta-chip">[calendar SVG] [Month Year]</span>
      <span class="meta-chip">[clock SVG] ~[N] min episode</span>
    </div>
    <a class="header-watch-btn" href="[youtube-url]" target="_blank">
      <svg width="13" height="13" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
      Watch on YouTube
    </a>
  </div>
</div>
```

**Critical:** `.header-meta` uses `flex-direction: column; align-items: flex-start`. Chips row above button — never inline.

### Body Block

Contains (in order):
1. **Intro callout** — emoji + 2–3 sentences on why this episode matters
2. **Core message cards** — 2-column grid, 3–5 cards, last odd card spans full width
3. **Section divider + label** — `KEY TAKEAWAYS` or `10 QUESTIONS`
4. **10 Q&A items** — each `.qa-item` with `.qa-question` and `.qa-answer`
5. **Pull quote** — single best quotable line, Lora italic, blue left border

### Q&A Item HTML

```html
<div class="qa-item">
  <div class="qa-question">
    <span class="qa-num">Q[N]</span>
    <span class="qa-q-text">[Question text]</span>
  </div>
  <div class="qa-answer">
    <p>[Answer paragraph]</p>
  </div>
</div>
```

### Core Card HTML

```html
<div class="core-card [full-width if last and odd]">
  <span class="core-card-icon">[emoji]</span>
  <div class="core-card-title">[Short title]</div>
  <div class="core-card-desc">[2-3 sentence description]</div>
</div>
```

### Pull Quote HTML

```html
<div class="pull-quote">
  <p>"[Quote text]"</p>
  <cite>— [Guest name], [Role]</cite>
</div>
```

### Full CSS

Paste this inside `<style>` in the `<head>`:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #ffffff;
  --bg-soft: #f7f6f3;
  --bg-hover: #efeeeb;
  --border: #e8e7e3;
  --border-soft: #f0efec;
  --text-primary: #37352f;
  --text-secondary: #787774;
  --text-muted: #b5b3ad;
  --accent-blue: #2383e2;
  --accent-blue-light: #e8f1fb;
  --accent-orange: #d9730d;
  --accent-orange-light: #fbecdd;
  --accent-green: #0f7b6c;
  --accent-green-light: #dcf3ef;
  --accent-purple: #6940a5;
  --accent-purple-light: #f3effe;
  --accent-red: #e03e3e;
  --accent-red-light: #fbe4e4;
  --accent-yellow: #dfab01;
  --accent-yellow-light: #fef3cd;
  --tag-bg: #f1f0ed;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
  --radius: 6px;
  --radius-lg: 10px;
}

html { font-size: 16px; scroll-behavior: smooth; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f2f1ed;
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
  padding: 40px 20px 80px;
}

.page {
  max-width: 720px;
  margin: 0 auto;
  background: var(--bg);
  border-radius: 14px;
  box-shadow: var(--shadow-md), 0 0 0 1px rgba(0,0,0,0.04);
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #141413 0%, #1c1410 55%, #251b0e 100%);
  padding: 52px 56px 44px;
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.header-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.18);
  color: rgba(255,255,255,0.8);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 100px;
  margin-bottom: 20px;
}

.header-dot {
  width: 6px; height: 6px;
  background: #d97757;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.85); }
}

.header h1 {
  font-family: 'Lora', Georgia, serif;
  font-size: 30px;
  font-weight: 600;
  color: #fff;
  line-height: 1.3;
  margin-bottom: 14px;
  letter-spacing: -0.3px;
}

.header h1 em {
  font-style: italic;
  color: #d97757;
}

.header-subtitle {
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  line-height: 1.6;
  max-width: 500px;
  margin-bottom: 28px;
}

.header-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 14px;
}

.meta-chips {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.meta-chip {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 100px;
  padding: 5px 12px;
  font-size: 12px;
  color: rgba(255,255,255,0.75);
}

.meta-chip svg { opacity: 0.7; flex-shrink: 0; }

.header-watch-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #d97757;
  border: 1px solid #c4623e;
  color: #faf9f5;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  padding: 7px 16px;
  border-radius: 6px;
  transition: background 0.15s, box-shadow 0.15s;
}

.header-watch-btn:hover {
  background: #c4623e;
  box-shadow: 0 0 0 3px rgba(217,119,87,0.3);
}

.body { padding: 0 56px 56px; }

.divider {
  height: 1px;
  background: var(--border);
  margin: 32px 0;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 18px;
}

.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.callout {
  display: flex;
  gap: 14px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  margin-bottom: 28px;
}

.callout-icon { font-size: 20px; flex-shrink: 0; margin-top: 1px; }

.callout-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.65;
}

.callout-text strong { color: var(--text-primary); font-weight: 600; }

.core-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 8px;
}

.core-card {
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  transition: box-shadow 0.15s, border-color 0.15s;
}

.core-card:hover {
  box-shadow: var(--shadow-sm);
  border-color: #d0cfcb;
}

.core-card-icon { font-size: 22px; margin-bottom: 10px; display: block; }
.core-card-title { font-size: 13.5px; font-weight: 600; color: var(--text-primary); margin-bottom: 6px; line-height: 1.3; }
.core-card-desc { font-size: 12.5px; color: var(--text-secondary); line-height: 1.6; }
.core-card.full-width { grid-column: span 2; }

.pull-quote {
  border-left: 3px solid var(--accent-blue);
  padding: 14px 20px;
  margin: 28px 0;
  background: var(--accent-blue-light);
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
}

.pull-quote p {
  font-family: 'Lora', Georgia, serif;
  font-size: 16px;
  font-style: italic;
  color: var(--text-primary);
  line-height: 1.65;
}

.pull-quote cite {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  font-style: normal;
  font-weight: 500;
}

.qa-list { display: flex; flex-direction: column; gap: 0; }

.qa-item {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: box-shadow 0.15s;
  margin-bottom: 12px;
}

.qa-item:hover { box-shadow: var(--shadow-sm); }

.qa-question {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px 20px;
  background: var(--bg);
  cursor: default;
}

.qa-num {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--accent-blue);
  background: var(--accent-blue-light);
  border-radius: 4px;
  padding: 3px 7px;
  flex-shrink: 0;
  margin-top: 1px;
}

.qa-q-text {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.45;
}

.qa-answer {
  padding: 0 20px 18px 20px;
  background: var(--bg-soft);
  border-top: 1px solid var(--border-soft);
}

.qa-answer p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  padding-top: 14px;
}

.qa-answer p + p { padding-top: 10px; }
```

### Quality Checklist

Before saving any newsletter, verify:
- [ ] `noembed` metadata fetched (or user-provided info used)
- [ ] Header h1 has `<em>` wrapping the most evocative phrase
- [ ] `.header-meta` is `flex-direction: column` — chips row above button
- [ ] "Watch on YouTube" button links to the actual YouTube URL
- [ ] All 10 Q&As are substantive (not generic filler)
- [ ] Pull quote is a real, quotable line (not a summary)
- [ ] HTML is self-contained (no external CSS other than Google Fonts)
- [ ] File saved to `output/YYYY-MM-DD/{slug}-newsletter.html`
