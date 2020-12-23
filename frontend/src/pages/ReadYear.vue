<template>
  <q-page class="q-pa-sm" style="margin: auto; max-width: 400px">
    <div class="row justify-between q-my-sm">
      <q-btn
        color="secondary"
        icon="arrow_left"
        unelevated
        :label="year - 1"
        :to="'/read/' + (year - 1)"
      />
      <q-btn
        color="secondary"
        icon-right="arrow_right"
        unelevated
        :label="year + 1"
        :to="'/read/' + (year + 1)"
      />
    </div>
    <div v-if="loaded" class="q-mb-xl">
      <div class="text-h2 q-mt-md">{{ year }}</div>
      <div class="text-subtitle1 q-mt-sm q-mb-md">
        {{ combinedReads.length }}
        {{ combinedReads.length === 1 ? "book" : "books" }}
        {{ combinedReads.length > 0 ? "read" : "entered" }}
      </div>
      <q-card
        v-for="read in combinedReads"
        :key="read.book.ol_id"
        class="col-12 q-mb-sm"
        flat
        bordered
      >
        <q-card-section horizontal>
          <q-card-section class="q-pt-xs">
            <div class="text-overline">{{ read.date.slice(5) }}</div>
            <component
              :is="read.unmatched ? 'span' : 'router-link'"
              class="revert-link"
              :to="read.ol_book_id"
            >
              <div class="text-h5 q-mt-sm q-mb-xs">
                {{ read.book.title }}
              </div>
            </component>
            <div class="text-subtitle2">{{ read.book.authors[0].name }}</div>
          </q-card-section>

          <q-space />

          <q-card-section class="col-4">
            <a
              v-if="!read.unmatched"
              target="_BLANK"
              :href="`https://openlibrary.org${read.book.work_id}`"
            >
              <q-img
                class="rounded-borders"
                :src="
                  `http://covers.openlibrary.org/b/ID/${read.book.image_id}-M.jpg`
                "
              />
            </a>
          </q-card-section>
        </q-card-section>

        <q-separator />
      </q-card>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "PageReadYear",

  props: {
    year: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      loaded: false,
      reads: [],
      unmatched: []
    };
  },

  computed: {
    combinedReads() {
      let i = 0;
      let j = 0;

      let combo = [];
      while (i < this.reads.length || j < this.unmatched.length) {
        if (
          !this.reads[i] ||
          (this.unmatched[j] && this.reads[i].date > this.unmatched[j].date)
        ) {
          const fakeRead = {
            unmatched: true,
            date: this.unmatched[j].date,
            book: {
              ol_id: "fake" + this.unmatched[j].read_key,
              title: this.unmatched[j].title,
              authors: [{ name: this.unmatched[j].author }]
            }
          };
          combo.push(fakeRead);
          j += 1;
        } else {
          combo.push(this.reads[i]);
          i += 1;
        }
      }

      return combo;
    }
  },

  async mounted() {
    await this.getReads(this.year);
  },

  methods: {
    async getReads(year) {
      this.loaded = false;
      const { data } = await this.$axios.get(`/reads/year/${year}`);
      this.reads = data.reads;
      this.unmatched = data.unmatched;
      this.loaded = true;
    }
  },

  beforeRouteUpdate(to, from, next) {
    this.getReads(to.params.year);

    next();
  }
};
</script>
