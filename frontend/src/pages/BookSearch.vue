<template>
  <q-page class="q-pa-sm" style="margin: auto; max-width: 400px">
    <div class="q-pt-sm text-h3">
      Book Search
    </div>
    <q-form @submit="handleSearch">
      <q-input ref="search" v-model="title" label="Title">
        <template v-slot:after>
          <q-btn flat icon="search" @click="handleSearch" />
        </template>
      </q-input>
    </q-form>
    <div v-if="loading" class="q-mt-xl text-center">
      <q-spinner size="7rem" />
    </div>
    <div v-else-if="initialSearch" class="q-mt-md">
      <div class="q-my-sm">
        <span class="text-bold text-deep-purple"> {{ results.length }}</span>
        books found for "{{ searchedTitle }}"
      </div>
      <q-card v-for="book in results" :key="book.work_id" class="q-mb-sm">
        <q-card-section class="text-h6 q-mb-none">
          <div class="text-h6">
            <router-link class="revert-link underline" :to="book.work_id">
              {{ book.title }}
            </router-link>
          </div>
          <div class="text-subtitle1">
            {{ authors(book.authors) }}
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "BookSearch",

  data() {
    const initialTitle = this.$route.query.title || "";
    return {
      initialSearch: false,
      loading: false,
      results: [],
      searchedTitle: initialTitle,
      title: initialTitle
    };
  },

  mounted() {
    this.$refs.search.focus();

    if (this.title) {
      this.fetchData(this.title);
    }
  },

  methods: {
    authors(authors) {
      return authors.map(author => author.name).join(", ");
    },

    async fetchData(title) {
      this.loading = true;
      this.initialSearch = true;
      this.searchedTitle = title;
      if (title.trim() !== "") {
        const { data } = await this.$axios.get("/books/search", {
          params: { title }
        });
        this.results = data;
      }

      this.loading = false;
    },

    async handleSearch() {
      this.$router.push({
        path: "/search",
        query: { title: this.title }
      });
    }
  },

  beforeRouteUpdate(to, from, next) {
    this.fetchData(to.query.title);
    this.title = to.query.title;
    next();
  }
};
</script>

<style lang="sass" scoped>
.underline:hover
  text-decoration: underline
</style>
