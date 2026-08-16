import { LETTER_MAX_LENGTH } from '~/types/api'
import type { RecipientType, Tone } from '~/types/api'

export const LETTER_DRAFT_KEY = 'lio-draft'

export interface LetterDraft {
  letterText: string
  recipientType: RecipientType
  tone: Tone
}

const RECIPIENT_TYPES: RecipientType[] = ['ex', 'job', 'past_self', 'person_lost', 'other']
const TONES: Tone[] = ['gentle', 'encouraging', 'neutral']

export function readLetterDraft(): LetterDraft | null {
  if (!import.meta.client) return null

  try {
    const raw = localStorage.getItem(LETTER_DRAFT_KEY)
    if (!raw) return null

    const saved = JSON.parse(raw) as Partial<LetterDraft>
    if (typeof saved.letterText !== 'string') return null

    return {
      letterText: saved.letterText.slice(0, LETTER_MAX_LENGTH),
      recipientType: RECIPIENT_TYPES.includes(saved.recipientType as RecipientType)
        ? (saved.recipientType as RecipientType)
        : 'other',
      tone: TONES.includes(saved.tone as Tone) ? (saved.tone as Tone) : 'gentle',
    }
  } catch {
    return null
  }
}

export function writeLetterDraft(draft: LetterDraft): void {
  if (!import.meta.client) return

  try {
    localStorage.setItem(
      LETTER_DRAFT_KEY,
      JSON.stringify({
        ...draft,
        letterText: draft.letterText.slice(0, LETTER_MAX_LENGTH),
      }),
    )
  } catch {
    // A blocked or full local store should never interrupt the writing flow.
  }
}

export function clearLetterDraft(): void {
  if (!import.meta.client) return

  try {
    localStorage.removeItem(LETTER_DRAFT_KEY)
  } catch {
    // The in-memory letter can still be cleared when local storage is unavailable.
  }
}
