<script setup lang="ts">
// Nuxt renders this route on the server too, so the response carries a real 404.
const event = useRequestEvent()
if (event) setResponseStatus(event, 404)

useHead({ title: 'This page was never written — Let It Out' })
</script>

<template>
  <section class="mx-auto max-w-2xl px-6 py-16 sm:py-24">
    <p class="eyebrow">404</p>
    <h1 class="mt-4 font-serif text-3xl leading-tight text-foreground sm:text-4xl">
      This page was never written
    </h1>
    <p class="mt-6 text-base leading-8 text-secondary-foreground">
      There is nothing at this address. Nothing was lost — it simply never existed.
    </p>

    <div class="mt-10 flex flex-wrap items-center gap-4">
      <NuxtLink to="/" class="action-button">Back to the beginning</NuxtLink>
      <NuxtLink
        to="/write"
        class="text-sm font-medium text-secondary-foreground underline underline-offset-4 hover:text-primary"
      >
        Or start a letter
      </NuxtLink>
    </div>
  </section>
</template>
