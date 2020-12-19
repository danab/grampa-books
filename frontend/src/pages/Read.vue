<template>
  <q-page style="margin: auto; max-width: 400px">
    <div v-for="year in years" :key="year" class="q-mb-xl"> 
      <div class="text-h2 q-my-md"> {{ year }} </div>
      <q-card v-for="read in getReads(year)" :key="read.book.key" class="col-12 q-mb-sm" flat bordered>
        <q-card-section horizontal>
          <q-card-section class="q-pt-xs">
            <div class="text-overline">{{ read.date.slice(5) }} </div>
            <div class="text-h5 q-mt-sm q-mb-xs">{{ read.book.title }}</div>
            <div class="text-subtitle2">{{ read.book.authors[0].name }} </div>
          </q-card-section>

          <q-space />

          <q-card-section class="col-4">
            <a target="_BLANK" :href="`https://openlibrary.org${read.book.work_id}`" >
              <q-img
                class="rounded-borders"
                :src="`http://covers.openlibrary.org/b/ID/${read.book.image_id}-M.jpg`" 
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
  name: 'PageRead',

  data() {
    return {
      loaded: false,
      reads: []
    }
  },

  async mounted() {
    console.log('updated')
    const { data } = await this.$axios.get('/reads/')

    this.reads = data
    this.loaded = true
  },

  computed: {
    years() {
      return new Set(this.reads.map(read => read.date.slice(0, 4)))
    }
  },

  methods: {
    getReads(year) {
      return this.reads.filter(read => read.date.slice(0, 4) === year)
    }
  }

}
</script>
