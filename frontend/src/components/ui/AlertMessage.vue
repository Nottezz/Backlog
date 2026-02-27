<template>
  <Transition name="alert">
    <div
      v-if="show"
      :class="[
        'flex items-start gap-3 px-4 py-3 rounded-sm border font-body text-sm',
        variants[variant],
      ]"
      role="alert"
    >
      <!-- Icon -->
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
      <button
        v-if="dismissible"
        @click="$emit('dismiss')"
        class="shrink-0 opacity-60 hover:opacity-100 transition-opacity"
      >
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
  error: 'bg-red-50 border-red-200 text-red-800',
  success: 'bg-emerald-50 border-emerald-200 text-emerald-800',
  info: 'bg-amber-50 border-amber-200 text-amber-800',
}
</script>

<style scoped>
.alert-enter-active, .alert-leave-active {
  transition: all 0.3s ease;
}
.alert-enter-from, .alert-leave-to {
  opacity: 0;
  transform: translateY(-8px);
  max-height: 0;
}
.alert-enter-to, .alert-leave-from {
  max-height: 100px;
}
</style>
