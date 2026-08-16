<script setup lang="ts">
import { ArrowDown, ArrowRight, LockKeyhole, RotateCcw } from 'lucide-vue-next'
import { RECIPIENTS, recipientFor } from '~/data/recipients'
import type { RecipientType } from '~/types/api'

useHead({
  title: 'Let It Out - write the letter you will never send',
  meta: [
    {
      name: 'description',
      content:
        'A private writing space for the letter you will never send. Write freely, ask for one reflection, then clear the draft when you are ready.',
    },
  ],
})

const recipientType = ref<RecipientType>('other')
const opening = ref('')
const hasDraft = ref(false)
const touched = ref(false)
let saveTimer: ReturnType<typeof setTimeout> | null = null

const addressee = computed(() => recipientFor(recipientType.value).addressee)
const actionLabel = computed(() => (opening.value.trim() ? 'Continue this letter' : 'Open a blank letter'))

function saveOpening() {
  if (!touched.value || !opening.value.trim()) return
  writeLetterDraft({
    letterText: opening.value,
    recipientType: recipientType.value,
    tone: 'gentle',
  })
  hasDraft.value = true
}

watch([opening, recipientType], () => {
  if (!import.meta.client || !touched.value) return
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(saveOpening, 350)
})

async function beginLetter() {
  if (saveTimer) {
    clearTimeout(saveTimer)
    saveTimer = null
  }
  saveOpening()
  await navigateTo({ path: '/write', query: { recipient: recipientType.value } })
}

onMounted(() => {
  hasDraft.value = readLetterDraft() !== null
})

onBeforeUnmount(() => {
  if (saveTimer) clearTimeout(saveTimer)
  saveOpening()
})
</script>

<template>
  <div class="home-page">
    <section class="letter-hero" aria-labelledby="home-heading">
      <img
        class="letter-hero__image"
        src="/hero-letter-writing.jpg"
        alt="A person writing a letter by hand in warm window light"
        width="1800"
        height="1100"
        fetchpriority="high"
      />
      <div class="letter-hero__wash" aria-hidden="true" />
      <div class="letter-hero__inner">
        <p class="letter-hero__kicker">A private place for unsent words</p>
        <h1 id="home-heading">Let It Out</h1>
        <p class="letter-hero__line">For everything you never got to say.</p>
        <p class="letter-hero__copy">
          Write without preparing for a reply. Take one quiet reflection if you want it, then
          release the draft when you are ready.
        </p>
        <div class="letter-hero__actions">
          <a class="action-button letter-hero__action" href="#begin">
            Begin a letter
            <ArrowDown aria-hidden="true" />
          </a>
          <NuxtLink class="letter-hero__link" to="/about">How your words are handled</NuxtLink>
        </div>
      </div>
      <InkFlourish class="letter-hero__flourish" />
      <div class="letter-hero__folio" aria-hidden="true">
        <span>Private correspondence</span>
        <span>Est. for this moment</span>
      </div>
    </section>

    <div class="home-content">
      <div v-if="hasDraft" class="resume-row">
        <RotateCcw aria-hidden="true" />
        <p>An unfinished letter is saved in this browser.</p>
        <NuxtLink to="/write">Resume it</NuxtLink>
      </div>

      <section id="begin" class="writing-intro" aria-labelledby="begin-heading">
        <div>
          <p class="eyebrow">The blank page</p>
          <h2 id="begin-heading">Begin without an audience.</h2>
        </div>
        <aside class="privacy-note" aria-label="How your letter is handled">
          <LockKeyhole aria-hidden="true" />
          <p>
            Drafts are saved on this device. Asking for a reflection sends the letter to an AI
            service for one response.
            <NuxtLink to="/about#your-words">See exactly how it works.</NuxtLink>
          </p>
        </aside>
      </section>

      <form class="entry-sheet" @submit.prevent="beginLetter">
        <div class="entry-sheet__meta" aria-hidden="true">
          <span>Unsent letter</span>
          <span>No. 01</span>
        </div>
        <div class="entry-sheet__stamp" aria-hidden="true">
          <span>Private</span>
          <strong>Keep</strong>
          <span>or release</span>
        </div>

        <div class="entry-sheet__recipient">
          <label for="home-recipient">Address this to</label>
          <select id="home-recipient" v-model="recipientType">
            <option v-for="recipient in RECIPIENTS" :key="recipient.value" :value="recipient.value">
              {{ recipient.label }}
            </option>
          </select>
        </div>

        <div class="entry-sheet__body">
          <p>Dear {{ addressee }},</p>
          <label class="sr-only" for="home-opening">Begin your letter</label>
          <textarea
            id="home-opening"
            v-model="opening"
            rows="7"
            maxlength="8000"
            placeholder="Start wherever the words begin."
            spellcheck="true"
            @input="touched = true"
          />
        </div>

        <div class="entry-sheet__footer">
          <p>{{ opening.length }} characters</p>
          <button type="submit" class="action-button">
            {{ actionLabel }}
            <ArrowRight aria-hidden="true" />
          </button>
        </div>
      </form>

      <section class="ritual-section" aria-labelledby="ritual-heading">
        <InkFlourish class="ritual-section__flourish" />
        <header class="ritual-section__heading">
          <p class="eyebrow">The ritual</p>
          <h2 id="ritual-heading">A small shape for heavy words.</h2>
          <p>No feed, no reply box, no performance. Just three deliberate steps.</p>
        </header>

        <div class="process-cards">
          <article class="process-card process-card--write">
            <div class="process-card__mark" aria-hidden="true">01</div>
            <p class="process-card__label">Write</p>
            <h3>Say it without editing yourself.</h3>
            <p>The draft stays in this browser while you find the words.</p>
            <span class="process-card__note">No audience</span>
          </article>
          <article class="process-card process-card--reflect">
            <div class="process-card__mark" aria-hidden="true">02</div>
            <p class="process-card__label">Reflect</p>
            <h3>Choose whether you want a response.</h3>
            <p>Ask for one short automated reflection, or skip it entirely.</p>
            <span class="process-card__note">Always optional</span>
          </article>
          <article class="process-card process-card--release">
            <div class="process-card__mark" aria-hidden="true">03</div>
            <p class="process-card__label">Release</p>
            <h3>Let the browser draft leave with you.</h3>
            <p>Press and hold to clear the saved letter from this device.</p>
            <span class="process-card__note">On your timing</span>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>
