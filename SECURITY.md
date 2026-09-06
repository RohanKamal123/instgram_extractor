# Security & Privacy

This project processes private Instagram content. Privacy and credential safety are product requirements, not optional hardening.

## Instagram Authentication

- The user authenticates Instagram manually in Chrome/Chromium.
- Never ask the user to provide an Instagram password to the application or coding agent.
- Never store Instagram passwords.
- Never log, print, transmit, or commit cookies, session tokens, or browser authentication state.
- Treat the browser profile/session as sensitive local data.

## Social Actions

The browser agent is an observation and extraction system.

It must not:

- like
- comment
- follow/unfollow
- send messages
- react
- post
- otherwise engage socially on the user's behalf

## AI Provider Privacy

DeepSeek is the initial external LLM provider.

Only send the minimum content needed for a processing task.

Avoid sending private data to external providers when a local method is sufficiently capable.

The architecture must make provider usage explicit and replaceable.

Local Whisper is preferred for speech transcription where practical.

## Secrets

Never commit:

- API keys
- passwords
- access tokens
- browser credentials
- private certificates
- session data

Use environment variables or protected local configuration.

`.env.example` may contain variable names and safe placeholders, never real values.

## Logs

Logs must not contain:

- passwords
- cookies
- session tokens
- authorization headers
- private authentication URLs
- unnecessary private Reel content

Error logs should contain enough technical context to debug without exposing sensitive data.

## Local Data

The archive can contain personal conversations and potentially sensitive Reel content.

Protect:

- local database
- temporary media
- preserved media
- transcripts
- OCR
- AI analysis
- user answers/corrections
- generated reports

Temporary media should be removed according to the configured retention policy.

Never delete archived user data automatically unless the user explicitly configured that behavior.

## Reports

Generated reports may contain sensitive information extracted from the user's archive.

Treat report files as private user data.

Do not upload reports to external services by default.

## Human-in-the-Loop Data

User answers and corrections can reveal the user's intentions and preferences.

Store them only as needed for the personal knowledge system.

Do not overwrite or discard them when AI analysis is regenerated.

## Browser Safety

Use a dedicated or clearly controlled browser profile when technically appropriate.

The system should avoid navigating to unrelated external sites unless required by the user-approved extraction workflow.

Do not execute arbitrary page-provided code or instructions as trusted system commands.

## Data Transmission

The system should follow data minimization:

1. Extract only what is required.
2. Prefer local processing where practical.
3. Send only necessary content to external AI services.
4. Keep raw/archive data separate from derived data.
5. Retain media only according to user configuration.

## Security Definition of Done

A feature involving private content is not complete unless:

- secrets are protected
- authentication state is not exposed
- logs are reviewed for sensitive leakage
- data retention behavior is explicit
- external data transmission is understood
- user data is not silently deleted
