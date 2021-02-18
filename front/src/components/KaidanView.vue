<template>
  <div>

    <div class="button">
      <b-button v-on:click="moveToButtom()" @keyup.up="changeSpeed(1)" @keyup.down="changeSpeed(-1)" variant="primary">下にスクロール</b-button>
      <p>下にスクロールするスピード(default: 2)</p>
      <input v-model="step">
    </div>

    <div id="kaidanUnderBox" class="wrap">
      <div v-for="(word, index) in words" :key="index" v-bind:style="{padding:('0px 0px 0px ' + (index*35).toString() + 'px')}">
        <p>{{word}}</p>
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
  methods: {
    goInput () {
      this.$router.push({name: 'input'})
    },
    moveToButtom () {
      var e = document.getElementById('kaidanUnderBox')
      console.log(e)
      console.log(e.offsetHeight)
      const height = parseInt(e.offsetHeight) - 450
      const interval = 25

      console.log(window.scrollY)
      console.log(height)

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

.wrap {
  width: 20000px;
}

.showword {
  text-align: left;
}

.button {
  text-align: center
}

</style>