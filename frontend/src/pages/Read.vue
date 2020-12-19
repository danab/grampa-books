<template>
  <q-page style="margin: auto; max-width: 400px">
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
