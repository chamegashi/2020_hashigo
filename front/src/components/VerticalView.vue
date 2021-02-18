<template>
  <div>

    <div class="button">
      <b-button v-on:click="moveToButtom()" @keyup.up="changeSpeed(1)" @keyup.down="changeSpeed(-1)" variant="primary">下にスクロール</b-button>
      <p>下にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div id="underBox" class="underbox">
      <div v-for="(word, index) in words" :key="index" class="showword">
        <p class="showSentence">{{word}}</p>
      </div>
    </div>

    <div class="button">
      <b-button v-on:click="moveToTOP()" variant="primary">TOP に戻る</b-button>
    </div>

  </div>
</template>

<script>
export default {
  props: {
    words: Array
  },
  data: () => ({
    is_loading: false,
    input_text: '',
    step: 2
  }),
  created () {

  },
  methods: {
    goInput () {
      this.$router.push({name: 'input'})
    },
    moveToButtom () {
      var e = document.getElementById('underBox')
      const height = parseInt(e.offsetHeight) - 450
      const interval = 25

      const timer = setInterval(() => {
        window.scrollBy(0, this.step)
        if(window.scrollY >= height) {
          clearInterval(timer)
        }
      }
      , interval)
    },
    moveToTOP () {
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      })
    },
    changeSpeed (diff) {
      this.step = this.step + diff
    }
  }
}
</script>

<style scoped>

.showword {
  text-align: center;
  writing-mode: vertical-rl;
  width: 50%;
}

.showSentence {
  margin: 0 0 18px 0;
}

.button {
  text-align: center
}

</style>