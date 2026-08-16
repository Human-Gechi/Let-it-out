<script setup lang="ts">
import type { Tone } from '~/types/api'

const props = defineProps<{
  reflection: string
  tone: Tone
}>()

const paragraphs = computed(() =>
  props.reflection
    .split(/\n\s*\n/)
    .map((part) => part.trim())
    .filter(Boolean),
)
</script>

<template>
  <section class="reflection-panel animate-fade-rise" aria-labelledby="reflection-heading">
    <p class="field-label">One reflection</p>
    <h2 id="reflection-heading" class="mt-2 font-serif text-2xl leading-snug text-foreground">
      What came back
    </h2>
    <div class="mt-5 space-y-4 font-serif text-lg leading-8 text-foreground">
      <p v-for="(paragraph, index) in paragraphs" :key="index">{{ paragraph }}</p>
    </div>
    <p class="mt-6 text-xs leading-5 text-muted-foreground">
      Generated from the letter you submitted. This is not advice, diagnosis, or therapy.
    </p>
  </section>
</template>
