<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />

    <main class="flex-1 pt-[60px]">
      <!-- ─── HERO ─── -->
      <section class="relative overflow-hidden bg-base-950 text-white">
        <!-- Gradient orbs -->
        <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
          <div class="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] rounded-full bg-accent/20 blur-[120px]" />
          <div class="absolute bottom-[-20%] right-[-5%] w-[400px] h-[400px] rounded-full bg-accent-300/10 blur-[100px]" />
        </div>

        <div class="relative max-w-6xl mx-auto px-6 py-28 lg:py-36">
          <!-- Eyebrow badge -->
          <div class="inline-flex items-center gap-2 bg-white/10 border border-white/10 rounded-full px-4 py-1.5 mb-10 animate-fade-in">
            <span class="w-1.5 h-1.5 rounded-full bg-accent-300 animate-pulse" />
            <span class="font-body text-xs text-white/70 tracking-wide">Личный трекер фильмов</span>
          </div>

          <!-- Headline -->
          <h1 class="font-display text-5xl lg:text-[4.5rem] font-bold leading-[1.05] mb-7 animate-fade-up max-w-3xl">
            Ваши фильмы —<br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-accent-300 to-accent-400">
              под контролем
            </span>
          </h1>

          <p class="font-body text-lg text-white/60 leading-relaxed mb-12 max-w-xl animate-fade-up"
            style="animation-delay:0.1s;opacity:0;animation-fill-mode:forwards">
            Сохраняйте фильмы в личный список, оценивайте просмотренное
            и планируйте, что посмотреть следующим.
          </p>

          <!-- CTA -->
          <div class="flex flex-wrap gap-4 animate-fade-up"
            style="animation-delay:0.2s;opacity:0;animation-fill-mode:forwards">
            <RouterLink to="/register"
              class="inline-flex items-center gap-2 px-7 py-3.5 bg-accent hover:bg-accent-600 text-white font-display font-semibold rounded-xl transition-all shadow-lg shadow-accent/30 hover:shadow-accent/40 text-base">
              Начать →
            </RouterLink>
            <RouterLink to="/login"
              class="inline-flex items-center gap-2 px-7 py-3.5 bg-white/10 hover:bg-white/15 border border-white/10 text-white font-body font-medium rounded-xl transition-all text-base">
              Уже есть аккаунт
            </RouterLink>
          </div>
        </div>
      </section>

      <!-- ─── FEATURES ─── -->
      <section class="max-w-6xl mx-auto px-6 py-24">
        <div class="text-center mb-16">
          <p class="font-mono text-xs tracking-widest text-base-400 uppercase mb-3">Возможности</p>
          <h2 class="font-display text-3xl lg:text-4xl font-bold text-base-900">
            Всё, что нужно для кино-списка
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="(feature, i) in features" :key="i"
            class="card p-7 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 group">
            <div
              class="w-11 h-11 rounded-2xl flex items-center justify-center text-xl mb-5"
              :class="feature.bg"
            >
              {{ feature.icon }}
            </div>
            <h3 class="font-display font-bold text-base-900 text-lg mb-2 group-hover:text-accent transition-colors">
              {{ feature.title }}
            </h3>
            <p class="font-body text-sm text-base-500 leading-relaxed">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </section>

      <!-- ─── HOW IT WORKS ─── -->
      <section class="bg-surface-muted border-y border-surface-border">
        <div class="max-w-6xl mx-auto px-6 py-24">
          <div class="text-center mb-16">
            <p class="font-mono text-xs tracking-widest text-base-400 uppercase mb-3">Как это работает</p>
            <h2 class="font-display text-3xl lg:text-4xl font-bold text-base-900">
              Три шага до порядка
            </h2>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            <!-- Connector -->
            <div class="hidden md:block absolute top-8 left-1/3 right-1/3 h-px bg-surface-border" />

            <div v-for="(step, i) in steps" :key="i" class="relative text-center">
              <div class="w-16 h-16 rounded-2xl bg-base-950 text-white font-display font-bold text-2xl flex items-center justify-center mx-auto mb-5 shadow-lg">
                {{ i + 1 }}
              </div>
              <h3 class="font-display font-bold text-base-900 text-lg mb-2">{{ step.title }}</h3>
              <p class="font-body text-sm text-base-500 leading-relaxed max-w-xs mx-auto">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ─── FAQ ─── -->
      <section class="max-w-6xl mx-auto px-6 py-24">
        <div class="text-center mb-16">
          <p class="font-mono text-xs tracking-widest text-base-400 uppercase mb-3">FAQ</p>
          <h2 class="font-display text-3xl lg:text-4xl font-bold text-base-900">
            Вопросы и ответы
          </h2>
        </div>

        <div class="max-w-2xl mx-auto divide-y divide-surface-border">
          <div v-for="(item, i) in faq" :key="i">
            <button
              class="w-full flex items-center justify-between py-5 text-left group"
              @click="toggleFaq(i)"
            >
              <span class="font-body font-medium text-base-900 group-hover:text-accent transition-colors pr-4">
                {{ item.q }}
              </span>
              <span
                class="shrink-0 w-7 h-7 rounded-lg bg-surface-muted border border-surface-border flex items-center justify-center text-base-500 transition-all duration-200"
                :class="{ 'bg-accent border-accent text-white rotate-45': openFaq === i }"
              >
                +
              </span>
            </button>
            <Transition name="faq">
              <div v-if="openFaq === i" class="pb-5">
                <p class="font-body text-sm text-base-500 leading-relaxed">{{ item.a }}</p>
              </div>
            </Transition>
          </div>
        </div>
      </section>

      <!-- ─── CTA ─── -->
      <section class="bg-base-950 text-white">
        <div class="max-w-6xl mx-auto px-6 py-20">
          <div class="relative rounded-3xl bg-gradient-to-br from-accent-700 to-accent p-12 lg:p-16 overflow-hidden text-center">
            <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
              <div class="absolute top-[-30%] right-[-10%] w-[300px] h-[300px] rounded-full bg-white/10 blur-[60px]" />
            </div>
            <h2 class="relative font-display text-3xl lg:text-4xl font-bold mb-4">
              Начните прямо сейчас
            </h2>
            <p class="relative font-body text-white/70 mb-10 text-lg max-w-md mx-auto">
              Создайте аккаунт и ведите свой список фильмов
            </p>
            <RouterLink to="/register"
              class="inline-flex items-center gap-2 px-8 py-4 bg-white text-accent-700 font-display font-bold rounded-xl hover:bg-accent-50 transition-all shadow-xl text-base">
              Создать аккаунт →
            </RouterLink>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const openFaq = ref<number | null>(null)
