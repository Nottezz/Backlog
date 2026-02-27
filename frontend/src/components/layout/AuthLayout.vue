<template>
  <div class="min-h-screen bg-parchment-50 flex flex-col">
    <!-- Decorative top stripe -->
    <div class="h-1 bg-ink-900" />

    <div class="flex-1 flex items-center justify-center px-4 py-16">
      <div class="w-full max-w-md">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center justify-center gap-2 mb-10 group">
          <span class="font-display text-2xl font-bold text-ink-900">Backlog</span>
        </RouterLink>

        <!-- Card -->
        <div class="card p-8 shadow-md">
          <slot />
        </div>

        <!-- Footer links -->
        <div class="mt-6 text-center">
          <slot name="footer" />
        </div>
      </div>
    </div>

    <!-- Decorative bottom -->
    <div class="h-1 bg-ink-900" />
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
