<script setup lang="ts">
const props = defineProps<{
  open: boolean
  reflection: string
  showHelp: boolean
  resourceNote: string
  safeToRelease: boolean
}>()

const emit = defineEmits<{
  keepWriting: []
  release: []
}>()

const isMounted = ref(false)
const panel = ref<HTMLElement | null>(null)
const primaryButton = ref<HTMLButtonElement | null>(null)

let restoreTo: HTMLElement | null = null
let previousOverflow: string | null = null

const paragraphs = computed(() =>
  props.reflection
    .split(/\n\s*\n/)
    .map((part) => part.trim())
    .filter(Boolean),
)

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
  if (event.key === 'Escape') {
    event.preventDefault()
    emit('keepWriting')
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
  restoreTo = document.activeElement as HTMLElement | null
  lockScroll()
  nextTick(() => primaryButton.value?.focus())
}

function handleClose() {
  unlockScroll()

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

onBeforeUnmount(unlockScroll)
</script>

<template>
  <Teleport v-if="isMounted && open" to="body">
    <div
      ref="panel"
      class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto px-4 py-6 sm:py-8"
      role="dialog"
      aria-modal="true"
      aria-labelledby="reflection-dialog-heading"
      aria-describedby="reflection-dialog-disclaimer"
      @keydown="onKeydown"
    >
      <div class="fixed inset-0 bg-canvas/92 backdrop-blur-sm" aria-hidden="true" />

      <section class="card-raised animate-fade-rise relative my-auto w-full max-w-xl overflow-hidden p-6 sm:p-8">
        <InkFlourish class="pointer-events-none absolute -left-20 -top-14 h-32 w-[40rem] opacity-25" />

        <div class="relative">
          <p class="field-label">One reflection</p>
          <h2 id="reflection-dialog-heading" class="mt-2 font-serif text-3xl leading-tight text-foreground">
            What came back
          </h2>

          <div class="mt-6 max-h-[40vh] space-y-4 overflow-y-auto pr-2 font-serif text-lg leading-8 text-foreground sm:max-h-[44vh]">
            <p v-for="(paragraph, index) in paragraphs" :key="index">{{ paragraph }}</p>
          </div>

          <p id="reflection-dialog-disclaimer" class="mt-6 text-xs leading-5 text-muted-foreground">
            Generated from the letter you submitted. This is not advice, diagnosis, or therapy.
          </p>

          <CrisisCard v-if="showHelp" :note="resourceNote" embedded class="mt-7" />

          <div class="mt-7 grid gap-3 sm:grid-cols-[auto_1fr]">
            <!-- Keep writing always takes initial focus: releasing is immediate and cannot be undone. -->
            <button
              ref="primaryButton"
              type="button"
              :class="safeToRelease ? 'text-button' : 'action-button'"
              @click="emit('keepWriting')"
            >
              Keep writing
            </button>

            <button
              type="button"
              :class="safeToRelease ? 'action-button' : 'text-button'"
              @click="emit('release')"
            >
              {{ safeToRelease ? 'Release this draft' : 'Release anyway' }}
            </button>
          </div>

          <p class="mt-3 text-right text-xs text-muted-foreground">
            Releasing clears the draft from this browser and returns you to the start.
          </p>
        </div>
      </section>
    </div>
  </Teleport>
</template>
