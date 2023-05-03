import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import Dashboard from "../views/Dashboard.vue";
import ForgotPassword from "../views/ForgotPassword.vue";
import DashboardHome from "../views/dashboard/Home.vue";
import DashboardAnalyze from "../views/dashboard/Analyze.vue";
import DashboardGenerate from "../views/dashboard/Generate.vue";
import DashboardView from "../views/dashboard/View.vue";
import DashboardSettings from "../views/dashboard/Settings.vue";
import DashboardInfo from "../views/dashboard/Info.vue";
import {getAuth} from 'firebase/auth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AboutView
    },
    {
      path: '/forgot_password',
      name: 'forgot',
      component: ForgotPassword
    },
    {
      path: "/dashboard",
      component: Dashboard,
      meta: {requresAuth: true},
      children: [
        {
          path: "",
          component: DashboardHome,
        },
        {
          path: "analyze-report",
          component: DashboardAnalyze,
        },
        {
          path: "generate-report",
          component: DashboardGenerate,
        },
        {
          path: "view-report",
          component: DashboardView,
        },
        {
          path: "settings",
          component: DashboardSettings,
        },
        {
          path: "info",
          component: DashboardInfo,
        },
      ],
    },
  ]
})
//Router guard so login is required
router.beforeEach((to, from, next) => {
  const auth = getAuth()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !auth.currentUser) {
    next({ name: 'home' }) // Redirect to home page if user is not logged in
  } else {
    next()
  }
})
export default router
