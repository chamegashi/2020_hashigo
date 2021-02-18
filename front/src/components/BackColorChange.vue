<template>
  <div>

    <div class="button">
      <b-button v-on:click="moveToButtom()" @keyup.up="changeSpeed(1)" @keyup.down="changeSpeed(-1)" variant="primary">下にスクロール</b-button>
      <p>下にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div id="vibunderBox" class="vibunderBox">
      <div v-for="(sentence, index) in vib_words" :key="index" class="show-sentence">
        <div v-for="(word, word_index) in sentence" :key="word_index" class="showword">
          <p v-if="word_index % 2 === 0" class="color0">{{word}}</p>
          <p v-else-if="word_index % 2 === 1" class="color1">{{word}}</p>
        </div>
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
    vib_words: Array
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
      var e = document.getElementById('vibunderBox')
      const height = parseInt(e.offsetHeight) - 450
      const interval = 25
      console.log(this.vib_words);

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

.show-sentence {
  text-align: center;
}

.showword {
  display: inline-block;
  /* padding: 0 3px 0 3px; */
}

.color0 {
  background: #eeffee;
}

.color1 {
  background: #ffeeee;
}

.button {
  text-align: center
}

</style>