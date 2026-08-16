/**
 * Mirrors backend/app/schemas.py. Keep these in step with the FastAPI models.
 */

export type RecipientType = 'ex' | 'job' | 'past_self' | 'person_lost' | 'other'

export type Tone = 'gentle' | 'encouraging' | 'neutral'

export interface PromptResponse {
  prompt: string
  recipient_type: RecipientType
}

export interface ReflectRequest {
  letter_text: string
  recipient_type: RecipientType
  tone: Tone
}

export interface ReflectResponse {
  reflection: string
  safe_to_release: boolean
  resource_note: string | null
}

export interface HealthResponse {
  status: 'ok' | 'degraded' | 'disabled'
  ai_enabled: boolean
  ai_reachable: boolean
  ai_reason: string | null
}

/** The backend caps letter_text at 8000 characters. */
export const LETTER_MAX_LENGTH = 8000
