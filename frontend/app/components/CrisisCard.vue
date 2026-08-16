<script setup lang="ts">
import { HeartHandshake, Phone } from 'lucide-vue-next'

defineProps<{
  note: string
}>()

interface CrisisLine {
  region: string
  name: string
  number: string
  href: string
}

const LINES: CrisisLine[] = [
  { region: 'US', name: '988 Suicide & Crisis Lifeline', number: '988', href: 'tel:988' },
  { region: 'UK', name: 'Samaritans', number: '116 123', href: 'tel:116123' },
  { region: 'Nigeria', name: 'MANI', number: '0809 111 6264', href: 'tel:08091116264' },
]
</script>

<template>
  <section
    role="note"
    aria-label="Support lines you can call"
    class="animate-fade-rise rounded-lg border border-care bg-care-soft p-6 sm:p-7"
  >
    <div class="flex items-start gap-3">
      <HeartHandshake class="mt-0.5 h-5 w-5 shrink-0 text-care" aria-hidden="true" />
      <div class="min-w-0">
        <h2 class="font-serif text-xl leading-snug text-foreground">
          Before you let this one go
        </h2>
        <p class="mt-2 text-sm leading-relaxed text-secondary-foreground">
          What you wrote matters more than the letter does. If any of it is true right now,
          there is someone who will pick up.
        </p>
      </div>
    </div>

    <p class="mt-5 text-sm leading-relaxed text-secondary-foreground">
      {{ note }}
    </p>

    <ul class="mt-5 space-y-2">
      <li v-for="line in LINES" :key="line.region">
        <a
          :href="line.href"
          class="flex items-center gap-3 rounded-md border border-border bg-card px-4 py-3 transition-colors hover:border-care"
        >
          <Phone class="h-4 w-4 shrink-0 text-care" aria-hidden="true" />
          <span class="min-w-0 flex-1">
            <span class="block text-sm font-medium text-foreground">
              {{ line.region }} — {{ line.name }}
            </span>
            <span class="block text-xs text-muted-foreground">Tap to call {{ line.number }}</span>
          </span>
        </a>
      </li>
    </ul>

    <p class="mt-5 text-xs leading-relaxed text-muted-foreground">
      You can keep writing for as long as you want. Nothing has been sent to the person you wrote to.
    </p>
  </section>
</template>
