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
        <div class="sign-in-container login" v-if="register === false">
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
            <div class="forgot-row">
                <button id="forgotPass" @click="forgotPassword" type="button">
                  Forgot Password?
                </button>
            </div>
            <div class="alt-login-row">
                <!-- <p1>Sign in with:v-on
                  <img src="../assets/google_logo.png" alt="google" :click="google-trigger">
                  <img src="../assets/github_logo.png" alt="github" v-on:click="github-trigger">
                </p1> -->
                
            </div>
            <div class="login">
              <p1 v-if="errMsg">{{ errMsg }}</p1>
              <button @click="attemptLogin" type="button">Log In</button>
            </div>
            <div class="login-register">
              <p>Don't have an account?</p>
              <button @click="registerAccountLink" type="button">Register</button>
            </div>
          </form>
        </div>

        <div class="sign-in-container register" v-if="register">
          <form>
            <h2>Register</h2>
            <!-- <div class="input-container">
              <label for="username">Username</label>
              <span class="material-icons-outlined">person</span>
              <input
                type="text"
                id="username"
                name="username"
                autocomplete="off"
                v-model="usernameValue"
              />
            </div> -->
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
            <div class="login">
              <button @click="attemptSignUp" type="button">Sign Up</button>
            </div>
            <div class="login-register">
              <p>Already have an account?</p>
              <button @click="registerAccountLink" type="button">Login</button>
            </div>
          </form>
        </div>
      </div>
      </div>
    </div>
    <!-- <div class="footer">
      <div class="footer-container">
        <h2>Team Website</h2>
        <button>https://spyot.github.io/SpyOt/</button>
      </div>
  </div> -->
</template>

<script>
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword} from "firebase/auth";
export default {
  data() {
    return {
      emailValue: "",
      passwordValue: "",
      checked: false,
      register: false,
      errMsg: ""
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
      signInWithEmailAndPassword(getAuth(), this.emailValue, this.passwordValue)
        .then((data) => {
          console.log("Login Successful!");
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          console.log(error.code);
          switch (error.code) {
            case "auth/invalid-email":
              this.errMsg = "Invalid email";
              break;
            case "auth/user-not-found":
              this.errMsg = "Account not found";
              break;
            case "auth/wrong-password":
              this.errMsg = "Invalid password";
              break;
            default:
              this.errMsg = "Email or password incorrect"
              break;
          }
          // alert(error.message);
        });
    },
    attemptSignUp() {
      createUserWithEmailAndPassword(getAuth(), this.emailValue, this.passwordValue)
        .then((data) => {
          console.log("Sign Up Successful!");
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          console.log(error.code);
          alert(error.code);
        });
    },
    registerAccountLink() {
      this.register = !this.register;
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

p1 {
  font-size: 1.5em;
  color: red;
}

img  {
  height: 35px;
  width: 35px;
  margin-left: 1em;
}
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
  /* grid-template-columns: repeat(2, 1fr); */
  grid-template-columns: 70% 30%;
  grid-template-rows: 1fr;
}
.footer {
  margin-top: 7em;
  width: 100%;
  bottom: 0;
  /* grid-area: 3 / 1 / 4 / 4; */
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
  /* grid-area: 1 / 1 / 2 / 2; */

  display: flex;
  flex-direction: column;
  align-items: center;
  align-content: center;
}

.left-container h2 {
  color: var(--primary-color);
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
/* .right-container .sign-in-container.login {
  display: none;
}
.right-container .sign-in-container.register {
  display: none;
} */
.sign-in-container h2 {
  font-size: 2em;
  color:white;
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
  color: white;
  font-weight: 600;
  margin-left: 15px;
  padding: 0 35px 0 5px;
}
.heading {
  grid-area: 1 / 1 / 2 / 4;
  /* background-color: var(--secondary-color); */
}
.heading .logo {
  text-align: left;
  margin-left: 2em;
  font-size: 3em;
  color: white;
}
.input-container span {
  position: absolute;
  font-size: 1.2em;
  color: var(--label-color);
  line-height: 50px;
}

.alt-login-row {
  margin: none;
  padding: none;
}

.login .forgot-row {
  margin-top: -1em;
}

.login .forgot-row button {
  font-size: .8rem;
  margin-left: -.5em;
  margin-top: -2em;
  /* font-weight: 660; */
  text-align: left;
  color: var(--label-color);
  border: none;

}
.login .forgot-row button:hover {
  text-decoration: underline;
  text-decoration-color: red;
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
  color: white;
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
