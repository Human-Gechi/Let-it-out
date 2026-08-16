import type {
  HealthResponse,
  PromptResponse,
  RecipientType,
  ReflectRequest,
  ReflectResponse,
} from '~/types/api'

export class ApiError extends Error {
  readonly status: number
  readonly retryAfterSeconds: number | null

  constructor(message: string, status: number, retryAfterSeconds: number | null = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.retryAfterSeconds = retryAfterSeconds
  }
}

function describe(status: number, detail: unknown): string {
  if (status === 429) return 'That was quick. Give it a moment and try again.'
  if (status === 422) return 'The letter needs at least a word, and at most 8000 characters.'
  if (status === 0) return 'Could not reach the server. Check that the backend is running.'
  if (typeof detail === 'string' && detail) return detail
  return 'Something went wrong on our side. Your words are still here.'
}

/**
 * Thin typed client over the FastAPI backend.
 * Requests are not persisted here; draft storage is handled separately in the browser.
 */
export function useLetItOutApi() {
  const base = useRuntimeConfig().public.apiBase

  async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
    let response: Response

    try {
      response = await fetch(`${base}${path}`, {
        ...options,
        headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
      })
    } catch {
      throw new ApiError(describe(0, null), 0)
    }

    if (!response.ok) {
      let detail: unknown = null
      try {
        detail = (await response.json())?.detail
      } catch {
        detail = null
      }
      const retryAfter = response.headers.get('Retry-After')
      throw new ApiError(
        describe(response.status, detail),
        response.status,
        retryAfter ? Number(retryAfter) : null,
      )
    }

    return (await response.json()) as T
  }

  return {
    getPrompt: (recipientType: RecipientType) =>
      request<PromptResponse>(`/prompt?recipient_type=${encodeURIComponent(recipientType)}`),

    reflect: (payload: ReflectRequest) =>
      request<ReflectResponse>('/reflect', {
        method: 'POST',
        body: JSON.stringify(payload),
      }),

    health: () => request<HealthResponse>('/health'),
  }
}
