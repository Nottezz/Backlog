<template>
  <RouterView v-slot="{ Component, route }">
    <Transition name="page" mode="out-in">
      <component :is="Component" :key="route.path" />
    </Transition>
  </RouterView>
  <ToastNotification />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ToastNotification from '@/components/ui/ToastNotification.vue'

const authStore = useAuthStore()

onMounted(async () => {
  // Restore session on app load
  if (authStore.token) {
    await authStore.fetchCurrentUser()
  }
})
</script>
