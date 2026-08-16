<script setup lang="ts">
import { RefreshCw } from 'lucide-vue-next'

defineProps<{
  prompt: string | null
  loading: boolean
  error: string | null
}>()

defineEmits<{ shuffle: [] }>()
</script>

<template>
  <div class="prompt-panel">
    <p class="field-label">Need a first line?</p>
    <div class="prompt-panel__body" aria-live="polite">
      <p v-if="loading" class="animate-soft-pulse">Finding a place to begin...</p>
      <p v-else-if="prompt">{{ prompt }}</p>
      <p v-else-if="error">{{ error }}</p>
      <p v-else>You do not need a perfect opening. Ask for one only if the page feels stuck.</p>
    </div>
    <button type="button" class="text-button mt-3" :disabled="loading" @click="$emit('shuffle')">
      <RefreshCw aria-hidden="true" />
      {{ prompt ? 'Another line' : 'Give me a line' }}
    </button>
  </div>
</template>
