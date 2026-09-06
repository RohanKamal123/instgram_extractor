# Data Model

The data model separates original/archive information, AI-derived intelligence, and human-provided knowledge.

## Reel

Represents the original Instagram Reel discovered in an accessible DM.

Fields:

- id
- instagram_message_id
- reel_url
- conversation_id
- source_identity
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
- frame_reference
- created_at

## Analysis

Represents AI-generated understanding of a Reel.

Fields:

- id
- reel_id
- title
- summary
- why_saved
- why_saved_is_inference
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

AI analysis must be regenerable without destroying raw information or user answers/corrections.

## User Question

Represents an ambiguity or missing important information that the system cannot safely resolve automatically.

Fields:

- id
- reel_id
- session_id
- question
- reason
- evidence/context
- question_type
- status
- created_at
- answered_at

Possible question types:

- mcq
- free_text
- confirmation

Possible statuses:

- pending
- answered
- dismissed
- superseded

## Question Option

Represents an option for a human-in-the-loop question.

Fields:

- id
- question_id
- label
- value
- position

## User Answer

Represents the user's response to a question.

Fields:

- id
- question_id
- reel_id
- selected_option_id
- free_text
- answered_at

User answers are durable knowledge and must survive AI-analysis regeneration.

## User Correction

Represents an explicit correction to AI interpretation or extracted knowledge.

Fields:

- id
- reel_id
- field
- original_value
- corrected_value
- reason
- created_at

## Evidence

Represents source material supporting an analysis or human question.

Fields:

- id
- reel_id
- evidence_type
- content/reference
- timestamp
- created_at

Possible evidence types:

- transcript
- subtitle
- OCR
- visual
- caption
- metadata
- external_resource

## Embedding

Represents semantic-search representation.

Fields:

- id
- reel_id
- content_type
- embedding
- model
- created_at

## Processing Session

Represents one continuous extraction run initiated by the user.

Fields:

- id
- selected_source_identity
- status
- started_at
- paused_at
- completed_at
- created_at
- updated_at

Possible statuses:

- starting
- running
- waiting_for_user
- paused
- completed
- failed
- stopped

## Processing Job

Represents asynchronous processing work for a Reel or processing stage.

Fields:

- id
- session_id
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
- waiting_for_user
- completed
- failed
- cancelled

## Report

Represents a generated output artifact derived from the knowledge base.

Fields:

- id
- report_type
- title
- scope
- output_path
- generated_at
- source_snapshot/reference

Reports are derived artifacts. They are not the canonical knowledge store.

## Visualization

Represents a generated data visualization used in reports or the UI.

Fields:

- id
- report_id
- visualization_type
- title
- data_reference
- output_path
- created_at

## Relationships

- One `Reel` can have multiple `Transcript` records over time, while one is designated current/preferred.
- One `Reel` can have multiple `OCR` records.
- One `Reel` can have multiple `Analysis` versions.
- One `Reel` can have many `User Question` records.
- One `User Question` can have many `Question Option` records and one or more answer records if re-answered.
- `User Answer` and `User Correction` are preserved independently of regenerated AI analysis.
- `Evidence` links source material to analysis/questions.
- One `Processing Session` has many `Processing Job` records.
- `Report` and `Visualization` reference knowledge-base data rather than replacing it.
