<script setup lang="ts">
const props = defineProps<{
  open: boolean
  letter: string
}>()

const emit = defineEmits<{
  cancel: []
  released: []
}>()

const HOLD_MS = 1500
const RELEASE_MS = 1500
const REDUCED_RELEASE_MS = 250
const PREVIEW_CHARS = 260

const isMounted = ref(false)
const step = ref<'confirm' | 'release'>('confirm')
const reduced = ref(false)
const panel = ref<HTMLElement | null>(null)
const holdButton = ref<HTMLButtonElement | null>(null)
const stage = ref<HTMLElement | null>(null)
const holdProgress = ref(0)

let releaseTimer: ReturnType<typeof setTimeout> | null = null
let holdFrame: number | null = null
let holdStartedAt = 0
let restoreTo: HTMLElement | null = null
let previousOverflow: string | null = null

const excerpt = computed(() => {
  const text = props.letter.trim()
  if (text.length <= PREVIEW_CHARS) return text
  return `${text.slice(0, PREVIEW_CHARS).trimEnd()}...`
})

const labelledBy = computed(() =>
  step.value === 'confirm' ? 'release-confirm-heading' : 'release-stage-heading',
)

const holdStyle = computed(() => ({ '--hold-progress': `${holdProgress.value}%` }))

function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function clearReleaseTimer() {
  if (releaseTimer === null) return
  clearTimeout(releaseTimer)
  releaseTimer = null
}

function cancelHold() {
  if (holdFrame !== null) cancelAnimationFrame(holdFrame)
  holdFrame = null
  holdStartedAt = 0
  holdProgress.value = 0
}

function completeRelease() {
  cancelHold()
  reduced.value = prefersReducedMotion()
  step.value = 'release'
  nextTick(() => stage.value?.focus())
  releaseTimer = setTimeout(
    () => emit('released'),
    reduced.value ? REDUCED_RELEASE_MS : RELEASE_MS,
  )
}

function updateHold(now: number) {
  const elapsed = now - holdStartedAt
  holdProgress.value = Math.min(100, (elapsed / HOLD_MS) * 100)
  if (holdProgress.value >= 100) {
    completeRelease()
    return
  }
  holdFrame = requestAnimationFrame(updateHold)
}

function beginHold() {
  if (step.value !== 'confirm' || holdFrame !== null) return
  holdStartedAt = performance.now()
  holdFrame = requestAnimationFrame(updateHold)
}

function onHoldKeydown(event: KeyboardEvent) {
  if (event.key !== 'Enter' && event.key !== ' ') return
  event.preventDefault()
  if (!event.repeat) beginHold()
}

function onHoldKeyup(event: KeyboardEvent) {
  if (event.key !== 'Enter' && event.key !== ' ') return
  event.preventDefault()
  cancelHold()
}

function lockScroll() {
  if (previousOverflow !== null) return
  previousOverflow = document.body.style.overflow
  document.body.style.overflow = 'hidden'
}

function unlockScroll() {
  if (previousOverflow === null) return
  document.body.style.overflow = previousOverflow
  previousOverflow = null
}

function focusableInPanel(): HTMLElement[] {
  if (!panel.value) return []
  return Array.from(
    panel.value.querySelectorAll<HTMLElement>(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])',
    ),
  ).filter((element) => element.offsetParent !== null || element === document.activeElement)
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape' && step.value === 'confirm') {
    event.preventDefault()
    emit('cancel')
    return
  }
  if (event.key !== 'Tab') return

  const items = focusableInPanel()
  if (!items.length) {
    event.preventDefault()
    return
  }

  const first = items[0]!
  const last = items[items.length - 1]!
  const active = document.activeElement as HTMLElement | null
  if (event.shiftKey && (active === first || !panel.value?.contains(active))) {
    event.preventDefault()
    last.focus()
  } else if (!event.shiftKey && (active === last || !panel.value?.contains(active))) {
    event.preventDefault()
    first.focus()
  }
}

function handleOpen() {
  step.value = 'confirm'
  holdProgress.value = 0
  restoreTo = document.activeElement as HTMLElement | null
  lockScroll()
  nextTick(() => holdButton.value?.focus())
}

function handleClose() {
  cancelHold()
  clearReleaseTimer()
  unlockScroll()
  step.value = 'confirm'

  const target = restoreTo
  restoreTo = null
  if (target?.isConnected) nextTick(() => target.focus())
}

onMounted(() => {
  isMounted.value = true
  if (props.open) handleOpen()
})

watch(
  () => props.open,
  (open) => {
    if (!isMounted.value) return
    if (open) handleOpen()
    else handleClose()
  },
)

onBeforeUnmount(() => {
  cancelHold()
  clearReleaseTimer()
  unlockScroll()
})
</script>

<template>
  <Teleport v-if="isMounted && open" to="body">
    <div
      ref="panel"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto px-4 py-8"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="labelledBy"
      @keydown="onKeydown"
    >
      <div class="fixed inset-0 bg-canvas/92 backdrop-blur-sm" aria-hidden="true" />

      <div v-if="step === 'confirm'" class="card-raised animate-fade-rise relative w-full max-w-lg p-6 sm:p-8">
        <InkFlourish class="pointer-events-none absolute -left-16 -top-12 h-28 w-[36rem] opacity-25" />
        <div class="relative">
          <p class="field-label">Final step</p>
          <h2 id="release-confirm-heading" class="mt-2 font-serif text-3xl leading-tight">
            Clear this browser draft?
          </h2>
          <p class="mt-4 text-sm leading-6 text-secondary-foreground">
            This removes the saved letter from this device. It cannot undo a reflection request
            that has already been processed.
          </p>

          <blockquote class="letter-paper mt-6 max-h-44 overflow-hidden px-5 py-4 font-serif text-sm leading-7 text-secondary-foreground">
            {{ excerpt }}
          </blockquote>

          <div class="mt-6 grid gap-3 sm:grid-cols-[auto_1fr]">
            <button type="button" class="text-button" @click="emit('cancel')">Not yet</button>
            <button
              ref="holdButton"
              type="button"
              class="action-button release-hold"
              :style="holdStyle"
              @pointerdown="beginHold"
              @pointerup="cancelHold"
              @pointercancel="cancelHold"
              @pointerleave="cancelHold"
              @keydown="onHoldKeydown"
              @keyup="onHoldKeyup"
              @blur="cancelHold"
            >
              Press and hold to release
            </button>
          </div>
          <p class="mt-3 text-right text-xs text-muted-foreground">Hold for a moment so this stays intentional.</p>
        </div>
      </div>

      <div v-else ref="stage" tabindex="-1" class="relative w-full max-w-lg focus:outline-none">
        <h2 id="release-stage-heading" class="sr-only">Releasing your browser draft</h2>
        <InkFlourish class="pointer-events-none absolute -left-40 top-1/2 h-40 w-[50rem] -translate-y-1/2 opacity-45" />
        <div class="letter-paper relative px-7 py-8" :class="reduced ? 'opacity-0' : 'animate-ink-release'">
          <p class="font-serif text-base leading-8 text-foreground">{{ excerpt }}</p>
        </div>
        <p class="relative mt-7 text-center text-sm text-muted-foreground" role="status" aria-live="polite">
          Clearing the saved draft from this browser.
        </p>
      </div>
    </div>
  </Teleport>
</template>
