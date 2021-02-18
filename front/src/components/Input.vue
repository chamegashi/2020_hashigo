<template>
  <div>
    <h1 style="text-align: center">読みやすさ向上システム</h1>
    <h3 style="text-align: center">文字入力</h3>
    <b-form-textarea
      v-model="input_text"
      placeholder="表示させる文章を入力"
      rows="9"
      max-rows="20"
    ></b-form-textarea>
    <div class="select_block">
      <div class="old_block">
        <div style="text-align: center">
          <!-- <p>最大文節数(default: 3) <input v-model="max_sentence"></p>
          <p>文節の切れやすさ(default: 2) <input v-model="devide_num"></p> -->
          <p>最大文字数(default: 10) <input v-model="max_words"></p>
          <p>tfIdf するかどうか <input v-model="tf_idf_flag"></p>
        </div>
      </div>
      <div clsss = "mitani_block">
        <div style="text-align: center">
          <b-button v-on:click="goTreeShow()" variant="primary">レイアウトに変換</b-button>
        </div>
        <div style="text-align: center">
          <b-button v-on:click="goWidthSentence()" variant="primary">最適な文字幅を調整する</b-button>
        </div>
        <div style="text-align: center">
          <b-button v-on:click="goSearchDistance()" variant="primary">通常レイアウト</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    input_text: '',
    max_sentence: 3,
    devide_num: 2,
    max_words: 10,
    tf_idf_flag: 0,
  }),
  methods: {
    goTreeShow () {
      this.$router.push({name: 'show', params: {sentence: this.input_text, max_words: this.max_words, ver: "mitani", tf_idf_flag: this.tf_idf_flag}})
    },
    goSearchDistance () {
      this.$router.push({name: 'search', params: {words: this.input_text, max_words: this.max_words}})
    },
    goWidthSentence () {
      this.$router.push({name: 'reserch', params: {sentence: this.input_text}})
    }
  }
}
</script>

<style scoped>

.old_block{
  padding: 5px 5px 5px 5px;
}
.mitani_block{
  padding: 5px 5px 5px 5px;
}

</style>