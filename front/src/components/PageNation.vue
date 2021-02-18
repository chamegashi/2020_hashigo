<template>
  <div>

    <div class="button">
      <b-button v-if="show_page <= 0" disable>前へ</b-button>
      <b-button v-else v-on:click="changeShowPage(show_page-1)" variant="primary">前へ</b-button>

     <b-button v-if="max_page <= show_page" disable>次へ</b-button>
     <b-button v-else v-on:click="changeShowPage(show_page+1)" variant="primary">次へ</b-button>

     <b-button v-if="max_page <= show_page" disable>Enter で次へ</b-button>
     <b-button v-else @keyup.enter="changeShowPage(show_page+1)" variant="primary">Enter で次へ</b-button>

     <b-button v-if="show_page != 0" v-on:click="changeShowPage(0)" variant="primary">Top へ戻る</b-button>

    </div>

    <div>
      <div v-for="(show_word, index) in show_words" :key="index" class="box">
        <div v-for="(word, index) in show_word" :key="index" class="showword">
          <p>{{word}}</p>
        </div>
      </div>
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
    show_page: 0,
    max_page: 0,
    stack_words: []
  }),
  watch: {
    words: {
      handler: function () {
        this.makeShowWords()
      }
    }
  },
  methods: {
    makeShowWords () {
      this.show_page = 0
      let limit = 11
      var i = 0
      var max = 0
      var result_array = []
      var input_words = []
      this.words.forEach(function(e) {
        if(i > limit){
          i = 0
          result_array.push(input_words)
          input_words = []
          max = max + 1
        }
        input_words.push(e)
        i = i + 1
      });
      result_array.push(input_words)
      max = max + 1

      this.max_page = Math.floor(max / 3)
      this.stack_words = result_array
      this.changeShowPage(this.show_page)
    },
    changeShowPage (page_num) {
      this.show_words = []
      this.show_page = page_num
      if(page_num*3 < this.stack_words.length){
        this.show_words.push(this.stack_words[page_num*3])
      }
      if(page_num*3+1 < this.stack_words.length){
        this.show_words.push(this.stack_words[page_num*3+1])
      }
      if(page_num*3+2 < this.stack_words.length){
        this.show_words.push(this.stack_words[page_num*3+2])
      }
    }
  }
}
</script>

<style scoped>

.showword {
  text-align: center;
  width: 480px;
}

.button {
  text-align: center
}

.box{
  float: left;
}

</style>