<template>
  <div class="Home">
    <b-container fluid>
      <b-row>
        <b-col align-self="center">
          <h1>CS 590 Neural Network Adversarial Attack Demo</h1>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-img thumbnail fluid :src=originalURL alt="Image 1"></b-img>
          <h3>Original Picture</h3>
          <h3>{{originalResult}}</h3>
          <h3>Confidence: {{originalConfidence}}%</h3>
        </b-col>
        <b-col>
          <b-img thumbnail fluid :src=noiseURL alt="Image 2"></b-img>
          <h3>Gradient Ascent</h3>
        </b-col>
        <b-col>
          <b-img thumbnail fluid :src=noise10xURL alt="Image 2"></b-img>
          <h3>Gradient Ascent 10x</h3>
        </b-col>
        <b-col>
          <b-img thumbnail fluid :src=transformedURL alt="Image 3"></b-img>
          <h3>Transformed Picture</h3>
          <h3>{{transformedResult}}</h3>
          <h3>Confidence: {{transformedConfidence}}%</h3>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="4" align-self="center">
        </b-col>
        <b-col cols="4" align-self="center">
          <b-form-select v-model="selected" :options="options"></b-form-select>
        </b-col>
        <b-col cols="4" align-self="center">
        </b-col>
      </b-row>
      <b-row>
        <b-col align-self="center">
          <b-button class="btn-primary" @click="upload">Submit a Picture</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
  import axios from 'axios'

  axios.defaults.baseURL = 'http://127.0.0.1:5000'

  export default {
    name: 'hello',
    methods: {
      upload () {
        let input = document.createElement('input')
        input.type = 'file'

        let file = ''
        input.onchange = async e => {
          file = e.target.files[0]
          let formData = new FormData()
          formData.append('file', file)
          try {
            let response = await axios.post('upload', formData, {
              headers: {'Content-Type': 'multipart/form-data'}
            })
            let originalURL = response.data.url
            response = await axios.post('run',
              {
                originalURL: response.data.url,
                category: this.selected
              }, {
                headers: {'Content-Type': 'application/json'}
              })
            this.originalURL = 'http://127.0.0.1:5000/' + originalURL
            this.transformedURL = 'http://127.0.0.1:5000/' + response.data.transformedURL
            this.noiseURL = 'http://127.0.0.1:5000/' + response.data.noiseURL
            this.noise10xURL = 'http://127.0.0.1:5000/' + response.data.noise10xURL
            this.originalResult = response.data.originalResult
            this.transformedResult = response.data.transformedResult
            this.originalConfidence = response.data.originalConfidence
            this.transformedConfidence = response.data.transformedConfidence
          } catch (e) {
            console.log(e)
          }
        }
        input.click()
      }
    },
    data () {
      return {
        selected: null,
        options: [
          {value: null, text: 'Transform to...'},
          {value: 607, text: 'jack-o\'-lantern'},
          {value: 886, text: 'Vending Machine'},
          {value: 248, text: 'Husky'},
          {value: 625, text: 'Life Boat'},
          {value: 624, text: 'Library'},
          {value: 605, text: 'iPod'},
          {value: 413, text: 'Assault Rifle'},
          {value: 999, text: 'Toilet Tissue'}
        ],
        originalURL: '',
        transformedURL: '',
        noiseURL: '',
        noise10xURL: '',
        originalResult: '',
        transformedResult: '',
        originalConfidence: '',
        transformedConfidence: ''
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  img {
    height: 300px !important;
    width: 300px !important;
    margin-top: 30px !important;
    margin-bottom: 20px !important;
  }

  .btn-primary {
    margin-top: 20px !important;
  }
</style>
