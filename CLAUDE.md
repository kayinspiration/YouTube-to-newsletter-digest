# Learn From Youtube

One-command pipeline: paste a YouTube URL, get a publication-ready HTML newsletter.

## Primary Workflow

Use `/digest <youtube-url>` to generate a newsletter. See `.claude/commands/digest.md`.

## Transcript Extraction

`scripts/extract-transcript.py` requires `youtube-transcript-api` (install via `scripts/install-dependencies.sh`).

## Output

Newsletters are saved to `output/YYYY-MM-DD/{slug}-newsletter.html`.
Cleaned transcripts are saved alongside as `{guest-slug}-transcript.docx`.

## Skill File

The full skill spec lives in `docs/youtube-summary.skill` (ZIP archive containing `youtube-summary/SKILL.md`).

## Content Guidelines

**Transcript-first:** Re-read the transcript before composing. Use the speaker's actual language and phrasing. Preserve specifics: tools named, numbers cited, stories told. The newsletter should feel like you were in the room.

**Flexible structure:** Choose the format that fits the episode:
- **Q&A** — interview-style with clear back-and-forth
- **Narrative** — one big thesis developed progressively
- **Tutorial** — how-to or process breakdowns
- **Debate** — multi-guest, surface tension and disagreements
- **Hybrid** — mix freely (narrative intro + Q&As + checklist)

**No limits:** Cover the episode exhaustively. There is NO cap on Q&As or sections. Each Q&A answer should be 3-8+ sentences grounded in the transcript.

**Screenshots are mandatory:** Always capture 6-10 screenshots from key video moments using Playwright MCP. Seek the video to specific timestamps, capture frames, convert to base64, and embed inside Q&A answers using `.slide-wrapper` / `.slide-img`. Screenshots make newsletters dramatically more engaging — aim for at least 1 per thematic section. The HTML must remain self-contained (base64 data URIs, no external image files).

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
2. **Results banner** — horizontal flex row of 3–4 key stats (big orange numbers)
3. **Core message cards** — 2-column grid, 3–5 cards with `.core-card-tag`, last odd card spans full width
4. **Thematic sections** — Q&As grouped into `<section class="section">` blocks, each with `section-label` (PART N), `section-title`, `section-desc`, and a `qa-list`
5. **Highlight boxes** — green ACTION callouts inside Q&A answers where actionable advice appears
6. **Pull quotes** — distributed within sections (not just at the end) for visual rhythm
7. **Action plan** — `.phase-list` with `.phase-badge` (STEP 1–N) steps at the end
8. **Final pull quote** — single best quotable line, Lora italic, blue left border

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

### Results Banner HTML

```html
<div class="results-banner">
  <div class="result-item">
    <span class="result-num">[big number]</span>
    <span class="result-label">[short label]</span>
  </div>
  <!-- 3-4 items -->
</div>
```

### Core Card HTML

```html
<div class="core-card [full-width if last and odd]">
  <span class="core-card-tag">[CATEGORY LABEL]</span>
  <span class="core-card-icon">[emoji]</span>
  <div class="core-card-title">[Short title]</div>
  <div class="core-card-desc">[2-3 sentence description]</div>
</div>
```

### Section HTML

```html
<section class="section">
  <div class="section-label">PART [N]</div>
  <h2 class="section-title">[Topic Title]</h2>
  <p class="section-desc">[Brief description of this section.]</p>
  <div class="qa-list">
    <!-- Q&A items for this topic -->
  </div>
  <!-- Optional: pull-quote within section -->
</section>
```

### Highlight Box HTML (inside `.qa-answer`)

```html
<div class="highlight-box">
  <p><strong>📌 ACTION:</strong> [actionable advice here]</p>
</div>
```

### Slide Wrapper HTML (images inside `.qa-answer`)

```html
<div class="slide-wrapper">
  <img class="slide-img" src="data:image/jpeg;base64,[DATA]" alt="[description]">
  <div class="slide-caption">[Caption describing the screenshot]</div>
</div>
```

### Phase List HTML (action plan)

```html
<div class="phase-list">
  <div class="phase-item">
    <span class="phase-badge">STEP [N]</span>
    <div class="phase-text"><strong>[Title]</strong> [Description]</div>
  </div>
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

/* Results Banner */
.results-banner {
  display: flex;
  gap: 0;
  background: linear-gradient(135deg, var(--accent-orange-light) 0%, #fff8f3 100%);
  border: 1px solid #f0d4bb;
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.result-item {
  flex: 1;
  min-width: 100px;
  text-align: center;
  padding: 8px 12px;
  border-right: 1px solid rgba(217,115,13,0.2);
}

.result-item:last-child { border-right: none; }

.result-num {
  font-size: 22px;
  font-weight: 700;
  color: var(--accent-orange);
  display: block;
  line-height: 1.2;
}

.result-label {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 4px;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Sections */
.section { margin-bottom: 36px; }

.section-title {
  font-family: 'Lora', Georgia, serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  line-height: 1.35;
}

.section-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 18px;
}

/* Core Card Tag */
.core-card-tag {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: var(--tag-bg);
  color: var(--text-muted);
  border-radius: 4px;
  padding: 2px 6px;
  margin-bottom: 6px;
}

/* Highlight Box */
.highlight-box {
  background: var(--accent-green-light);
  border: 1px solid #a8d9d2;
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  margin-top: 14px;
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.65;
}

.highlight-box strong { color: var(--accent-green); }

/* Slide Wrapper */
.slide-wrapper {
  margin: 14px 0;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border);
}

.slide-img {
  width: 100%;
  display: block;
}

.slide-caption {
  padding: 8px 14px;
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-soft);
  border-top: 1px solid var(--border-soft);
}

/* Phase List */
.phase-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}

.phase-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 18px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}

.phase-badge {
  font-size: 11px;
  font-weight: 700;
  background: var(--accent-blue-light);
  color: var(--accent-blue);
  border-radius: 4px;
  padding: 3px 8px;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 1px;
}

.phase-text {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.55;
}

.phase-text strong { color: var(--text-primary); font-weight: 600; }
```

### Quality Checklist

Before saving any newsletter, verify:
- [ ] `noembed` metadata fetched (or user-provided info used)
- [ ] Header h1 has `<em>` wrapping the most evocative phrase
- [ ] `.header-meta` is `flex-direction: column` — chips row above button
- [ ] "Watch on YouTube" button links to the actual YouTube URL
- [ ] Results banner has 3-4 key stats from the episode
- [ ] Q&As are organized into thematic `<section>` blocks (PART 1, 2, etc.)
- [ ] All Q&As are substantive (not generic filler)
- [ ] Highlight boxes with ACTION callouts in relevant Q&A answers
- [ ] Pull quotes distributed within sections, plus final pull quote
- [ ] Action plan uses `.phase-list` with concrete steps
- [ ] Core cards have `.core-card-tag` labels
- [ ] Pull quote is a real, quotable line (not a summary)
- [ ] 6-10 screenshots captured via Playwright and embedded as base64 `.slide-wrapper` / `.slide-img` / `.slide-caption`
- [ ] At least 1 screenshot per thematic section, placed contextually inside Q&A answers
- [ ] HTML is self-contained (no external CSS other than Google Fonts, images as base64 data URIs)
- [ ] File saved to `output/YYYY-MM-DD/{slug}-newsletter.html`
