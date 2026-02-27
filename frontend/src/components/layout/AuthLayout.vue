<template>
  <div class="min-h-screen bg-surface-soft flex flex-col">
    <!-- Gradient top accent -->
    <div class="h-1 bg-gradient-to-r from-accent-700 via-accent to-accent-300" />

    <div class="flex-1 flex items-center justify-center px-4 py-16">
      <div class="w-full max-w-md">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center justify-center gap-2.5 mb-10 group">
          <div class="w-9 h-9 rounded-xl bg-accent flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l7.59-7.59L21 8l-9 9z"/>
            </svg>
          </div>
          <span class="font-display font-bold text-2xl text-base-900 tracking-tight group-hover:text-accent transition-colors">
            Backlog
          </span>
        </RouterLink>

        <!-- Card -->
        <div class="card p-8 shadow-xl shadow-base-100/50">
          <slot />
        </div>

        <!-- Footer slot -->
        <div class="mt-5 text-center">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
