import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase, ref, push } from "firebase/database";
const firebaseConfig = {
  apiKey: "AIzaSyDoBEoypPjsbvU-n3-b_30Xw_P2Z6x3rAU",
  authDomain: "spyot-56f6e.firebaseapp.com",
  databaseURL: "https://spyot-56f6e-default-rtdb.firebaseio.com",
  projectId: "spyot-56f6e",
  storageBucket: "spyot-56f6e.appspot.com",
  messagingSenderId: "869272684117",
  appId: "1:869272684117:web:4d4051a4b506f2f2eef6dc",
  measurementId: "G-YW1WX5YERW"
};


// Initialize the Firebase App
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const auth = getAuth();
auth.onAuthStateChanged(user => {
  if (user) {
    console.log('User is logged in!');
  } else {
    console.log('User is not logged in!');
  }
});
export {db}

// Create Vue.js app instance and mount it to the DOM
const vueApp = createApp(App);
vueApp.use(router)
vueApp.mount('#app')