function toggleFaq(i: number) {
  openFaq.value = openFaq.value === i ? null : i
}

const features = [
  {
    icon: '🎬',
    bg: 'bg-violet-50',
    title: 'Личный список',
    description: 'Добавляйте фильмы с названием, описанием, годом, рейтингом и ссылкой для просмотра.',
  },
  {
    icon: '✅',
    bg: 'bg-emerald-50',
    title: 'Отметки о просмотре',
    description: 'Отмечайте просмотренные фильмы одним нажатием и следите за прогрессом.',
  },
  {
    icon: '🔐',
    bg: 'bg-blue-50',
    title: 'Приватность',
    description: 'Каждый фильм приватен по умолчанию. Публикуйте только то, чем хотите поделиться.',
  },
]

const steps = [
  {
    title: 'Создайте аккаунт',
    description: 'Зарегистрируйтесь с помощью email — это займёт меньше минуты.',
  },
  {
    title: 'Добавляйте фильмы',
    description: 'Название, год, описание, рейтинг и ссылка — всё опционально.',
  },
  {
    title: 'Следите за прогрессом',
    description: 'Отмечайте просмотренное и планируйте, что посмотреть следующим.',
  },
]

const faq = [
  {
    q: 'Могу ли я поделиться своим списком?',
    a: 'Да. Каждый фильм можно сделать публичным. По умолчанию список виден только вам.',
  },
  {
    q: 'Как добавить фильм?',
    a: 'После входа нажмите кнопку «Добавить фильм», заполните название и любые дополнительные поля — всё остальное опционально.',
  },
  {
    q: 'Можно ли изменить пароль?',
    a: 'Да. Воспользуйтесь функцией «Забыли пароль» на странице входа — мы пришлём ссылку для сброса на ваш email.',
  },
  {
    q: 'Как связаться с поддержкой?',
    a: 'Напишите нам на admin@backlog-movie.ru — ответим в течение рабочего дня.',
  },
]
</script>

<style scoped>
.faq-enter-active, .faq-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.faq-enter-from, .faq-leave-to { opacity: 0; max-height: 0; }
.faq-enter-to, .faq-leave-from { opacity: 1; max-height: 200px; }
</style>
