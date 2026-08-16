<script setup lang="ts">
import { Check, Monitor, Moon, Sun } from 'lucide-vue-next'
import type { Theme } from '~/composables/useTheme'

const { theme, setTheme } = useTheme()

// Light mode is commented out for now, which leaves Dark as the only choice.
// Restore the two entries below together with the block in useTheme.
const OPTIONS: { value: Theme; label: string; icon: typeof Sun }[] = [
  // { value: 'system', label: 'System', icon: Monitor },
  // { value: 'light', label: 'Light', icon: Sun },
  { value: 'dark', label: 'Dark', icon: Moon },
]

const open = ref(false)
const root = ref<HTMLElement | null>(null)
const trigger = ref<HTMLButtonElement | null>(null)

const current = computed(() => OPTIONS.find((o) => o.value === theme.value) ?? OPTIONS[0]!)

function choose(next: Theme) {
  setTheme(next)
  open.value = false
  trigger.value?.focus()
}

function onDocumentMousedown(event: MouseEvent) {
  if (!open.value) return
  const target = event.target as Node | null
  if (target && root.value?.contains(target)) return
  open.value = false
}

function onKeydown(event: KeyboardEvent) {
  if (event.key !== 'Escape' || !open.value) return
  open.value = false
  trigger.value?.focus()
}

onMounted(() => {
  document.addEventListener('mousedown', onDocumentMousedown)
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onDocumentMousedown)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div ref="root" class="relative">
    <button
      ref="trigger"
      type="button"
      class="icon-button"
      aria-haspopup="menu"
      :aria-expanded="open"
      :title="`Appearance: ${current.label}`"
      @click="open = !open"
    >
      <span class="sr-only">Appearance: {{ current.label }}</span>
      <component :is="current.icon" class="h-4 w-4" aria-hidden="true" />
    </button>

    <div
      v-if="open"
      role="menu"
      aria-label="Appearance"
      class="card-raised absolute right-0 top-full z-50 mt-2 w-40 overflow-hidden p-1"
    >
      <button
        v-for="option in OPTIONS"
        :key="option.value"
        type="button"
        role="menuitem"
        class="flex w-full items-center gap-2.5 rounded px-3 py-2 text-left text-sm transition-colors hover:bg-surface-muted"
        :class="theme === option.value ? 'text-primary' : 'text-secondary-foreground'"
        @click="choose(option.value)"
      >
        <component :is="option.icon" class="h-4 w-4" aria-hidden="true" />
        <span class="flex-1">{{ option.label }}</span>
        <template v-if="theme === option.value">
          <span class="sr-only">Selected</span>
          <Check class="h-4 w-4" aria-hidden="true" />
        </template>
      </button>
    </div>
  </div>
</template>
