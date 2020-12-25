<template>
  <q-page v-if="loaded" class="q-pa-sm" style="margin: auto; max-width: 400px">
    <div class="q-pt-sm text-h3">
      {{ author.name }}
    </div>
    <div class="q-mb-sm text-h5">
      <span class="text-indigo">{{ author.books.length }}</span>
      {{ author.books.length === 1 ? "book" : "books" }}
    </div>
    <q-card
      v-for="book in author.books"
      :key="book.ol_id"
      class="col-12 q-mb-sm"
      flat
      bordered
    >
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs">
          <router-link class="revert-link" :to="book.work_id">
            <div class="text-h5 q-mt-sm q-mb-xs">{{ book.title }}</div>
          </router-link>
          <div class="text-subtitle2">{{ author.name }}</div>
        </q-card-section>

        <q-space />

        <q-card-section class="col-4">
          <q-img
            class="rounded-borders"
            :src="`http://covers.openlibrary.org/b/ID/${book.image_id}-M.jpg`"
          />
        </q-card-section>
      </q-card-section>

      <q-separator />
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: "Author",

  props: {
    id: {
      required: true,
      type: String
    }
  },

  data() {
    return {
      author: {},
      loaded: false
    };
  },

  async mounted() {
    const { data } = await this.$axios.get("/authors/" + this.id);

    this.loaded = true;
    this.author = data;
  }
};
</script>
