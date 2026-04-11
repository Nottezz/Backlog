import { ref } from 'vue'
import { moviesApi, type MovieRead } from '@/api/movies.ts'

export function useMovieRoulette() {
  const pickedMovie = ref<MovieRead | null>(null)
  const excludedIds = ref<number[]>([])
  const loading = ref(false)
  const exhausted = ref(false)
  const isOpen = ref(false)

  async function spin() {
    loading.value = true
    exhausted.value = false

    try {
      const movie = await moviesApi.getRandom(excludedIds.value)
      pickedMovie.value = movie
    } catch (e: unknown) {
      const err = e as { response?: { status?: number } }
      if (err.response?.status === 404) {
        exhausted.value = true
        pickedMovie.value = null
      }
    } finally {
      loading.value = false
    }
  }

  // Убрать текущий фильм из пула и сразу крутить снова
  async function reject() {
    if (pickedMovie.value) {
      excludedIds.value.push(pickedMovie.value.id)
      pickedMovie.value = null
      await spin()
    }
  }

  // Открыть рулетку и сразу сделать первый выбор
  async function open() {
    isOpen.value = true
    await spin()
  }

  // Закрыть и сбросить всё состояние
  function close() {
    isOpen.value = false
    pickedMovie.value = null
    excludedIds.value = []
    exhausted.value = false
    loading.value = false
  }

  // Начать заново, не закрывая модалку
  async function restart() {
    excludedIds.value = []
    exhausted.value = false
    pickedMovie.value = null
    await spin()
  }

  return {
    pickedMovie,
    excludedIds,
    loading,
    exhausted,
    isOpen,
    open,
    close,
    spin,
    reject,
    restart,
  }
}
