import Vue from "vue";
import VueRouter from "vue-router";
import AuthGuard from "./utils/auth.guard";
import { adminRoot } from "./constants/config";
import { UserRole } from "./utils/auth.roles";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: () => import(/* webpackChunkName: "home" */ "./views"),
    redirect: `home`,
    meta: { loginRequired: true },
    children: [
      {
        path: "home",
        component: () => import("./views/home/Home.vue"),
      },
      {
        path: "statistics",
        component: () => import("./views/Statistics.vue"),
      },
      {
        path: "horses",
        component: () => import("./views/horses/Horses.vue"),
      },
      {
        path: "reports",
        component: () => import("./views/Reports.vue"),
      },
      {
        path: "admin",
        component: () => import("./views/admin/Admin.vue"),
      },
      {
        path: "pegasus",
        component: () => import("./components/Pegasus/Pegasus.vue"),
      },
      {
        name: "CardioBioReport",
        path: "horse/cardio_bio_report/:measure_id/:id",
        component: () => import("./views/reports/CardioBioReport.vue"),
      },
      {
        name: "DnaCardioBioReport",
        path: "horse/dna_cadio_bio_report/:measure_id/:id",
        component: () => import("./views/reports/DnaCardioBioReport.vue"),
      },
    ],
  },

  {
    path: "/error",
    component: () => import(/* webpackChunkName: "error" */ "./views/Error"),
  },
  {
    path: "/login",
    component: () =>
      import(/* webpackChunkName: "user" */ "./views/user/Login"),
  },
  {
    path: "*",
    component: () => import(/* webpackChunkName: "error" */ "./views/Error"),
  },
];

const router = new VueRouter({
  linkActiveClass: "active",
  routes,
  base: "/velox/vue_index.html/",
  //base: "/",
  mode: "history",
});
router.beforeEach(AuthGuard);
export default router;
