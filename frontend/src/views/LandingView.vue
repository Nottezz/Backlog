<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />

    <main class="flex-1 pt-16">
      <!-- ─── HERO ─── -->
      <section class="relative overflow-hidden border-b border-ink-200">
        <!-- Background texture lines -->
        <div class="absolute inset-0 opacity-[0.03]" aria-hidden="true">
          <div v-for="i in 20" :key="i"
            class="absolute border-t border-ink-900"
            :style="{ top: `${i * 5}%`, left: 0, right: 0 }"
          />
        </div>

        <div class="max-w-6xl mx-auto px-6 py-28 lg:py-36">
          <div class="max-w-3xl">
            <!-- Eyebrow -->
            <div class="flex items-center gap-3 mb-8 animate-fade-in">
              <div class="w-8 h-px bg-accent" />
              <span class="font-mono text-xs tracking-widest text-ink-400 uppercase">Личный кинотеатр</span>
            </div>

            <!-- Headline -->
            <h1 class="font-display text-5xl lg:text-7xl font-bold text-ink-900 leading-[1.05] mb-8 animate-fade-up">
              Все фильмы,<br />
              которые вы хотите<br />
              <em class="text-ink-400 font-normal not-italic">посмотреть</em>
            </h1>

            <p class="font-body text-lg text-ink-500 leading-relaxed mb-12 max-w-xl animate-fade-up" style="animation-delay: 0.1s; opacity: 0; animation-fill-mode: forwards;">
              Backlog — минималистичный трекер фильмов. Сохраняйте, оценивайте
              и отмечайте просмотренное. Никакой лишней информации.
            </p>

            <!-- CTA -->
            <div class="flex flex-wrap gap-4 animate-fade-up" style="animation-delay: 0.2s; opacity: 0; animation-fill-mode: forwards;">
              <RouterLink to="/register" class="btn-primary text-base px-8 py-4">
                Начать бесплатно
              </RouterLink>
              <RouterLink to="/login" class="btn-secondary text-base px-8 py-4">
                Уже есть аккаунт
              </RouterLink>
            </div>
          </div>
        </div>

        <!-- Decorative number -->
        <div class="absolute right-8 bottom-8 font-mono text-[10rem] font-bold text-ink-900 opacity-[0.03] leading-none select-none hidden lg:block" aria-hidden="true">
          01
        </div>
      </section>

      <!-- ─── FEATURES ─── -->
      <section class="max-w-6xl mx-auto px-6 py-24">
        <div class="flex items-center gap-4 mb-16">
          <div class="w-8 h-px bg-accent" />
          <span class="font-mono text-xs tracking-widest text-ink-400 uppercase">Возможности</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-0 border border-ink-100">
          <div v-for="(feature, i) in features" :key="i"
            class="p-8 border-b md:border-b-0 md:border-r border-ink-100 last:border-0 hover:bg-parchment-100 transition-colors group"
          >
            <div class="font-mono text-xs text-ink-300 mb-6">0{{ i + 1 }}</div>
            <div class="text-3xl mb-5">{{ feature.icon }}</div>
            <h3 class="font-display text-xl font-bold text-ink-900 mb-3 group-hover:text-ink-700 transition-colors">
              {{ feature.title }}
            </h3>
            <p class="font-body text-sm text-ink-500 leading-relaxed">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </section>

      <!-- ─── HOW IT WORKS ─── -->
      <section class="bg-ink-900 text-parchment-100">
        <div class="max-w-6xl mx-auto px-6 py-24">
          <div class="flex items-center gap-4 mb-16">
            <div class="w-8 h-px bg-accent" />
            <span class="font-mono text-xs tracking-widest text-parchment-200 opacity-60 uppercase">Как это работает</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-12 lg:gap-16">
            <div v-for="(step, i) in steps" :key="i" class="relative">
              <!-- Step number -->
              <div class="font-display text-7xl font-bold text-parchment-100 opacity-10 leading-none mb-4 select-none">
                {{ i + 1 }}
              </div>
              <h3 class="font-display text-xl font-semibold text-parchment-100 mb-3">
                {{ step.title }}
              </h3>
              <p class="font-body text-sm text-parchment-100 opacity-60 leading-relaxed">
                {{ step.description }}
              </p>
              <!-- Connector line -->
              <div v-if="i < 2" class="hidden md:block absolute top-10 left-full w-16 h-px bg-parchment-100 opacity-10 -translate-y-1/2" />
            </div>
          </div>
        </div>
      </section>

      <!-- ─── FAQ ─── -->
      <section class="max-w-6xl mx-auto px-6 py-24">
        <div class="flex items-center gap-4 mb-16">
          <div class="w-8 h-px bg-accent" />
          <span class="font-mono text-xs tracking-widest text-ink-400 uppercase">Вопросы и ответы</span>
        </div>

        <div class="max-w-2xl">
          <div v-for="(item, i) in faq" :key="i"
            class="border-t border-ink-100 last:border-b"
          >
            <button
              class="w-full flex items-center justify-between py-5 text-left group"
              @click="toggleFaq(i)"
            >
              <span class="font-body font-medium text-ink-900 group-hover:text-ink-600 transition-colors">
                {{ item.q }}
              </span>
              <span class="shrink-0 ml-4 w-5 h-5 rounded-full border border-ink-200 flex items-center justify-center text-ink-400 transition-transform duration-200"
                :class="{ 'rotate-45': openFaq === i }">
                +
              </span>
            </button>
            <Transition name="faq">
              <div v-if="openFaq === i" class="pb-5">
                <p class="font-body text-sm text-ink-500 leading-relaxed">{{ item.a }}</p>
              </div>
            </Transition>
          </div>
        </div>
      </section>

      <!-- ─── CTA FOOTER ─── -->
      <section class="border-t border-ink-200 bg-parchment-100">
        <div class="max-w-6xl mx-auto px-6 py-20 flex flex-col lg:flex-row items-center justify-between gap-8">
          <div>
            <h2 class="font-display text-3xl lg:text-4xl font-bold text-ink-900 mb-2">
              Начните сегодня
            </h2>
            <p class="font-body text-ink-500">Бесплатно. Без лишнего.</p>
          </div>
          <RouterLink to="/register" class="btn-accent text-base px-10 py-4 shrink-0">
            Создать аккаунт →
          </RouterLink>
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
    icon: '📋',
    title: 'Личный список',
    description: 'Добавляйте фильмы с описанием, годом, рейтингом и ссылкой для просмотра. Всё в одном месте.',
  },
  {
    icon: '✓',
    title: 'Отмечайте просмотренное',
    description: 'Простая отметка «просмотрено» помогает видеть прогресс и не возвращаться к одному и тому же.',
  },
  {
    icon: '🔒',
    title: 'Только ваши данные',
    description: 'Каждый список приватен по умолчанию. Публикуйте только то, чем хотите поделиться.',
  },
]

const steps = [
  {
    title: 'Зарегистрируйтесь',
    description: 'Создайте аккаунт за одну минуту, используя email и пароль.',
  },
  {
    title: 'Добавляйте фильмы',
    description: 'Вносите название, год, описание, рейтинг и ссылку на просмотр.',
  },
  {
    title: 'Отслеживайте прогресс',
    description: 'Отмечайте просмотренные фильмы и планируйте, что посмотреть следующим.',
  },
]

const faq = [
  {
    q: 'Это бесплатно?',
    a: 'Да, Backlog полностью бесплатен. Создайте аккаунт и начните пользоваться прямо сейчас.',
  },
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
    a: 'Конечно. Воспользуйтесь функцией «Забыли пароль» на странице входа — мы пришлём ссылку для сброса на ваш email.',
  },
]
</script>

<style scoped>
.faq-enter-active, .faq-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.faq-enter-from, .faq-leave-to {
  opacity: 0;
  max-height: 0;
}
.faq-enter-to, .faq-leave-from {
  opacity: 1;
  max-height: 200px;
}
</style>
