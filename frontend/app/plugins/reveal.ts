/** Reveals longer-form content once it enters the viewport. */

const STEP_MS = 80

export default defineNuxtPlugin((nuxtApp) => {
  // The directive is registered on both sides so SSR can resolve it; only the
  // mounted hook runs in the browser, which is where the observer lives.
  nuxtApp.vueApp.directive('reveal', {
    mounted(el: HTMLElement, binding) {
      const step = typeof binding.value === 'number' ? binding.value : 0
      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

      if (reduced) {
        el.dataset.reveal = 'revealed'
        return
      }

      el.dataset.reveal = 'pending'
      el.style.setProperty('--reveal-delay', `${step * STEP_MS}ms`)

      const observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (!entry.isIntersecting) continue
            el.dataset.reveal = 'revealed'
            observer.disconnect()
          }
        },
        { threshold: 0.1, rootMargin: '0px 0px -40px 0px' },
      )

      observer.observe(el)
      ;(el as HTMLElement & { _revealObserver?: IntersectionObserver })._revealObserver = observer
    },

    unmounted(el: HTMLElement & { _revealObserver?: IntersectionObserver }) {
      el._revealObserver?.disconnect()
    },
  })
})
