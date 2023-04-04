import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
const firebaseConfig = {
  apiKey: "AIzaSyDoBEoypPjsbvU-n3-b_30Xw_P2Z6x3rAU",
  authDomain: "spyot-56f6e.firebaseapp.com",
  projectId: "spyot-56f6e",
  storageBucket: "spyot-56f6e.appspot.com",
  messagingSenderId: "869272684117",
  appId: "1:869272684117:web:4d4051a4b506f2f2eef6dc",
  measurementId: "G-YW1WX5YERW"
};

initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

const app = createApp(App)

app.use(router)

app.mount('#app')
