<template>
  <button
    type="button"
    role="switch"
    :aria-checked="modelValue"
    :aria-label="label"
    class="flex items-center gap-3 group focus:outline-none"
    @click="$emit('update:modelValue', !modelValue)"
  >
    <!-- Track -->
    <div
      :class="[
        'relative w-10 h-6 rounded-full transition-colors duration-200 flex-shrink-0',
        modelValue ? 'bg-accent' : 'bg-base-200',
        'group-focus-visible:ring-2 group-focus-visible:ring-accent/40 group-focus-visible:ring-offset-2',
      ]"
    >
      <!-- Thumb -->
      <div
        :class="[
          'absolute top-1 w-4 h-4 bg-white rounded-full shadow-sm transition-transform duration-200',
          modelValue ? 'translate-x-5' : 'translate-x-1',
        ]"
      />
    </div>

    <!-- Label -->
    <span v-if="label" class="font-body text-sm text-base-700 select-none cursor-pointer">
      {{ label }}
    </span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  label?: string
}>()

defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>
