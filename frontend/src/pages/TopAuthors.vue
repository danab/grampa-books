<template>
  <div style="max-width: 600px; margin: auto">
    <div class="text-center text-h3 q-mt-lg q-mb-md">Top Authors</div>
    <q-list v-if="loaded" bordered class="embiggen" separator>
      <q-item
        v-for="(author, index) in authors"
        :key="author.ol_id"
        v-ripple
        clickable
        :to="'/authors/' + author.ol_id"
      >
        <q-item-section avatar>
          {{ getIndex(index) }}
        </q-item-section>
        <q-item-section>{{ author.name }} </q-item-section>
        <q-item-section side>{{ author.books.length }} books </q-item-section>
        <q-item-section class="text-green" side>
          {{ getReads(author.books) }} reads
        </q-item-section>
      </q-item>
    </q-list>
    <div v-else class="text-center q-mt-xl">
      <q-spinner size="3rem" />
      <div>Calculating...</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Leaderboard",

  data() {
    return {
      loaded: false,
      authors: []
    };
  },

  async mounted() {
    const { data } = await this.$axios.get("/authors/top");

    this.loaded = true;
    this.authors = data;
  },

  methods: {
    getIndex(index) {
      if (index === 0) {
        return index + 1 + ".";
      }

      const currentReads = this.getReads(this.authors[index].books);
      const previousReads = this.getReads(this.authors[index - 1].books);

      if (currentReads === previousReads) {
        return "-";
      } else {
        return index + 1 + ".";
      }
    },

    getReads(books) {
      return books.reduce((acc, book) => acc + book.reads.length, 0);
    }
  }
};
</script>

<style lang="sass" scoped>
.embiggen
  font-size: 1.2rem
  font-weight: bold
</style>
