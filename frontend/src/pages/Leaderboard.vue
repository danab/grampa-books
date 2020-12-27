<template>
  <div class="text-center mono">
    <div class="text-h3 q-mt-lg q-mb-md">LEADERS</div>
    <template v-for="(leader, index) in leaders">
      <div v-if="leader.initials" :key="leader.initials">
        <div
          class="row justify-between text-h5"
          style="max-width: 300px; margin: auto;"
        >
          <span class="text-bold">
            {{ index + 1 }}. {{ leader.initials }}
          </span>
          <span class="text-deep-purple">
            {{ leader.num }}
          </span>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "Leaderboard",

  data() {
    return {
      loaded: false,
      leaders: []
    };
  },

  async mounted() {
    const { data } = await this.$axios.get("/leaderboard/");
    console.log(data);

    this.loaded = true;
    this.leaders = data;
  }
};
</script>

<style lang="sass" scoped>
.mono
  font-family: monospace
</style>
