const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "entry", component: () => import("pages/Entry.vue") },
      { path: "", component: () => import("pages/Read.vue") },
      { path: "search", component: () => import("pages/BookSearch.vue") },
      { path: "leaderboard", component: () => import("pages/Leaderboard.vue") },
      {
        path: "read/:year",
        component: () => import("pages/ReadYear.vue"),
        props: route => ({ year: Number(route.params.year) })
      },
      {
        path: "works/:id",
        component: () => import("pages/Work.vue"),
        props: true
      },
      {
        path: "authors/:id",
        component: () => import("pages/Author.vue"),
        props: true
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "*",
    component: () => import("pages/Error404.vue")
  }
];

export default routes;
