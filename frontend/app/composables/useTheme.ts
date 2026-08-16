export type Theme = 'light' | 'dark' | 'system'

const STORAGE_KEY = 'lio-theme'

function isTheme(value: unknown): value is Theme {
  return value === 'light' || value === 'dark' || value === 'system'
}

/**
 * Light mode is commented out for now — the app is dark only, so this just
 * pins <html> to dark and ignores both the stored choice and the OS setting.
 * Uncomment the block below (and the options in ThemeMenu) to bring it back.
 */
export function useTheme() {
  const theme = useState<Theme>('lio-theme', () => 'dark')

  onMounted(() => {
    document.documentElement.classList.add('dark')
    document.documentElement.dataset.theme = 'dark'
  })

  // const theme = useState<Theme>('lio-theme', () => 'light')
  //
  // onMounted(() => {
  //   const stored = window.localStorage.getItem(STORAGE_KEY)
  //   if (isTheme(stored)) theme.value = stored
  //
  //   const media = window.matchMedia('(prefers-color-scheme: dark)')
  //
  //   const apply = () => {
  //     const dark = theme.value === 'dark' || (theme.value === 'system' && media.matches)
  //     document.documentElement.classList.toggle('dark', dark)
  //     document.documentElement.dataset.theme = theme.value
  //   }
  //
  //   const stop = watch(theme, (next) => {
  //     window.localStorage.setItem(STORAGE_KEY, next)
  //     apply()
  //   })
  //
  //   apply()
  //   media.addEventListener('change', apply)
  //
  //   onBeforeUnmount(() => {
  //     stop()
  //     media.removeEventListener('change', apply)
  //   })
  // })

  return { theme, setTheme: (next: Theme) => (theme.value = next) }
}
