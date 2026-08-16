<script setup lang="ts">
import { RECIPIENTS, recipientFor } from '~/data/recipients'
import type { RecipientType } from '~/types/api'

const props = defineProps<{ modelValue: RecipientType }>()
const emit = defineEmits<{ 'update:modelValue': [value: RecipientType] }>()

const selected = computed(() => recipientFor(props.modelValue))
</script>

<template>
  <div class="recipient-picker">
    <label for="recipient-picker" class="field-label">Who is it for?</label>
    <select
      id="recipient-picker"
      class="recipient-select"
      :value="modelValue"
      @change="emit('update:modelValue', ($event.target as HTMLSelectElement).value as RecipientType)"
    >
      <option v-for="option in RECIPIENTS" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <p class="recipient-picker__description">{{ selected.description }}</p>
  </div>
</template>
