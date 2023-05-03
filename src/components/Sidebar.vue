<template>
  <aside :class="`${is_expanded ? 'is_expanded' : ''}`">
    <div class="logo">
      <p>SpyOT</p>
    </div>
    <div class="menu-toggle-wrap">
      <button class="menu-toggle" @click="ToggleMenu">
        <span class="material-icons-outlined">keyboard_double_arrow_right</span>
      </button>
    </div>

    <div class="menu">
      <router-link class="button" to="/dashboard">
        <span class="material-icons-outlined">dashboard</span>
        <span class="text">Dashboard</span>
      </router-link>
      <router-link class="button" to="/dashboard/generate-report">
        <span class="material-icons-outlined">build</span>
        <span class="text">Generate Report</span>
      </router-link>
      <router-link class="button" to="/dashboard/analyze-report">
        <span class="material-icons-outlined">search</span>
        <span class="text">Analyze Report</span>
      </router-link>
      <router-link class="button" to="/dashboard/view-report">
        <span class="material-icons-outlined">dns</span>
        <span class="text">View Report</span>
      </router-link>
      <router-link class="button" to="/dashboard/info">
        <span class="material-icons-outlined">info</span>
        <span class="text">Information</span>
      </router-link>
      <router-link class="button" to="/dashboard/settings">
        <span class="material-icons-outlined">settings</span>
        <span class="text">Settings</span>
      </router-link>
      <router-link class="button" to="/" @click="logout">
        <span class="material-icons-outlined">logout</span>
        <span class="text">Logout</span>
      </router-link>
    </div>

    <div class="padding"></div>

    <div class="menu">
      <Logout />
    </div>
  </aside>
</template>

<script setup>
import { ref } from "vue";
import { getAuth, signOut } from 'firebase/auth';
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = async () => {
  try {
    await signOut(getAuth());
    router.push({ name: 'home' });
  } catch (error) {
    console.log(error.message);
  }
};


const is_expanded = ref(localStorage.getItem("is_expanded") === "true");

const ToggleMenu = () => {
  is_expanded.value = !is_expanded.value;

  localStorage.setItem("is_expanded", is_expanded.value);
};
</script>

<style scoped>
button {
  cursor: pointer;
  appearance: none;
  border: none;
  outline: none;
  background: none;
}

aside div,
button {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

aside {
  display: flex;
  flex-direction: column;
  background-color: rgb(26, 25, 25);
  color: var(--color-text);
  width: calc(2rem + 32px);
  overflow: hidden;
  min-height: 100vh;
  padding: 1rem;
  transition: 0.2s ease-in-out;

}

aside .padding {
  height: 200px;
}

aside .logo {
  margin-bottom: 1rem;
}

aside .logo img {
  widows: 2rem;
}

aside .menu-toggle-wrap {
  /* display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  position: relative; */
  top: 0;
  transition: 0.2s ease-out;
  /* margin-left: none; */
}
aside .menu-toggle-wrap .menu-toggle {
  /* background-color: red; */
  /* padding-right: .4rem; */
  /* border: solid; */
  /* border-radius: 1px; */
  border-color: var(--secondary-color);
}

aside .menu-toggle-wrap .menu-toggle {
  transition: 0.2s ease-out;
}


aside.is_expanded {
  width: 300px;
}

aside.is_expanded .menu-toggle-wrap {
  top: -3rem;
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  position: relative;
  /* transition: 0.2s ease-out; */
}

aside.is_expanded .menu-toggle-wrap .menu-toggle {
  transform: rotate(-180deg);
}

aside.is_expanded h3,
aside.is_expanded .button .text {
  opacity: 1;
  display: inline;
  color: var(--color-text);
  transition: 0.2s ease-out;
  padding-right: 3em;
}

aside.is_expanded .button .material-icons-outlined {
  margin-right: 1rem;
  padding-left: .3em;
}

aside.is_expanded .logo {
  margin-bottom: 1rem;
  transform: scale(3.6);
  translate: 20.5rem 2rem;
}

.menu {
  margin: 1em -1rem;
}

.menu .button {
  display: flex;
  align-items: center;
  text-decoration: none;

  padding: 1rem 1rem;
  transition: 0.2s ease-out;
}


.menu .button:hover .material-icons-outlined,
.menu .button:hover .text,
.menu .button.router-link-exact-active .material-icons-outlined,
.menu .button.router-link-exact-active .text {
  color: var(--color-text);
}

.menu .button.router-link-exact-active {
  border-right: 5px solid var(--color-text);
  background: var(--secondary-color); 
  font-size: 1.3em;
  font-weight: 900;
  /* THIS ONE TO CHANGE */
}
aside.is_expanded .menu .button.router-link-exact-active{
  margin-left: .5em;
  margin-right: .5em;
  border-radius: 4px;
}

.menu .button .material-icons-outlined {
  font-size: rem;
  color: var(--color-text);
  transition: 0.2s ease-out;
  
}
.material-icons-outlined {
  color: var(--color-text);
}
.menu .button .text {
  display: none;
}
</style>
