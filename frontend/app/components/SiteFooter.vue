<script setup lang="ts">
const year = new Date().getFullYear()

const CRISIS_LINES = [
  { region: 'US', display: '988', tel: '988' },
  { region: 'UK', display: '116 123', tel: '116123' },
  { region: 'Nigeria', display: '0809 111 6264', tel: '08091116264' },
]
</script>

<template>
  <footer class="site-footer">
    <InkFlourish class="site-footer__flourish" />
    <div class="site-footer__inner">
      <div class="site-footer__letterhead">
        <div class="site-footer__brand">
          <LogoMark class="h-5 w-5" />
          <Wordmark class="text-[18px]" />
        </div>
        <p class="site-footer__statement">
          Some words need somewhere to go,<br />not someone to receive them.
        </p>
        <p>
          There is no account and no public posting. Your saved draft stays in this browser unless
          you request an AI reflection.
        </p>
      </div>

      <nav class="site-footer__nav" aria-label="Footer navigation">
        <h2>Continue</h2>
        <ul class="site-footer__links">
          <li><NuxtLink to="/write">Write a letter</NuxtLink></li>
          <li><NuxtLink to="/about">About the space</NuxtLink></li>
          <li><NuxtLink to="/about#your-words">Your words and privacy</NuxtLink></li>
        </ul>
      </nav>

      <div class="site-footer__safety">
        <h2>This is not a crisis service</h2>
        <p>If you may hurt yourself or feel unsafe, call someone who can stay with you.</p>
        <ul class="site-footer__lines">
          <li v-for="line in CRISIS_LINES" :key="line.tel">
            <span>{{ line.region }}</span>
            <a :href="`tel:${line.tel}`">{{ line.display }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div class="site-footer__base">
      <p>&copy; {{ year }} Let It Out</p>
      <p>
        Hero photograph by
        <a href="https://www.pexels.com/photo/elegant-woman-writing-a-letter-by-sunlit-desk-37713506/" target="_blank" rel="noreferrer">
          Alexander Mass / Pexels
        </a>
      </p>
    </div>
  </footer>
</template>
