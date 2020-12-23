<template>
  <div v-if="loaded" class="row" style="max-width: 400px; margin: auto">
    <q-card class="col-12 q-mb-sm q-mt-md" flat bordered>
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs">
          <!-- <div class="text-overline">{{ read.date.slice(5) }}</div> -->
          <div class="text-h5 q-mt-sm q-mb-xs">
            {{ work.title }}
          </div>
          <div class="text-subtitle2">
            {{ authors }}
          </div>
          <div class="q-mt-md">
            This book was read
            <span class="text-red">{{ work.reads.length }}</span>
            {{ work.reads.length === 1 ? "time" : "times" }}
            <ul>
              <li v-for="read in work.reads" :key="read.date">
                <router-link
                  class="text-bold"
                  :to="`/read/${read.date.slice(0, 4)}`"
                >
                  {{ read.date }}
                </router-link>
                - <q-btn flat label="Edit Date" @click="editDate(read)" />
              </li>
            </ul>
          </div>
        </q-card-section>

        <q-space />

        <q-card-section class="col-4">
          <q-img
            class="rounded-borders"
            :src="`http://covers.openlibrary.org/b/ID/${work.image_id}-M.jpg`"
          />
        </q-card-section>
      </q-card-section>

      <q-separator />
    </q-card>

    <q-dialog v-model="editDialog">
      <q-card style="width: 300px" class="q-px-sm q-pb-md">
        <q-card-section class="q-pb-sm">
          <div class="text-h6">{{ work.title }}</div>
          <div class="text-bolder">
            {{ authors }}
          </div>
        </q-card-section>

        <q-form @submit="handleUpdateDate">
          <q-card-section class="q-pt-none">
            <q-input v-model="newDate" hide-bottom-space label="Date">
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy
                    ref="qDateProxyStart"
                    transition-show="scale"
                    transition-hide="scale"
                  >
                    <q-date v-model="newDate" mask="YYYY-MM-DD">
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
              v-model="editRead.comment"
              label="Submitter Comment"
              type="textarea"
              rows="3"
              disable
            />
            <q-input
              v-model="editRead.initials"
              label="Initials"
              maxlength="3"
              disable
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              unelevated
              color="primary"
              label="Submit"
              type="submit"
              :loading="submitting"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: "Work",

  props: {
    id: {
      required: true,
      type: String
    }
  },

  data() {
    return {
      editDialog: false,
      editRead: {},
      loaded: false,
      newDate: "",
      submitting: false,
      work: {}
    };
  },

  computed: {
    authors() {
      return this.work.authors.map(author => author.name).join(", ");
    }
  },

  async mounted() {
    const { data } = await this.$axios.get(`/books/${this.id}`);

    this.work = data;
    this.loaded = true;
  },

  methods: {
    editDate(read) {
      this.editDialog = true;
      this.editRead = read;
      this.newDate = read.date;
    },

    async handleUpdateDate() {
      this.submitting = true;

      await this.$axios.post("/edit_read_date/", {
        book_id: this.id,
        date: this.editRead.date,
        new_date: this.newDate
      });

      this.submitting = false;
      this.editDialog = false;

      const idx = this.work.reads.findIndex(read => read === this.editRead);

      this.work.reads[idx].date = this.newDate;
    }
  }
};
</script>
