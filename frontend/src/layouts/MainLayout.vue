<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          <router-link class="revert-link" to="/">
            JFS Book Log
          </router-link>
        </q-toolbar-title>

        <q-btn flat icon="search" to="/search" />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label header class="text-grey-8">
          Links
        </q-item-label>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from "components/EssentialLink.vue";

const linksData = [
  {
    title: "Search",
    caption: "Search Books",
    icon: "search",
    link: "/search"
  },
  {
    title: "Top Books",
    caption: "By Times Read",
    icon: "leaderboard",
    link: "/top-books"
  },
  {
    title: "Top Authors",
    caption: "By Times Read",
    icon: "star_border",
    link: "/top-authors"
  },
  {
    title: "Home",
    caption: "By Year",
    icon: "book",
    link: "/"
  }
];

export default {
  name: "MainLayout",
  components: { EssentialLink },
  data() {
    return {
      leftDrawerOpen: false,
      essentialLinks: linksData
    };
  }
};
</script>
