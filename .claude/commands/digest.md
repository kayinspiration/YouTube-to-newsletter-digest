# YouTube-to-Newsletter Digest

Generate a publication-ready HTML newsletter from a YouTube video.

**Input URL:** $ARGUMENTS

---

## Pipeline Steps

Execute these steps in order:

### Step 1: Parse URL and Extract Video ID

Extract the YouTube video ID from the URL. Handle these formats:
- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`
- `youtube.com/embed/VIDEO_ID`

If the user provides a title/guest instead of a URL, skip noembed and proceed with what they gave.
If the input is not a valid YouTube URL or title, stop and ask for clarification.

### Step 2: Check Dependencies

Verify `youtube-transcript-api` is installed:
```bash
python3 -c "import youtube_transcript_api; print('OK')"
```
If not installed, run `bash scripts/install-dependencies.sh` first.

### Step 3: Fetch Episode Metadata

Use WebFetch to get metadata from noembed (YouTube is blocked directly):
```
https://noembed.com/embed?url=$ARGUMENTS
```

Extract from the response:
- **Episode title** — the main headline
- **Guest name(s)** — look for patterns like "x", "with", "ft.", "featuring" in the title
- **Channel/host name** — the `author_name` field
- **Thumbnail URL** — the `thumbnail_url` field

### Step 4: Extract Transcript

Run the transcript extraction script:
```bash
python3 scripts/extract-transcript.py VIDEO_ID en
```

Clean up the raw transcript:
- Join lines into flowing paragraphs (group by speaker turns or natural pauses)
- Remove filler artifacts like `[Music]`, `[Applause]`, repeated stutters
- Preserve timestamps if the transcript is long (>5,000 words)

Save the cleaned transcript as a `.docx` file:
- Filename: `[guest-slug]-transcript.docx`
- Save alongside the final newsletter

If the transcript fails (captions disabled), fall back to research-based summary and inform the user.

### Step 4b: Capture Video Screenshots

**Always capture screenshots** from key moments in the video that visually explain or enhance the Q&A content. Screenshots make newsletters dramatically more engaging and help readers follow along without watching the full video.

#### How to Capture

1. Use Playwright MCP to navigate to the YouTube video URL
2. Accept any cookie/consent dialogs, then wait for the video player to load
3. Identify 6-10 key timestamps from the transcript where visual context adds value:
   - Title cards, intro screens, or on-screen graphics
   - Key data points shown on screen (charts, numbers, diagrams)
   - Important moments where the speaker is making a key point
   - Product shots, demos, or visual examples
   - Reaction shots or memorable visual moments
4. For each timestamp, seek the video using JavaScript:
   ```javascript
   const v = document.querySelector('video');
   v.currentTime = SECONDS;
   v.pause();
   ```
5. Take a screenshot of each frame using Playwright's screenshot tool
6. Save screenshots to `output/YYYY-MM-DD/screenshots/` as JPEG files
7. Convert all screenshots to base64 and save as `screenshots/base64_images.json`

```python
import base64, json, glob
images = {}
for f in sorted(glob.glob('screenshots/shot-*.jpeg')):
    key = f.split('shot-')[1].replace('.jpeg', '').split('-', 1)[1]
    with open(f, 'rb') as img:
        images[key] = base64.b64encode(img.read()).decode()
with open('screenshots/base64_images.json', 'w') as out:
    json.dump(images, out)
```

#### Where to Place Screenshots

- Embed screenshots inside Q&A answers using `.slide-wrapper` / `.slide-img` / `.slide-caption`
- Place them where the visual adds context the text alone can't convey
- Aim for at least 1 screenshot per thematic section
- Use base64 data URIs so the HTML remains self-contained
- Every screenshot must have a descriptive `.slide-caption`

```html
<div class="slide-wrapper">
  <img class="slide-img" src="data:image/jpeg;base64,[DATA]" alt="[description]">
  <div class="slide-caption">[Caption describing the screenshot]</div>
