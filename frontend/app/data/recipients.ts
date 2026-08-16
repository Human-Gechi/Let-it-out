import type { RecipientType, Tone } from '~/types/api'

export interface RecipientOption {
  value: RecipientType
  /** What the user picks in the UI. */
  label: string
  /** Reads as the opening of the letter: "To ___". */
  addressee: string
  description: string
}

/** Order matters — this is the order the composer offers them in. */
export const RECIPIENTS: RecipientOption[] = [
  {
    value: 'ex',
    label: 'Someone I loved',
    addressee: 'the person I loved',
    description: 'A relationship that ended before the conversation did.',
  },
  {
    value: 'person_lost',
    label: 'Someone I lost',
    addressee: 'the person I lost',
    description: 'Grief that never got its last word.',
  },
  {
    value: 'past_self',
    label: 'Who I used to be',
    addressee: 'the girl I used to be',
    description: 'The version of you that was carrying it alone.',
  },
  {
    value: 'job',
    label: 'A job that ended',
    addressee: 'the place I worked',
    description: 'A room you gave years to and left quietly.',
  },
  {
    value: 'other',
    label: 'Something else',
    addressee: 'whoever this is for',
    description: 'A thing you have been holding that has no name yet.',
  },
]

export interface ToneOption {
  value: Tone
  label: string
  description: string
}

export const TONES: ToneOption[] = [
  { value: 'gentle', label: 'Gentle', description: 'Soft, unhurried, no advice.' },
  { value: 'encouraging', label: 'Encouraging', description: 'Warm and a little braver.' },
  { value: 'neutral', label: 'Plain', description: 'Steady and matter of fact.' },
]

export function recipientFor(value: RecipientType): RecipientOption {
  return RECIPIENTS.find((option) => option.value === value) ?? RECIPIENTS[RECIPIENTS.length - 1]!
}
