<template>
  <header class="site-header">
    <div class="site-header__inner">
      <NuxtLink to="/" class="brand-link" aria-label="Let It Out home">
        <LogoMark />
        <Wordmark class="text-[19px]" />
      </NuxtLink>

      <nav class="header-nav" aria-label="Main navigation">
        <NuxtLink to="/about" class="header-link">How your words move</NuxtLink>
        <NuxtLink to="/write" class="action-button">Write</NuxtLink>
        <!-- Hidden while light mode is commented out: Dark is the only choice. -->
        <!-- <ThemeMenu /> -->
      </nav>
    </div>
  </header>
</template>
