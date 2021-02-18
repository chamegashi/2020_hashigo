<template>
  <div>

    <div class="button">
      <b-button v-on:click="moveToButtom()" @keyup.up="changeSpeed(1)" @keyup.down="changeSpeed(-1)" variant="primary">下にスクロール</b-button>
      <p>下にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div id="colorUnderBox" class="ColorUnderBox">
      <div v-for="(sentence, index) in words" :key="index" class="show-sentence">
          <span v-if="(index % 4) === 0" class="color3 showword">{{sentence}}</span>
          <span v-if="(index % 4) === 1" class="color2 showword">{{sentence}}</span>
          <span v-if="(index % 4) === 2" class="color1 showword">{{sentence}}</span>
          <span v-if="(index % 4) === 3" class="color0 showword">{{sentence}}</span>
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
      var e = document.getElementById('colorUnderBox')
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

.show-sentence {
  text-align: center;
}

.showword {
  display: inline-block;
  padding: 7.5px;
}

.color0 {
  display: inline-block;
  animation: move0 1s infinite;
}

.color1 {
  display: inline-block;
  animation: move1 1s infinite;
}

.color2 {
  display: inline-block;
  animation: move2 1s infinite;
}

.color3 {
  display: inline-block;
  animation: move3 1s infinite;
}

@keyframes move0 {
    0% {color: #000000;}
    100%{color:#ffffff;}
}

@keyframes move1 {
    0% {color: #444444;}
    75% {color: #ffffff;}
    76% {color: #000000;}
    100%{color:#444444;}
}

@keyframes move2 {
    0% {color: #888888;}
    50% {color: #ffffff;}
    51% {color: #000000;}
    100%{color:#888888;}
}

@keyframes move3 {
    0% {color: #bbbbbb;}
    25% {color: #ffffff;}
    26% {color: #000000;}
    100%{color:#bbbbbb;}
}

.button {
  text-align: center
}

</style>