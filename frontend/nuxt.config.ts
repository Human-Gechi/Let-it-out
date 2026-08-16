import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-08-01',
  future: { compatibilityVersion: 4 },
  devtools: { enabled: false },
  ssr: true,

  css: ['~/assets/css/main.css'],

  components: [{ path: '~/components', pathPrefix: false }],

  vite: {
    plugins: [tailwindcss()],
  },

  runtimeConfig: {
    public: {
      // FastAPI backend. Override with NUXT_PUBLIC_API_BASE.
      apiBase: 'http://127.0.0.1:8000',
    },
  },

  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      title: 'Let It Out — write the letter you will never send',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Write the letter you never sent. Keep the draft in this browser, ask for one reflection if you want it, then clear it when you are ready.',
        },
        { name: 'theme-color', content: '#f1ecef' },
      ],
      link: [{ rel: 'icon', href: '/favicon.svg', type: 'image/svg+xml' }],
      script: [
        {
          // Applies the stored theme before first paint so the page never flashes.
          innerHTML: `(function(){try{var t=localStorage.getItem('lio-theme')||'light';var d=t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.toggle('dark',d);document.documentElement.dataset.theme=t}catch(e){}})()`,
          tagPosition: 'head',
        },
      ],
    },
  },
})
