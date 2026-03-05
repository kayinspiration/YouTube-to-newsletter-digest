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

If the input is not a valid YouTube URL, stop and ask for a valid URL.

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

If the transcript fails (captions disabled), inform the user and stop gracefully.

### Step 5: Research Guest and Topic

Run 3-4 web searches in parallel to gather substance:
1. `[Guest name] background career work history`
2. `[Guest name] [company/role] philosophy approach`
3. `[Episode title keywords] key takeaways insights`
4. `[Guest name] notable quotes talks interviews`

Extract: current role, career milestones, key themes, direct quotes.

### Step 6: Synthesize Newsletter Content

Using the transcript + research, generate:

1. **Header subtitle** — 2 compelling sentences (<200 chars) teasing the guest's perspective
2. **Intro callout** — emoji + 2-3 sentences on why this episode matters
3. **5 core message cards** — each with emoji, short title, 2-3 sentence description
4. **10 Q&A insights** — each Q is a question the episode addresses; each A is 3-6 sentences of substantive answer as if the guest is speaking. Cover: career story, core philosophy, tactical advice, provocative opinions, future predictions.
5. **Pull quote** — the single most quotable line from the episode

### Step 7: Render HTML Newsletter

Generate a complete, self-contained HTML file using the design system from CLAUDE.md.

The HTML must include:
- Google Fonts link (Inter + Lora)
- All CSS from the design system (inline in `<style>`)
- Header block with: AI UX WEEKLY tag with pulsing dot, h1 with `<em>` on key phrase, subtitle, meta chips (guest, date, duration), Watch on YouTube button
- Body block with: intro callout, core-grid with cards, section divider, 10 Q&A items, pull quote
- Meta chips should include inline SVG icons for guest, calendar, and clock

**Critical rules:**
- `.header-meta` must use `flex-direction: column` — chips above button, never inline
- Header h1 must have an `<em>` wrapping the most evocative phrase (styled in orange #d97757)
- All 10 Q&As must be substantive, not generic filler
- Pull quote must be a real quotable line, not a summary
- "Watch on YouTube" button must link to the original URL

### Step 8: Save to Output

```bash
mkdir -p output/$(date +%Y-%m-%d)
```

Save the HTML file as: `output/YYYY-MM-DD/{slug}-newsletter.html`

Where `{slug}` is derived from the guest name and topic (e.g., `jenny-wen-design-process-newsletter.html`).

After saving, tell the user the file path so they can open it:
```
open output/YYYY-MM-DD/{slug}-newsletter.html
```
