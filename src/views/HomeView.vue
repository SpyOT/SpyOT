<template>
  <div class="wrapper">
    <div class="heading">
      <h1 class="logo">SpyOT</h1>
    </div>
    <div class="body">
      <div class="left-container">
        <div class="left-side">
          <h2>Download the SpyOT Software to get Started</h2>
          <div class="download-container">
            <button id="download" @click="attemptDownload">
              DOWNLOAD SPYoT NOW
              <span class="material-icons-outlined">file_download</span>
            </button>
          </div>
        </div>
      </div>

      <div class="right-container">
        <div class="right-side">
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
      <div class="foot">
        <h2>Team Website</h2>
        <button>https://spyot.github.io/SpyOt/</button>
      </div>

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
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* .header {
  height: 30px;
} */

.body {
  flex: 1;
  width: 100%;
  overflow: auto;
}
.footer {
  justify-content: space-between;
  width: 100%;
  padding-top: 2em;
  height: 30px;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}
.foot button {
  width: 30%;
  background-color: transparent;
  color: red;
  font-size: 2em;
  /* padding-bottom: 3em; */
}
.foot{
  background-color: black;
  display: flex;
  flex-direction: row;
  padding: 1em;
  
}
.left-container {
  /* grid-column: 1; */
  width: 50%;
  float:left;
}

.left-side h2 {
  margin-top: 139px; 
  margin-left: 132px; 
  width: 564px; 
  font-size: 52px; 
  line-height: 74px; 
  color: #1DD75BFF; 
}

.download-container {
  margin-top: 50px;
  margin-left: 20em;
}
.download-container button{
  font-size: 2em;
  color: var(--primary-color);
  background: transparent;
  border-color: var(--primary-color);
  border-radius: 5px;
}
.right-container {
  /* grid-column: 1; */
  width: 500px;
  float: right;
  margin-right: 40px;
  margin-top: 5em;
}
.right-side {
  height: 440px;
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.right-side .sign-in-container {
  width: 100%;
  padding: 40px;
}
.right-side .sign-in-container.login {
  /* display: none; */
}
.right-side .sign-in-container.register {
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
  background-color: var(--secondary-color);
}
.heading .logo {
  text-align: left;
  margin-left: 2em;
  font-size: 3em;
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

.login button {
  font-size: 1.2em;
  font-weight: 500;
  width: 100%;
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
  /* justify-content: space-between; */
}

.login-register button {
  width: 200px;
  font-size: 1.5em;
  font-weight: 700;
  color: var(--primary-color);
  background-color: transparent;
  border: none;
  margin-left: -45px;
}
</style>
