<script setup lang="ts">
useHead({
  title: 'Why this exists — Let It Out',
  meta: [
    {
      name: 'description',
      content:
        'What Let It Out is for, what happens to the words you type, what the reflection is and is not, and where to go if you need a person.',
    },
  ],
})
</script>

<template>
  <article class="mx-auto max-w-2xl px-6 py-16 sm:py-24">
    <header v-reveal>
      <p class="eyebrow">Why this exists</p>
      <h1 class="mt-4 font-serif text-3xl leading-tight text-foreground sm:text-4xl">
        The letter you will never send
      </h1>
      <p class="mt-6 text-base leading-8 text-secondary-foreground">
        People have been writing unsent letters for a long time. You write the whole
        thing to someone who will never read it, and then it stays with you, or it
        does not. The point was never the sending. The point is that you finally got
        to say it in full, in your own words, without managing anyone's reaction.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        That is all this is. A quiet page, a sheet of paper, and no one on the other
        end. You can be unfair here. You can repeat yourself. You can write four
        sentences and stop.
      </p>
    </header>

    <section id="your-words" v-reveal="1" class="mt-14 scroll-mt-8">
      <h2 class="font-serif text-2xl leading-snug text-foreground">
        What happens to your words
      </h2>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        You type the letter on your own device. While you are writing, a draft is kept
        in this browser's local storage so that a refresh, a closed tab, or a dropped
        connection does not take it from you. That draft never leaves the browser on
        its own.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        If you ask for a reflection, the text of the letter is sent once, over the
        network, to this app's server, which passes it to an AI model so it can write
        a few sentences back. That is a real request to a real service. We are not
        going to tell you your words never leave the device, because at that moment
        they do.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        This app's backend does not write the letter to a saved-letter database. There
        is no account, no sign-in, and no history to return to here. The AI provider
        still processes the request under its own service terms. When you release the
        letter, the draft saved in this browser is deleted.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        If sending it anywhere at all is more than you want, you can skip the
        reflection entirely. Write the letter, read it back once, and release it. The
        release does not need the network.
      </p>
    </section>

    <section v-reveal="2" class="mt-14">
      <h2 class="font-serif text-2xl leading-snug text-foreground">
        What the reflection is
      </h2>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        A few warm sentences from a model that has just read what you wrote. It is
        meant to sound like someone sitting across from you who heard the whole thing
        and is not in a hurry to fix it.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        It is not a diagnosis. It does not know your history. It will not tell you
        what to do unless you asked it to, and it will not remember you the next time
        you come here. If it says something that does not land, it is wrong and you
        are not. Take it or leave it and go on with the release.
      </p>
    </section>

    <section v-reveal="3" class="mt-14">
      <h2 class="font-serif text-2xl leading-snug text-foreground">The safety check</h2>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        Some letters carry phrases about ending your life or hurting yourself. When
        those turn up, the app holds back the release prompt and shows a short list of
        places you can call instead. It does that because releasing a letter is meant
        to be a small ending, and if that is what is going on, an animation is not the
        right answer.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        Be clear on what is doing the checking: it is a simple keyword match, not a
        clinician. It will sometimes stop on a figure of speech, and it will sometimes
        miss someone who needs help. Your own read on how you are doing is better than
        it is.
      </p>
    </section>

    <section v-reveal="4" class="mt-14">
      <h2 class="font-serif text-2xl leading-snug text-foreground">What this is not</h2>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        It is not therapy. It is not a crisis service, and no one is monitoring what
        you write here. It is not a journal, either: there is nothing to return to,
        by design.
      </p>
      <p class="mt-5 text-base leading-8 text-secondary-foreground">
        If what you need is a person, these are the same numbers the app shows when
        the safety check trips.
      </p>

      <div class="card mt-7 bg-care-soft p-6">
        <p class="eyebrow text-care">If you need to talk to someone</p>
        <ul class="mt-4 space-y-4">
          <li class="text-base leading-7 text-secondary-foreground">
            <span class="font-medium text-foreground">United States</span> — call or
            text
            <a
              href="tel:988"
              class="rounded-sm font-medium text-primary underline underline-offset-4 hover:text-primary-hover"
              >988</a
            >, the Suicide and Crisis Lifeline.
          </li>
          <li class="text-base leading-7 text-secondary-foreground">
            <span class="font-medium text-foreground">United Kingdom</span> — call
            Samaritans on
            <a
              href="tel:116123"
              class="rounded-sm font-medium text-primary underline underline-offset-4 hover:text-primary-hover"
              >116 123</a
            >.
          </li>
          <li class="text-base leading-7 text-secondary-foreground">
            <span class="font-medium text-foreground">Nigeria</span> — call MANI on
            <a
              href="tel:08091116264"
              class="rounded-sm font-medium text-primary underline underline-offset-4 hover:text-primary-hover"
              >0809 111 6264</a
            >.
          </li>
        </ul>
        <p class="mt-5 text-sm leading-6 text-muted-foreground">
          Anywhere else, your local emergency number will point you to someone.
        </p>
      </div>
    </section>

    <section v-reveal="5" class="mt-14 border-t border-border pt-10">
      <p class="text-base leading-8 text-secondary-foreground">
        If you came here to check whether this was safe to use, that was a reasonable
        thing to do. The letter is waiting whenever you are.
      </p>
      <NuxtLink to="/write" class="action-button mt-7">Write the letter</NuxtLink>
    </section>
  </article>
</template>
