<template>
  <div>

    <h1 style="text-align: center">はしごレイアウトテスト</h1>
    <h3 style="text-align: center">文字幅検索</h3>

    <p style="text-align: center">max length<input id="length" v-model="maxLength"></p>

    <div class="button">
      <b-button v-on:click="goInput()" variant="primary">文字入力に戻る</b-button>
    </div>

    <div class="button">
      <b-button v-on:click="moveToButtom()" @keyup.up="changeSpeed(1)" @keyup.down="changeSpeed(-1)" variant="primary">下にスクロール</b-button>
      <p>下にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div id="LineWidthBox">
      <div v-for="(wordArray, index) in showWords" :key="index" class="show-sentence">
        <div v-for="(word, index) in wordArray" :key="index" class="showword">
          {{word}}
        </div>
      </div>
    </div>

    <div class="button">
      <b-button v-on:click="moveToTOP()" variant="primary">TOP に戻る</b-button>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    words: Array
  },
  data: () => ({
    is_loading: false,
    input_text: '',
    step: 2,
    showWords: [],
    maxLength: 20
  }),
  created () {
    this.sendSentence();
  },
  watch: {
    maxLength: function(){
      this.showWords = []
      this.makeWidthTop()
    }
  },
  methods: {
    goInput () {
      this.$router.push({name: 'input'})
    },
    moveToButtom () {
      var e = document.getElementById('LineWidthBox')
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
    sendSentence () {
        const path = 'http://127.0.0.1:5000/make_divided'
        const params = new URLSearchParams()

        params.append('sentence', this.$route.params.sentence)
        axios.post(path, params).then(res => {
          this.words = res.data.result
          this.makeWidthTop();
        }).catch(e => {
          console.log(e)
        })
    },
    
    makeWidthTop () {
      let nowLength = 0
      let addArray = []

      this.words.forEach(wordSet => {
        if(nowLength + wordSet.word.length < this.maxLength){
          nowLength = nowLength + wordSet.word.length;
          addArray.push(wordSet);
          return;
        }

        let max_divided = 0;

        addArray.forEach(childWordSet => {
          if(childWordSet.divided > max_divided){
            max_divided = childWordSet.divided;
          }
        })

        let showArray = []
        let nextArray = []
        let flag = false

        const reverseArray = addArray.reverse()

        reverseArray.forEach(childWordSet => {
          if(flag){
            showArray.push(childWordSet.word);
            return;
          }

          if(childWordSet.divided < max_divided){
            nextArray.push(childWordSet)
          }else{
            showArray.push(childWordSet.word);
            flag = true;            
          }
        })

        showArray = showArray.reverse();
        nextArray = nextArray.reverse();

        this.showWords.push(showArray);

        addArray = nextArray
        addArray.push(wordSet)
        nowLength = 0

        addArray.forEach(childWordSet => {
          nowLength = nowLength + childWordSet.word.length;
        })
      });
      
      let showArray = []

      addArray.forEach(wordSet => {
        showArray.push(wordSet.word)
      })

      this.showWords.push(showArray)
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
  padding: 7.5px;
}

.showword {
  display: inline-block;
  /* padding: 0 3px 0 3px; */
}

.button {
  text-align: center
}

</style>