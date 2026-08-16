<script setup lang="ts">
import { ArrowLeft, MessageCircleMore, Trash2 } from 'lucide-vue-next'
import { ApiError } from '~/composables/useLetItOutApi'
import { LETTER_MAX_LENGTH } from '~/types/api'
import type { RecipientType, Tone } from '~/types/api'
import { RECIPIENTS, recipientFor } from '~/data/recipients'

useHead({ title: 'Write a letter - Let It Out' })

type Stage = 'compose' | 'reflecting' | 'reflected' | 'released'

const PENDING_AT = 7000
const route = useRoute()
const api = useLetItOutApi()

const stage = ref<Stage>('compose')
const recipientType = ref<RecipientType>('other')
const tone = ref<Tone>('gentle')
const letterText = ref('')
const prompt = ref<string | null>(null)
const promptLoading = ref(false)
const promptError = ref<string | null>(null)
const reflection = ref('')
const resourceNote = ref('')
const safeToRelease = ref(true)
const errorMessage = ref<string | null>(null)
const ritualOpen = ref(false)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const closingRef = ref<HTMLElement | null>(null)

const addressee = computed(() => recipientFor(recipientType.value).addressee)
const hasLetter = computed(() => letterText.value.trim().length > 0)
const showCrisis = computed(() => !safeToRelease.value && resourceNote.value.length > 0)
const counterClass = computed(() => {
  if (letterText.value.length >= LETTER_MAX_LENGTH) return 'text-danger'
  if (letterText.value.length > PENDING_AT) return 'text-pending'
  return 'text-muted-foreground'
})

const restored = ref(false)
let saveTimer: ReturnType<typeof setTimeout> | null = null

function failureMessage(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.status === 429) {
      return err.retryAfterSeconds
        ? `Wait about ${err.retryAfterSeconds} seconds, then try again. Your draft is still here.`
        : 'Wait a moment, then try again. Your draft is still here.'
    }
    if (err.status === 0) {
      return 'The reflection service could not be reached. Your draft is still here.'
    }
    return err.message
  }
  return 'Something went wrong while requesting the reflection. Your draft is still here.'
}

function quietPromptMessage(err: unknown): string {
  if (err instanceof ApiError && err.status === 429) {
    return err.retryAfterSeconds
      ? `Try another line in about ${err.retryAfterSeconds} seconds.`
      : 'Try another line in a moment.'
  }
  return 'No prompt is available right now. You can still begin anywhere.'
}

async function loadPrompt() {
  promptLoading.value = true
  promptError.value = null
  try {
    const result = await api.getPrompt(recipientType.value)
    prompt.value = result.prompt
  } catch (err) {
    prompt.value = null
    promptError.value = quietPromptMessage(err)
  } finally {
    promptLoading.value = false
  }
}

function autoGrow() {
  const element = textareaRef.value
  if (!element) return
  element.style.height = 'auto'
  element.style.height = `${element.scrollHeight}px`
}

function writeDraft() {
  if (!letterText.value.trim()) return
  writeLetterDraft({
    letterText: letterText.value,
    recipientType: recipientType.value,
    tone: tone.value,
  })
}

watch(letterText, () => nextTick(autoGrow))

watch([letterText, recipientType, tone], () => {
  if (!import.meta.client || !restored.value || stage.value === 'released') return
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(() => {
    saveTimer = null
    writeDraft()
  }, 400)
})

async function submitLetter() {
  if (!hasLetter.value || stage.value === 'reflecting') return
  writeDraft()
  errorMessage.value = null
  stage.value = 'reflecting'

  try {
    const result = await api.reflect({
      letter_text: letterText.value,
      recipient_type: recipientType.value,
      tone: tone.value,
    })
    reflection.value = result.reflection
    safeToRelease.value = result.safe_to_release
    resourceNote.value = result.resource_note ?? ''
    stage.value = 'reflected'
  } catch (err) {
    stage.value = 'compose'
    errorMessage.value = failureMessage(err)
  }
}

function keepWriting() {
  stage.value = 'compose'
  nextTick(() => {
    autoGrow()
    textareaRef.value?.focus()
  })
}

function openRitual() {
  if (!hasLetter.value) return
  writeDraft()
  ritualOpen.value = true
}

function onReleased() {
  stage.value = 'released'
  ritualOpen.value = false
  letterText.value = ''
  reflection.value = ''
  resourceNote.value = ''
  safeToRelease.value = true
  errorMessage.value = null
  clearLetterDraft()
  nextTick(() => closingRef.value?.focus())
}

function startAnother() {
  stage.value = 'compose'
  prompt.value = null
  promptError.value = null
  nextTick(() => {
    autoGrow()
    textareaRef.value?.focus()
  })
}

