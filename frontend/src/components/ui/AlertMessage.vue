<template>
  <Transition name="alert">
    <div
      v-if="show"
      :class="[
        'flex items-start gap-3 px-4 py-3 rounded-xl border font-body text-sm',
        variants[variant],
      ]"
      role="alert"
    >
      <span class="shrink-0 mt-0.5">
        <svg v-if="variant === 'error'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else-if="variant === 'success'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </span>
      <div class="flex-1">
        <slot>{{ message }}</slot>
      </div>
      <button v-if="dismissible" @click="$emit('dismiss')" class="shrink-0 opacity-60 hover:opacity-100 transition-opacity">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
interface Props {
  show?: boolean
  variant?: 'error' | 'success' | 'info'
  message?: string
  dismissible?: boolean
}

withDefaults(defineProps<Props>(), {
  show: true,
  variant: 'info',
  dismissible: false,
})

defineEmits<{ dismiss: [] }>()

const variants = {
  error:   'bg-red-50 border-red-100 text-red-700',
  success: 'bg-emerald-50 border-emerald-100 text-emerald-700',
  info:    'bg-accent-50 border-accent-100 text-accent-700',
}
</script>

<style scoped>
.alert-enter-active, .alert-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.alert-enter-from, .alert-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.alert-enter-to, .alert-leave-from {
  max-height: 120px;
}
</style>
