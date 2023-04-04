<template>
  <div class="wrapper">
    <div class="heading">
      <h1 class="logo">SpyOT</h1>
    </div>
    <div class="body">
      <div class="left-container">
        <h2>Download the SpyOT Software to get Started</h2>
        <div class="download-container">
          <button id="download" @click="attemptDownload">
            DOWNLOAD SPYoT NOW
            <span class="material-icons-outlined">file_download</span>
          </button>
        </div>
      </div>

      <div class="right-container">
        <div class="sign-in-container login">
          <form>
            <h2>Log In</h2>
            <div class="input-container">
              <label for="email">Email</label>
              <span class="material-icons-outlined">mail</span>
              <input
                type="text"
                id="email"
                name="email"
                autocomplete="off"
                v-model="emailValue"
              />
            </div>
            <div class="input-container">
              <label for="password">Password</label>
              <span class="material-icons-outlined">lock</span>
              <input
                type="password"
                id="password"
                name="password"
                autocomplete="off"
                v-model="passwordValue"
              />
            </div>
            <div class="remember">
              <div class="remrow">
                <label for="checkbox">Remember Me</label>
                <input type="checkbox" v-model="checked" id="checkbox" />
              </div>
              <div class="forgot-password">
                <button id="download" @click="forgotPassword">
                  Forgot Password?
                </button>
              </div>
            </div>
            <div class="login">
              <button @click="attemptLogin">Log In</button>
            </div>
            <div class="login-register">
              <p>Don't have an account?</p>
              <button @click="registerAccountLink">Register</button>
            </div>
          </form>
        </div>

        <div class="sign-in-container register">
          <form>
            <h2>Register</h2>
            <div class="input-container">
              <label for="username">Username</label>
              <span class="material-icons-outlined">person</span>
              <input
                type="text"
                id="username"
                name="username"
                autocomplete="off"
                v-model="usernameValue"
              />
            </div>
            <div class="input-container">
              <label for="email">Email</label>
              <span class="material-icons-outlined">mail</span>
              <input
                type="text"
                id="email"
                name="email"
                autocomplete="off"
                v-model="emailValue"
              />
            </div>
            <div class="input-container">
              <label for="password">Password</label>
              <span class="material-icons-outlined">lock</span>
              <input
                type="password"
                id="password"
                name="password"
                autocomplete="off"
                v-model="passwordValue"
              />
            </div>
            <div class="remember">
              <div class="remrow">
                <label for="agreeCheck"
                  >I agree to the terms and conditions</label
                >
                <input type="checkbox" v-model="checked" id="agreeCheck" />
              </div>
            </div>
            <div class="login">
              <button @click="attemptSignUp">Sign Up</button>
            </div>
            <div class="login-register">
              <p>Already have an account?</p>
              <button @click="loginAccountLink">Login</button>
            </div>
          </form>
        </div>
      </div>
      </div>
    </div>
    <div class="footer">
      <div class="footer-container">
        <h2>Team Website</h2>
        <button>https://spyot.github.io/SpyOt/</button>
      </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      emailValue: "",
      usernameValue: "",
      passwordValue: "",
      checked: false,
    };
  },
  methods: {
    attemptDownload() {
      console.log("Download Button Clicked");
    },
    forgotPassword() {
      console.log("Forgot Password Clicked");
    },
    attemptLogin() {
      console.log("Login Button Clicked");
      this.$router.push("/dashboard");
    },
    attemptSignUp() {
      console.log("Signup Button Clicked");
    },
    registerAccountLink() {
      console.log("Register Account Clicked");
    },
    loginAccountLink() {
      console.log("Login Account Clicked");
    },
    // checkPrint() {
    //     if (this.checked) {
    //         console.log("Checkbutton = True");
    //     }
    // }
  },
};
</script>

<style scoped>
.wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: .1fr 1fr .1fr;
  grid-column-gap: px;
  grid-row-gap: 0px;
}

/* .header {
  height: 30px;
} */

.body {
  grid-area: 2 / 1 / 3 / 4;

  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 1fr;
}
.footer {
  grid-area: 3 / 1 / 4 / 4;
}
.footer-container{
  background-color: black;
  display: flex;
  flex-direction: row;
  padding: 1em;
}
.footer-container button {
  width: 30%;
  background-color: transparent;
  color: red;
  font-size: 2rem;
  /* padding-bottom: 3em; */
}

.left-container {
  grid-area: 1 / 1 / 2 / 2;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
}

.left-container h2 {
  color: #1DD75BFF;
  font-size: 3rem;
  padding: 1rem;
}

.left-container .download-container {
  padding: 1rem;
}
.left-container .download-container button{
  font-size: 2em;
  color: var(--primary-color);
  background: transparent;
  border-color: var(--primary-color);
  border-radius: 5px;
}
.right-container {
  grid-area: 1 / 2 / 2 / 3;
    margin: 1em;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.right-container .sign-in-container {
  width: 100%;
  padding: 40px;
}
.right-container .sign-in-container.login {
  /* display: none; */
}
.right-container .sign-in-container.register {
  position: absolute;
  transform: translateX(400px);
  display: none;
}
.sign-in-container h2 {
  font-size: 2em;
  color: var(--primary-color);
  text-align: center;
  border-bottom: 2px solid #dee1e6ff;
}
.input-container {
  position: relative;
  width: 100%;
  height: 50px;
  margin: 30px 0;
  border-bottom: 2px solid #dee1e6ff;
}
.input-container label {
  position: absolute;
  /* top:50%;
  left: 5px; */
  transform: translateY(-50%);
  font-size: 1em;
  color: white;
  font-weight: 500;
  pointer-events: none;
  transition: 0.5s;
}

/* .input-container input:focus~label,
.input-container input:valid~label {
  top: -5px;

} */
.input-container input {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  font-size: 1em;
  color: var(--label-color);
  font-weight: 600;
  margin-left: 15px;
  padding: 0 35px 0 5px;
}
.heading {
  grid-area: 1 / 1 / 2 / 4;
  background-color: var(--secondary-color);
}
.heading .logo {
  text-align: left;
  margin-left: 2em;
  font-size: 3em;
  color: black;
}
.input-container span {
  position: absolute;
  font-size: 1.2em;
  color: var(--label-color);
  line-height: 50px;
}

.remember {
  font-size: 0.9em;
  color: var(--label-color);
  font-weight: 500;
  margin: -15px 0 15px;
  display: flex;
  justify-content: space-between;
}

.remember input {
  accent-color: var(--primary-color);
  margin-left: 5px;
}
.forgot-password button {
  color: red;
  background: none;
  border: none;
  margin-left: -6px;
}
.forgot-password button:hover {
  text-decoration: underline;
}

.login {
  align-self: center;
  place-self: center;
}
.login button {
  font-size: 1.2em;
  font-weight: 500;
  width: 80%;
  height: 35px;
  color: var(--primary-color);
  background-color: transparent;
  border-color: var(--primary-color);

}

.login-register {
  font-size: 1em;
  color: var(--primary-color);
  text-align: center;
  font-weight: 500;
  margin: 15px 0 10px;
  display: flex;
}
.login-register p {
  align-items: center;
  align-content: center;
  justify-content: center;
  width:100%;
}
.login-register button {
  width:100%;
  font-size: 1.5em;
  font-weight: 700;
  color: var(--primary-color);
  background-color: transparent;
  border: none;
}
</style>
