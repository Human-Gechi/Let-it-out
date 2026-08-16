<script setup lang="ts">
import { TONES } from '~/data/recipients'
import type { Tone } from '~/types/api'

const props = defineProps<{ modelValue: Tone }>()
const emit = defineEmits<{ 'update:modelValue': [value: Tone] }>()

const selected = computed(() => TONES.find((option) => option.value === props.modelValue))
</script>

<template>
  <div class="tone-picker">
    <p id="tone-picker-label" class="field-label">Reflection tone</p>
    <div class="tone-control" role="radiogroup" aria-labelledby="tone-picker-label">
      <label
        v-for="option in TONES"
        :key="option.value"
        :data-selected="modelValue === option.value"
      >
        <input
          class="sr-only"
          type="radio"
          name="lio-tone"
          :value="option.value"
          :checked="modelValue === option.value"
          @change="emit('update:modelValue', option.value)"
        />
        <span>{{ option.label }}</span>
        <span class="sr-only">. {{ option.description }}</span>
      </label>
    </div>
    <p class="tone-picker__description">{{ selected?.description }}</p>
  </div>
</template>
