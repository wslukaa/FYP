import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000/',
  // set global headers
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Access-Control-Allow-Origin': '*',
  },
});


export default {
  fetchDemo() {
    return instance.get(`testing/`)

    //return instance.get(`/predict`)
  },
}
