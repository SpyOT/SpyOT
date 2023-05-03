<template>
    <div class="wrapper">
        <div class="color">
            <h1>Color Mode</h1>
            <h2>Click on the button to change from light/dark mode</h2>
            <button @click="toggleColorMode">{{ colorMode }}</button>
        </div>
        <div class="delete">
            <h1>Delete Account</h1>
            <button @click="deleteAccount">Delete Your Account</button>
        </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import { getAuth, deleteUser } from "firebase/auth";
  
  export default {
    setup() {

    const auth = getAuth();
    const error = ref("");

    const deleteAccount = async () => {
      try {
        await deleteUser(auth.currentUser);
        console.log("User account deleted");
        // this.$router.push("/");
      } catch (err) {
        error.value = err.message;
        console.error("Error deleting user account", error.value);
      }
    };
      const colorMode = ref("light");
  
      const toggleColorMode = () => {
        colorMode.value = colorMode.value === "dark" ? "light" : "dark";
  
        // Change the data-color-mode attribute on the root element
        const rootElement = document.documentElement;
        if (colorMode.value === "dark") {
          rootElement.setAttribute("data-color-mode", "dark");
        } else {
          rootElement.setAttribute("data-color-mode", "light");
        }
      };
  
      return {
        colorMode,
        toggleColorMode,
        deleteAccount,
        error,
      };
    },
  };
  </script>
 <style scoped>
.color, .delete{
    display: flex;
    flex-direction: column;
}
h2{
    color: var(--opps2);
}
</style>
  
  
  
  
  
  
  