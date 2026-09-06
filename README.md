# Instagram Reel Extractor

A personal AI archivist that continuously processes Instagram Reels from accessible DMs and turns them into structured personal knowledge.

## Why

Interesting Reels are easy to save and easy to forget. Reopening hundreds of Reels and manually taking notes is slow and frustrating.

This project automates the work after saving:

**Capture once → understand automatically → clarify when necessary → retrieve later.**

## Intended User Experience

1. Open Chrome with Instagram already logged in.
2. Run the extractor from a terminal.
3. The agent opens a clear status/control UI.
4. Enter the Instagram username/identity whose Reel messages should be extracted.
5. The system verifies and locks that source.
6. The agent continuously discovers and processes Reels.
7. The UI shows current activity and progress.
8. If important information is uncertain, the agent asks a question, preferably as an MCQ, with the Reel URL and evidence.
9. Answering the question lets processing continue.
10. At the end, the system generates a detailed human-readable PDF, summaries, and useful visualizations.
11. Later, search and RAG chat operate directly on the structured knowledge base; generated reports do not need to be attached.

## Current Product Boundaries

- Personal-only
- Browser automation rather than primary dependence on an Instagram API
- Manual Instagram authentication
- Self-DM as the primary source
- Other accessible DM conversations may be supported
- No social actions
- Transcript-first processing
- OCR and visual understanding
- DeepSeek initially for general-purpose LLM work
- Local Whisper where practical
- Resumable continuous processing
- Human-in-the-loop for important uncertainty
- Structured knowledge base as canonical memory

## Documentation

- `AGENTS.md` — autonomous engineering rules and product constraints
- `GOAL.md` — product goal and user experience
- `ARCHITECTURE.md` — application and development architecture
- `DECISIONS.md` — locked decisions
- `ROADMAP.md` — implementation phases
- `DATA_MODEL.md` — persistent data entities
- `DEVELOPMENT.md` — Windows/Trae/GitHub/VPS workflow
- `SECURITY.md` — privacy and security requirements

Read the documentation before making architectural changes.
