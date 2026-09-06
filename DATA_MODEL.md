# Data Model

## Reel

Represents the original Instagram Reel.

Fields:

- id
- instagram_message_id
- reel_url
- conversation_id
- sender
- creator
- caption
- captured_at
- original_media_url
- local_media_path
- media_retention_policy
- processing_status
- created_at
- updated_at

## Transcript

Represents speech/subtitle transcription.

Fields:

- id
- reel_id
- text
- language
- source
- confidence
- timestamped_segments
- created_at

Possible source values:

- instagram
- subtitle
- whisper
- other

## OCR

Represents text extracted from Reel frames.

Fields:

- id
- reel_id
- text
- timestamp
- confidence
- created_at

## Analysis

Represents AI-generated understanding.

Fields:

- id
- reel_id
- title
- summary
- why_saved
- key_points
- topics
- categories
- tools
- products
- people
- companies
- claims
- resources
- action_items
- importance
- confidence
- model
- created_at
- updated_at

## User Correction

Represents corrections to AI interpretation.

Fields:

- id
- reel_id
- field
- original_value
- corrected_value
- created_at

## Embedding

Represents semantic-search representation.

Fields:

- id
- reel_id
- content_type
- embedding
- model
- created_at

## Processing Job

Represents asynchronous processing.

Fields:

- id
- reel_id
- job_type
- status
- attempts
- error
- started_at
- completed_at
- created_at

Possible statuses:

- pending
- processing
- completed
- failed
