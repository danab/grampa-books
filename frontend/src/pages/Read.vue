<template>
  <q-page class="q-pa-sm" style="margin: auto; max-width: 400px">
    <div class="q-mt-sm text-h5 text-center">
      <span class="text-indigo">{{ totalBooks }}</span> books from
      <span class="text-deep-purple">{{ totalYears }}</span> years
    </div>
    <div class="text-subtitle1 text-center">
      (have been entered so far)
    </div>
    <router-link
      v-for="year in years"
      :key="year.year"
      :to="'/read/' + year.year"
      class="revert-link"
    >
      <q-card class="q-my-md bg-secondary text-white q-pa-lg" flat>
        <span class="text-h4">{{ year.year }}</span>
        <span class="text-h5"> - {{ year.num }} books </span>
      </q-card>
    </router-link>
  </q-page>
</template>

<script>
export default {
  name: "PageRead",

  data() {
    return {
      loaded: false,
      years: []
    };
  },

  computed: {
    totalBooks() {
      let books = 0;
      this.years.forEach(year => {
        books += year.num;
      });
      return books;
    },

    totalYears() {
      return this.years.length;
    }
  },

  async mounted() {
    await this.getYears();
  },

  methods: {
    async getYears(year) {
      this.loaded = false;
      const { data } = await this.$axios.get(`/reads/year`);
      this.years = data;
      this.loaded = true;
    }
  }
};
</script>
