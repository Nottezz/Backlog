<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-ink-950/40 backdrop-blur-sm" @click="$emit('close')" />

        <!-- Modal -->
        <div class="relative w-full max-w-lg bg-white rounded-sm shadow-2xl border border-ink-100 flex flex-col max-h-[90vh]">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-ink-100 shrink-0">
            <h2 class="font-display font-bold text-ink-900">
              {{ editMovie ? 'Редактировать фильм' : 'Добавить фильм' }}
            </h2>
            <button @click="$emit('close')" class="p-1 text-ink-400 hover:text-ink-700 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Form -->
          <div class="overflow-y-auto flex-1 px-6 py-5">
            <form id="movie-form" @submit.prevent="handleSubmit" class="flex flex-col gap-4">
              <BaseInput
                v-model="form.title"
                label="Название"
                placeholder="Название фильма"
                required
                :error="errors.title"
              />

              <div class="grid grid-cols-2 gap-4">
                <BaseInput
                  v-model="yearStr"
                  label="Год"
                  type="number"
                  placeholder="2024"
                  :error="errors.year"
                />
                <BaseInput
                  v-model="ratingStr"
                  label="Рейтинг"
                  type="number"
                  placeholder="7.5"
                  hint="от 1 до 10"
                  :error="errors.rating"
                />
              </div>

              <div class="flex flex-col gap-1.5">
                <label class="font-body text-sm font-medium text-ink-700">Описание</label>
                <textarea
                  v-model="form.description"
                  placeholder="Краткое описание фильма (минимум 20 символов)"
                  rows="3"
                  class="input-field resize-none"
                  :class="{ 'error': errors.description }"
                />
                <p v-if="errors.description" class="text-sm text-accent font-body">{{ errors.description }}</p>
              </div>

              <BaseInput
                v-model="form.watchLink"
                label="Ссылка для просмотра"
                placeholder="https://..."
              />

              <div class="flex items-center gap-3">
                <input
                  id="published"
                  v-model="form.published"
                  type="checkbox"
                  class="w-4 h-4 accent-ink-700 rounded"
                />
                <label for="published" class="font-body text-sm text-ink-700 cursor-pointer">
                  Сделать публичным
                </label>
              </div>

              <div v-if="editMovie" class="flex items-center gap-3">
                <input
                  id="watched"
                  v-model="form.watched"
                  type="checkbox"
                  class="w-4 h-4 accent-ink-700 rounded"
                />
                <label for="watched" class="font-body text-sm text-ink-700 cursor-pointer">
                  Просмотрен
                </label>
              </div>
            </form>
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 border-t border-ink-100 flex items-center justify-end gap-3 shrink-0">
            <button type="button" @click="$emit('close')" class="btn-secondary text-sm py-2">
              Отмена
            </button>
            <button
              type="submit"
              form="movie-form"
              class="btn-primary text-sm py-2"
              :disabled="loading"
            >
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              {{ editMovie ? 'Сохранить' : 'Добавить' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { MovieRead } from '@/api/movies'
import BaseInput from './BaseInput.vue'

interface Props {
  show: boolean
  editMovie?: MovieRead | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
  submit: [data: {
    title: string
    description: string | null
    year: number | null
    rating: number | null
    watchLink: string | null
    published: boolean
    watched?: boolean
  }]
}>()

const loading = ref(false)

const form = reactive({
  title: '',
  description: '',
  watchLink: '',
  published: false,
  watched: false,
})
const yearStr = ref('')
const ratingStr = ref('')
const errors = reactive({ title: '', description: '', year: '', rating: '' })

// Populate form when editing
watch(() => props.editMovie, (movie) => {
  if (movie) {
    form.title = movie.title
    form.description = movie.description || ''
    form.watchLink = movie.watchLink || ''
    form.published = movie.published
    form.watched = movie.watched
    yearStr.value = movie.year ? String(movie.year) : ''
    ratingStr.value = movie.rating ? String(movie.rating) : ''
  } else {
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  form.title = ''
  form.description = ''
  form.watchLink = ''
  form.published = false
  form.watched = false
  yearStr.value = ''
  ratingStr.value = ''
  Object.assign(errors, { title: '', description: '', year: '', rating: '' })
}

function validate(): boolean {
  Object.assign(errors, { title: '', description: '', year: '', rating: '' })
  let valid = true

  if (!form.title || form.title.length < 3) {
    errors.title = 'Название должно содержать не менее 3 символов'
    valid = false
  }

  if (form.description && form.description.length > 0 && form.description.length < 20) {
    errors.description = 'Описание должно содержать не менее 20 символов'
    valid = false
  }

  if (yearStr.value && (isNaN(Number(yearStr.value)) || Number(yearStr.value) < 1888)) {
    errors.year = 'Некорректный год'
    valid = false
  }

  if (ratingStr.value) {
    const r = Number(ratingStr.value)
    if (isNaN(r) || r < 1 || r > 10) {
      errors.rating = 'Рейтинг от 1 до 10'
      valid = false
    }
  }

  return valid
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  try {
    emit('submit', {
      title: form.title,
      description: form.description || null,
      year: yearStr.value ? Number(yearStr.value) : null,
      rating: ratingStr.value ? Number(ratingStr.value) : null,
      watchLink: form.watchLink || null,
      published: form.published,
      watched: form.watched,
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: all 0.25s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative, .modal-leave-to .relative {
  transform: translateY(20px) scale(0.98);
}
</style>