</div>
```

### Step 5: Research Guest and Topic

Run 3-4 web searches in parallel to gather substance:
1. `[Guest name] background career work history`
2. `[Guest name] [company/role] philosophy approach`
3. `[Episode title keywords] key takeaways insights`
4. `[Guest name] notable quotes talks interviews`

Extract: current role, career milestones, key themes, direct quotes.

### Step 6: Synthesize Newsletter Content

**Re-read the transcript first.** The transcript is the primary source — it takes precedence over web research whenever the two conflict. Use the speaker's actual language and phrasing rather than paraphrased summaries. Preserve the specificity of their anecdotes (tools named, numbers cited, stories told). The newsletter should feel like you were in the room, not like a press release.

#### Choose the Right Content Structure

The format should fit the episode, not the other way around. Before writing, ask: *what kind of content was this?* Then choose accordingly:

- **Q&A format** — best for interview-style episodes with clear back-and-forth
- **Narrative / essay** — best when the speaker has one big thesis developed progressively
- **Tutorial / walkthrough** — best for how-to episodes or process breakdowns
- **Debate / panel** — best for multi-guest or contrarian episodes
- **Hybrid** — mix formats freely. A narrative intro + Q&As + tactical checklist is fine

#### Content to Generate

1. **Header subtitle** — 2 compelling sentences (<200 chars) teasing the speaker's perspective
2. **Intro callout** — emoji + 2-3 sentences on why this episode matters
3. **Results banner** — 3-4 key stats/numbers from the episode (big orange numbers with short labels)
4. **Core message cards** — 3-5 cards with `.core-card-tag` (e.g., RULE 1, LESSON 1), emoji, short title, 2-3 sentence description
5. **Thematic sections** — Group Q&As into PARTS by topic. Each section has a `section-title`, `section-desc`, and 1-3 Q&As. Cover ALL topics with NO fixed limit. Each Q&A answer should be 3-8+ sentences of substantive content grounded in the transcript.
6. **Highlight boxes** — Add green ACTION callouts inside Q&A answers where actionable advice appears. Use `📌 ACTION:` prefix.
7. **Pull quotes** — Distribute 2-3 real quotable lines within sections for visual rhythm. Must be actual quotes from the episode, not summaries.
8. **Action plan** — Phase list with concrete STEP 1-N items at the end (when the episode warrants it)
9. **Final pull quote** — the single most quotable line from the episode

There is **NO limit** on how many insights, sections, or Q&As you produce. Cover the episode exhaustively — every substantive topic, every piece of tactical advice, every notable opinion. Depth and completeness are the goals.

### Step 7: Fact-Check

Before rendering the final HTML, verify every claim in detail:
- Cross-reference guest background, role, and company against web search results
- Confirm any statistics, dates, or product names mentioned
- Update or remove any content that cannot be verified

### Step 8: Render HTML Newsletter

Generate a complete, self-contained HTML file using the design system from CLAUDE.md.

The HTML must include:
- Google Fonts link (Inter + Lora)
- All CSS from the design system (inline in `<style>`), including results-banner, section, highlight-box, phase-list, slide-wrapper, and core-card-tag styles
- Header block with: AI UX WEEKLY tag with pulsing dot, h1 with `<em>` on key phrase, subtitle, meta chips (guest/host, date, duration), Watch on YouTube button
- Body block with: intro callout, results banner, core-grid with tagged cards, thematic sections containing Q&As with highlight boxes and optional images, distributed pull quotes, phase-list action plan, final pull quote
- Meta chips should include inline SVG icons for guest, calendar, and clock

**Critical rules:**
- `.header-meta` must use `flex-direction: column` — chips above button, never inline
- Header h1 must have an `<em>` wrapping the most evocative phrase (styled in orange #d97757)
- Q&As must be grouped into thematic `<section>` blocks with section-label, section-title, section-desc
- All Q&As must be substantive (3-8+ sentence answers), not generic filler
- Q&A answers should use the speaker's actual language and cite specifics from the transcript
- Include `.highlight-box` ACTION callouts in Q&A answers with actionable advice
- Pull quotes must be distributed within sections, not only at the end
- Action plan must use `.phase-list` / `.phase-badge` pattern (STEP 1-N)
- Core cards must have `.core-card-tag` labels
- Screenshots are mandatory: 6-10 base64-embedded images using `.slide-wrapper` / `.slide-img` / `.slide-caption`
- At least 1 screenshot per thematic section, placed contextually inside Q&A answers
- Pull quote must be a real quotable line, not a summary
- "Watch on YouTube" button must link to the original URL

### Step 9: Save to Output

```bash
mkdir -p output/$(date +%Y-%m-%d)
```

Save the HTML file as: `output/YYYY-MM-DD/{slug}-newsletter.html`

Where `{slug}` is derived from the guest name and topic (e.g., `jenny-wen-design-process-newsletter.html`).

Also save the transcript `.docx` to the same directory.

After saving, tell the user the file path so they can open it:
```
open output/YYYY-MM-DD/{slug}-newsletter.html
```
