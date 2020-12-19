<template>
  <q-page class="q-pa-sm" style="margin: auto; max-width: 400px">
    <q-form class="row q-my-md" @submit="handleSearch">
      <q-input
        ref="search"
        v-model="searchTerm"
        class="col-8"
        label="Title and/or Author"
      />
      <q-btn
        class="col-4"
        label="Search"
        type="submit"
        :loading="loading"
        unelevated
        color="primary"
      />
    </q-form>
    <div v-if="!loading" class="row">
      <q-card
        v-for="book in filteredResults"
        :key="book.key"
        class="col-12 q-mb-sm"
        flat
        bordered
      >
        <q-card-section horizontal>
          <q-card-section class="q-pt-xs">
            <div class="text-overline">
              {{ book.author_name && book.author_name[0] }}
            </div>
            <div class="text-h5 q-mt-sm q-mb-xs">{{ book.title }}</div>
            <div class="text-caption text-grey">
              First Published: {{ book.first_publish_year || " Unknown" }}
              <!-- <pre>
                {{ book }}
              </pre> -->
            </div>
          </q-card-section>

          <q-space />

          <q-card-section class="col-4">
            <q-img
              class="rounded-borders"
              :src="`http://covers.openlibrary.org/b/ID/${book.cover_i}-M.jpg`"
            />
          </q-card-section>
        </q-card-section>

        <q-separator />

        <q-card-actions class="row justify-between">
          <q-btn
            type="a"
            external
            target="_BLANK"
            :href="`https://openlibrary.org${book.key}`"
            label="More Info"
            unelevated
            color="primary"
          />
          <q-btn unelevated color="secondary" @click="handleSelect(book)">
            Select
          </q-btn>
        </q-card-actions>
      </q-card>
      <!-- {{ book.author_name }}
        {{ book.cover_i }}
        <img :src="`http://covers.openlibrary.org/b/ID/${book.cover_i}-M.jpg`" /> -->
    </div>
    <q-dialog v-model="chooseDialog">
      <q-card style="width: 300px" class="q-px-sm q-pb-md">
        <q-card-section class="q-pb-sm">
          <div class="text-h6">{{ selectedBook.title }}</div>
          <div class="text-bolder">
            {{ selectedBook.author_name && selectedBook.author_name[0] }}
          </div>
        </q-card-section>

        <q-form @submit="handleReadSubmit">
          <q-card-section class="q-pt-none">
            <q-input
              v-model="date"
              hide-bottom-space
              label="Read Date"
              :rules="[required('Choose a Date')]"
            >
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy
                    ref="qDateProxyStart"
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date v-model="date" mask="YYYY-MM-DD">
                      <div class="row items-center justify-end">
                        <q-btn
                          v-close-popup
                          label="Close"
                          color="primary"
                          flat
                        />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input
              v-model="submitterComment"
              label="Submitter Comment"
              type="textarea"
              rows="3"
            />
            <q-input v-model="initials" label="Initials" maxlength="3" />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn unelevated color="primary" label="Submit" type="submit" />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
export default {
  name: "PageIndex",

  data() {
    return {
      chooseDialog: false,
      date: "2020-12-13",
      initials: "",
      submitterComment: "",
      loading: false,
      results: [],
      searchTerm: "",
      selectedBook: {}
    };
  },

  computed: {
    // Require results to have an author...for now.
    filteredResults() {
      return this.results
        .filter(book => {
          if (!book.language?.includes("eng")) {
            console.log(JSON.parse(JSON.stringify(book)));
          }
          return (
            book.author_name?.length &&
            (!book.language || book.language.includes("eng"))
          );
        })
        .slice(0, 10);
    }
  },

  mounted() {
    this.$refs.search.focus();
  },

  methods: {
    handleSelect(book) {
      this.selectedBook = book;
      this.chooseDialog = true;
    },

    // This sucks, update author -> book -> read
    async handleReadSubmit() {
      await Promise.allSettled(
        this.selectedBook.author_key.map((key, i) => {
          return this.$axios.post("/authors/", {
            ol_id: key,
            name: this.selectedBook.author_name[i]
          });
        })
      );

      try {
        await this.$axios.post("/books/", {
          work_id: this.selectedBook.key,
          edition_id: "edition_id",
          image_id: this.selectedBook.cover_i,
          title: this.selectedBook.title,
          author_ol_ids: this.selectedBook.author_key
        });
      } catch (e) {
        if (e?.response?.status !== 400) {
          throw new Error("An error occurred!");
        }
      }

      try {
        await this.$axios.post("/reads/", {
          date: this.date,
          ol_book_id: this.selectedBook.key,
          submitter_comment: this.submitterComment,
          initials: this.initials
        });
      } catch (e) {
        throw new Error("An error occurred!");
      }

      this.submitterComment = "";
      this.chooseDialog = false;
    },

    async handleSearch() {
      const url = `http://openlibrary.org/search.json?q=${this.searchTerm}`;

      this.loading = true;

      const { data } = await this.$axios.get(url);

      this.results = data.docs;
      this.loading = false;
    },

    required(errorMsg) {
      return val => (val !== null && val !== "") || errorMsg;
    }
  }
};
</script>
