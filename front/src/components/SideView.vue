<template>
  <div>

    <div class="button">
      <b-button v-on:click="moveToRight()" @keyup.right="changeSpeed(1)" @keyup.left="changeSpeed(-1)" variant="primary">右にスクロール</b-button>
      <p>右にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div class="wrap">
      <div v-for="(show_word, index) in show_words" :key="index" class="box">
        <div v-for="(word, index) in show_word" :key="index" class="showword">
          <p>{{word}}</p>
        </div>
      </div>
      <b-button v-on:click="moveToTop()" variant="primary">Top にスクロール</b-button>
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
    show_words: [],
    step: 2
  }),
  watch: {
    words: {
      handler: function () {
        this.makeShowWords()
      }
    }
  },
  methods: {
    goInput () {
      this.$router.push({name: 'input'})
    },
    makeShowWords () {
      let limit = 11
      var i = 0
      var result_array = []
      var input_words = []
      this.words.forEach(function(e) {
        if(i > limit){
          i = 0
          result_array.push(input_words)
          input_words = []
        }        
        input_words.push(e)
        i = i + 1
      });
      result_array.push(input_words)
      this.show_words = result_array
    },
    moveToRight () {
      const width = 480 * this.show_words.length
      const interval = 25

      const timer = setInterval(() => {
        window.scrollBy(this.step, 0)
        if(window.scrollX >= width) {
          clearInterval(timer)
        }
      }
      , interval)
    },
    moveToTop () {
      window.scrollTo({
        left: 0,
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

.wrap {
  width: 20000px;
}

.showword {
  text-align: center;
  width: 480px;
}

.box{
  float: left;
}

</style>