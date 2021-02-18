<template>
  <div>
    <h1 style="text-align: center">読みやすさ向上システム</h1>
    <h3 style="text-align: center">文字幅調整</h3>

    <div class="button">
      <b-button v-on:click="goInput()" variant="primary">文字入力に戻る</b-button>
    </div>

    <div class="">
      <div v-for="(word, index) in showWords" :key="index" class="show-sentence">
        {{word}}
      </div>
    </div>
  </div>
</template>

<script>
export default {  
  props: {
    words: String,
    max_words: Number
  },
  data: () => ({
    showWords: []
  }),
  created() {
    this.makeLayout()
  },
  methods: {
    makeLayout () {
      let word = this.$route.params.words;
      const max_lenght = this.$route.params.max_words

      word.replace(' ', '');
      word.replace('  ', '');
      word.replace('\n', '');

      while(word){
        if(word.lenght < max_lenght){
          this.showWords.push(word);
          break;
        }

        const push_word = word.slice(0, max_lenght);
        this.showWords.push(push_word);
        word = word.slice(max_lenght);
      }
    },
    goInput () {
      this.$router.push({name: 'input'})
    }
  }
}
</script>

<style scoped>

.show-sentence {
  text-align: center;
  padding: 7.5px;
}

.showword {
  display: inline-block;
  padding: 0 3px 0 3px;
}

.showword {
  text-align: center;
}

.button {
  text-align: center
}

.sentences {
  text-align: center
}

</style>