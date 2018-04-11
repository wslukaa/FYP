<template>

  <div>
    <h1>Logistic Regression Trend Predictor</h1>
    <form action="/predict" method="post" enctype="multipart/form-data">
     <input type="file" name="csv" value="Upload">
     <input type="submit" value="Predict">
    </form>
    <p>
      {{ label }}
    </p>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      label: ""
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      const {data} = await api.fetchDemo()
      this.label = data;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
