<template>
  <div>
    <h1 style="text-align: center">読みやすさ向上システム</h1>
    <h3 style="text-align: center">文字表示</h3>

    <div class="button">
      <b-button v-on:click="goInput()" variant="primary">文字入力に戻る</b-button>
    </div>

    <div>
      <div class="loading" v-if="is_loading">
        Loading...
      </div>
    </div>

    <div v-if="!is_loading">
      <b-tabs content-class="mt-3" fill>
        <b-tab title="下スクロール" active><UnderView :words="words"></UnderView></b-tab>
        <!-- <b-tab title="右スクロール"><SideView :words="words"></SideView></b-tab> -->
        <!-- <b-tab title="ページ切り替え"><PageNation :words="words"></PageNation></b-tab> -->
        <!-- <b-tab title="縦読み"><VerticalView :words="words"></VerticalView></b-tab> -->
        <b-tab title="階段"><KaidanView :words="words"></KaidanView></b-tab>
        <!-- <b-tab title="振動"><VibrationView :vib_words="vib_words"></VibrationView></b-tab> -->
        <!-- <b-tab title="色の変更"><ColorChangeView :words="words"></ColorChangeView></b-tab> -->
        <!-- <b-tab title="ニュース"><NewsUnder :words="words"></NewsUnder></b-tab>         -->
        <!-- <b-tab title="アクセント"><AccentView :accent_words="accent_words"></AccentView></b-tab> -->
        <!-- <b-tab title="背景色"><BackColorChange :vib_words="vib_words"></BackColorChange></b-tab> -->
        <b-tab title="tf_idt"><TfIdfView :tf_idf_words="tf_idf_words"></TfIdfView></b-tab>
        <!-- <b-tab title="自動行"><LineWidthView :tf_idf_words="tf_idf_words"></LineWidthView></b-tab> -->
      </b-tabs>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import UnderView from '@/components/UnderView.vue'
// import SideView from '@/components/SideView.vue'
// import PageNation from '@/components/PageNation.vue'
// import VerticalView from '@/components/VerticalView.vue'
import KaidanView from '@/components/KaidanView.vue'
// import VibrationView from '@/components/VibrationView.vue'
// import ColorChangeView from '@/components/ColorChangeView.vue'
// import NewsUnder from '@/components/NewsUnder.vue'
// import AccentView from '@/components/AccentView.vue'
// import BackColorChange from '@/components/BackColorChange.vue'
import TfIdfView from '@/components/TfIdfView.vue'
// import LineWidthView from '@/components/LineWidthView.vue'

export default {
  components: {
    UnderView,
    // SideView,
    // PageNation,
    // VerticalView,
    KaidanView,
    // VibrationView,
    // ColorChangeView,
    // NewsUnder,
    // AccentView,
    // BackColorChange,
    TfIdfView,
    // LineWidthView
  },
  data: () => ({
    is_loading: false,
    input_text: '',
    words: Array,
    vib_words: Array,
    accent_words: Array,
    tf_idf_words: Array,
    width_words: Array,
  }),
  created () {
    this.sendSentence()
  },
  methods: {
    sendSentence () {
      {
        const path = 'http://127.0.0.1:8080/make_tree_dev'
        // const path = 'https://7553e0e9f723.ngrok.io/make_tree_dev'
        const params = new URLSearchParams()

        params.append('max_length', this.$route.params.max_words)
        params.append('sentence', this.$route.params.sentence)
        params.append('tf_idf', this.$route.params.tf_idf_flag)
        axios.post(path, params).then(res => {
          this.words = res.data.result
          this.vib_words = res.data.vib_result
          this.accent_words = res.data.accent_result
          this.tf_idf_words = res.data.tf_idf_result
          this.width_words = res.data.width_array
          this.is_loading = false
        }).catch(e => {
          console.log(e)
        })
      }
    },
    goInput () {
      this.$router.push({name: 'input'})
    }
  }
}
</script>

<style scoped>

.showword {
  text-align: center;
}

.button {
  text-align: center
}

</style>