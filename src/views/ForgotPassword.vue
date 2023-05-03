<template>
    <div class="wrapper">
      <h1>Reset Password</h1>
      <div class="input-container">
        <label for="email">Email</label>
        <span class="material-icons-outlined">mail</span>
        <input
          type="email"
          id="email"
          name="email"
          autocomplete="off"
          v-model="emailValue"
        />
      </div>
      <button @click="sendResetEmail">Send Reset Email</button>
    </div>
  </template>
  <script>
  import { getAuth, sendPasswordResetEmail } from "firebase/auth";
  
  export default {
    data() {
      return {
        emailValue: "",
      };
    },
    methods: {
      sendResetEmail() {
        const auth = getAuth();
        const email = this.emailValue;
        sendPasswordResetEmail(auth, email)
        .then(() => {
          console.log("Password reset email sent successfully");
        })
        .catch((error) => {
          console.error("Error sending password reset email: ", error);
        });
      },
    },
  };
  </script>
  <style scoped>
  h1 {
    color: var(--color-text);
  }
  </style>