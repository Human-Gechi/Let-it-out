<script setup lang="ts">
import type { HealthResponse } from '~/types/api'

type State = 'ok' | 'disabled' | 'degraded' | 'unreachable'

const { health } = useLetItOutApi()

const state = ref<State | null>(null)

/**
 * Client only — the footnote never renders during SSR, and it stays absent
 * until the check resolves so nothing on the page flashes.
 * ai_reason is deliberately never surfaced: it can carry provider internals.
 */
onMounted(async () => {
  try {
    const result: HealthResponse = await health()
    state.value = result.status
  } catch {
    state.value = 'unreachable'
  }
})

const LABELS: Record<State, string> = {
  ok: 'Reflections on',
  disabled: 'Reflections off — you can still write',
  degraded: 'Reflections may not come back right now',
  unreachable: 'Cannot reach the server',
}

const TONE: Record<State, string> = {
  ok: 'text-muted-foreground',
  disabled: 'text-muted-foreground',
  degraded: 'text-pending',
  unreachable: 'text-muted-foreground',
}
</script>

<template>
  <p v-if="state" class="flex items-center gap-2 text-xs" :class="TONE[state]">
    <span
      v-if="state === 'ok'"
      class="inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-current text-released"
      aria-hidden="true"
    />
    {{ LABELS[state] }}
  </p>
</template>
