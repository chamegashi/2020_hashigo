<template>
  <div>

    <div class="button">
      <b-button v-on:click="moveToButtom()" @keyup.up="changeSpeed(1)" @keyup.down="changeSpeed(-1)" variant="primary">下にスクロール</b-button>
      <p>下にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div id="tfidfUnderBox" class="tfidfUnderBox">
      <div v-for="(sentence, index) in tf_idf_words" :key="index" class="show-sentence">
        <div v-for="(word_data, word_index) in sentence" :key="word_index" class="showword">
          <p v-if="word_data.accent" class="highlight">{{word_data.word}}</p>
          <p v-else class="lowlight">{{word_data.word}}</p>
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
    tf_idf_words: Array
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
      var e = document.getElementById('tfidfUnderBox')
      const height = parseInt(e.offsetHeight) - 450
      const interval = 25
      console.log(this.accent_words);

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

.lowlight {
  color:#AAAAAA;
}

.highlight {
  color:#000000;
}

.button {
  text-align: center
}

</style>