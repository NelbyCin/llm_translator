import { createRouter, createWebHistory } from 'vue-router'
import NormalTranslation from '@/views/NormalTranslation.vue'
import DocTranslation from '@/views/DocTranslation.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { name: 'Translation', path: '/', component: NormalTranslation },
    { name: 'DocTranslation', path: '/translate_doc', component: DocTranslation },
  ]
})

export default router