onMounted(() => {
  const saved = readLetterDraft()
  if (saved) {
    letterText.value = saved.letterText
    recipientType.value = saved.recipientType
    tone.value = saved.tone
  } else {
    const requested = Array.isArray(route.query.recipient)
      ? route.query.recipient[0]
      : route.query.recipient
    if (RECIPIENTS.some((option) => option.value === requested)) {
      recipientType.value = requested as RecipientType
    }
  }

  restored.value = true
  watch(recipientType, () => {
    prompt.value = null
    promptError.value = null
  })
  nextTick(() => {
    autoGrow()
    textareaRef.value?.focus()
  })
})

onBeforeUnmount(() => {
  if (saveTimer) clearTimeout(saveTimer)
  if (stage.value !== 'released') writeDraft()
})
</script>

<template>
  <main class="writer-page">
    <template v-if="stage !== 'released'">
      <header class="writer-heading">
        <InkFlourish class="writer-flourish" />
        <div>
          <h1>Write it exactly as it is.</h1>
          <p>No one here needs you to make it polite, balanced, or easy to answer.</p>
        </div>
        <p class="writer-heading__status">
          Autosaved on this device.<br />
          Reflection uses an AI service.
          <NuxtLink to="/about#your-words">Details</NuxtLink>
        </p>
      </header>

      <div class="writer-grid">
        <aside
          class="writer-tools transition-opacity"
          :class="stage === 'compose' ? '' : 'opacity-55'"
          :inert="stage !== 'compose'"
          aria-label="Letter options"
        >
          <RecipientPicker v-model="recipientType" />
          <PromptCard
            :prompt="prompt"
            :loading="promptLoading"
            :error="promptError"
            @shuffle="loadPrompt"
          />
          <TonePicker v-model="tone" />
        </aside>

        <div>
          <section class="letter-paper writer-sheet" aria-labelledby="letter-salutation">
            <p id="letter-salutation" class="writer-sheet__salutation">Dear {{ addressee }},</p>
            <label for="letter-body" class="sr-only">Your letter</label>
            <textarea
              id="letter-body"
              ref="textareaRef"
              v-model="letterText"
              class="letter-field"
              :maxlength="LETTER_MAX_LENGTH"
              :disabled="stage !== 'compose'"
              placeholder="Start anywhere. It does not have to make sense yet."
              spellcheck="true"
            />
          </section>

          <div class="writer-sheet__meta">
            <span>Saved only in this browser until you request a reflection.</span>
            <span :class="counterClass">{{ letterText.length }} / {{ LETTER_MAX_LENGTH }}</span>
          </div>

          <div v-if="errorMessage" role="alert" class="card mt-5 bg-danger-soft p-4">
            <p class="m-0 text-sm leading-6 text-danger">{{ errorMessage }}</p>
            <button type="button" class="text-button mt-3" @click="submitLetter">Try again</button>
          </div>

          <div v-if="stage === 'compose'" class="writer-actions">
            <button type="button" class="action-button" :disabled="!hasLetter" @click="submitLetter">
              <MessageCircleMore aria-hidden="true" />
              Ask for a reflection
            </button>
            <button type="button" class="text-button" :disabled="!hasLetter" @click="openRitual">
              <Trash2 aria-hidden="true" />
              Release without reflection
            </button>
            <p class="writer-actions__note">Sending for reflection shares the letter for processing.</p>
          </div>

          <div aria-live="polite">
            <p
              v-if="stage === 'reflecting'"
              class="animate-soft-pulse mt-6 font-serif text-lg text-secondary-foreground"
            >
              Reading your letter and preparing one response...
            </p>

            <template v-else-if="stage === 'reflected'">
              <CrisisCard v-if="showCrisis" :note="resourceNote" class="mt-7" />
              <ReflectionPanel v-else :reflection="reflection" :tone="tone" />

              <div class="writer-actions">
                <button
                  v-if="safeToRelease"
                  type="button"
                  class="action-button"
                  @click="openRitual"
                >
                  <Trash2 aria-hidden="true" />
                  Release this draft
                </button>
                <button type="button" :class="safeToRelease ? 'text-button' : 'action-button'" @click="keepWriting">
                  <ArrowLeft aria-hidden="true" />
                  Keep writing
                </button>
                <button v-if="!safeToRelease" type="button" class="text-button" @click="openRitual">
                  Release anyway
                </button>
              </div>
            </template>
          </div>
        </div>
      </div>
    </template>

    <section v-else class="animate-fade-rise mx-auto max-w-xl py-16 text-center">
      <h1 ref="closingRef" tabindex="-1" class="font-serif text-4xl focus:outline-none">
        The browser draft is gone.
      </h1>
      <p class="mt-5 text-base leading-7 text-secondary-foreground">
        It was not sent to the person you wrote to. Take a minute before deciding what comes next.
      </p>
      <div class="mt-9 flex flex-wrap justify-center gap-3">
        <button type="button" class="action-button" @click="startAnother">Write another letter</button>
        <NuxtLink to="/" class="text-button">Back to the start</NuxtLink>
      </div>
    </section>

    <ReleaseRitual
      :open="ritualOpen"
      :letter="letterText"
      @cancel="ritualOpen = false"
      @released="onReleased"
    />
  </main>
</template>
