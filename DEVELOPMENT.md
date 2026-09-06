# Development Guide

## Environment Model

This project intentionally separates development from persistent runtime infrastructure.

### Primary development

- OS: Windows
- Coding agent: Trae
- Browser: user's normal Chrome/appropriate local Chromium session
- Source control: Git
- Canonical repository: GitHub

### Runtime / deployment

- VPS: persistent runtime and infrastructure when required
- The VPS is not the default coding workstation.
- Do not introduce remote/distributed components until a concrete requirement exists.

## Local-First Development

The first working version should run locally on Windows wherever practical.

Local execution is especially preferred for:

- Playwright/browser automation
- manual Instagram authentication
- interactive UI development
- OCR/transcription experiments
- tests
- debugging

The browser agent may eventually be deployed differently, but this is not assumed by the initial architecture.

## User Startup Experience

The intended normal workflow is:

1. User opens Chrome.
2. Instagram is already logged in through the user's normal browser session.
3. User opens/keeps an Instagram tab available.
4. User opens a terminal.
5. User runs the extractor command.
6. The application starts its interactive status UI.
7. The application asks for the Instagram username/identity from which Reels should be extracted.
8. The application verifies and locks the selected identity.
9. The continuous worker begins discovery and processing.
10. The UI displays progress and any questions requiring the user's attention.

The application must never require the user to paste an Instagram password into the terminal or UI.

## Git Workflow

GitHub is the canonical source of truth.

Prefer small coherent commits that represent working milestones.

Do not commit:

- API keys
- passwords
- browser cookies
- session tokens
- private browser profiles
- downloaded private Reel media unless explicitly intended and protected
- local databases containing private user data unless explicitly intended

## Local Configuration

Use environment variables and local configuration files for secrets and machine-specific settings.

Provide a safe `.env.example` without real credentials.

Keep secrets out of logs and error reports.

## Testing

Every meaningful feature should have tests.

Tests should be runnable locally without requiring a live Instagram account whenever possible.

Use mocks/fixtures for browser observations and external services.

Live Instagram tests should be isolated and should never perform social actions.

## Continuous Worker

The extractor is expected to run for long periods.

Persist processing state so it can recover after:

- application restart
- browser restart/failure
- network failure
- individual Reel processing failure
- user-question waiting state

The system should not restart completed work unnecessarily.

## Human-in-the-Loop Development

Important uncertainty must produce an explicit user question rather than a silent guess.

Questions should include the relevant Reel URL and evidence/context.

Use MCQ when appropriate.

After an answer is submitted, dependent processing should resume without requiring the entire extraction run to restart.

## Deployment Principle

Only move components to the VPS when there is a concrete operational reason, such as persistent services or workloads that benefit from remote availability.

The initial architecture should remain simple enough for one developer and one user to understand, run, and recover.
