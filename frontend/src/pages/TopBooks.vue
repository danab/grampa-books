<template>
  <div style="max-width: 400px; margin: auto">
    <div class="text-center text-h3 q-mt-lg q-mb-md">Top Books</div>
    <q-list bordered class="embiggen" separator>
      <q-item
        v-for="(book, index) in books"
        :key="book.work_id"
        v-ripple
        clickable
        :to="book.work_id"
      >
        <q-item-section avatar>
          {{ getIndex(index) }}
        </q-item-section>
        <q-item-section>{{ book.title }} </q-item-section>
        <q-item-section side>{{ book.reads.length }} reads </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
export default {
  name: "Leaderboard",

  data() {
    return {
      loaded: false,
      books: []
    };
  },

  async mounted() {
    const { data } = await this.$axios.get("/books/top/");

    this.loaded = true;
    this.books = data;
  },

  methods: {
    getIndex(index) {
      if (
        index === 0 ||
        this.books[index - 1].reads.length !== this.books[index].reads.length
      ) {
        return index + 1 + ".";
      } else {
        return " - ";
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.embiggen
  font-size: 1.2rem
  font-weight: bold
</style>
