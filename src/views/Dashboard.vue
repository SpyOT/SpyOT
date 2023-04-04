<template>
    <div class="dashboard">
      <Sidebar />
      <div class="body">
        <router-view></router-view>
      </div>
      
    </div>
  </template>
  
  <script setup>
  import Sidebar from  "../components/Sidebar.vue";

  </script>
  
  <style scoped>
  .dashboard {
    background-color: black;
    display: flex;
    /* column-gap: 3em; */
  }
  
  .body {
    margin-left: 3em;
    flex-grow: 1;
    margin-right: 2em;
    background-color: black;
    /* margin-bottom: 5em; */
  }
  
  
  
  </style>
  
  