import { ref } from 'vue'

type ToastVariant = 'error' | 'success' | 'info'

interface ToastItem {
  id: number
  message: string
  variant: ToastVariant
}

const toasts = ref<ToastItem[]>([])
let counter = 0

export function useToast() {
  function show(message: string, variant: ToastVariant = 'info', duration = 4000) {
    const id = ++counter
    toasts.value.push({ id, message, variant })
    setTimeout(() => dismiss(id), duration)
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  function error(message: string) {
    show(message, 'error')
  }

  function success(message: string) {
    show(message, 'success')
  }

  return { toasts, show, dismiss, error, success }
}
