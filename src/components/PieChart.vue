<template>
    <div>
      <pie-chart :data="chartData"></pie-chart>
    </div>
  </template>
  
  <script>
  import { Pie } from "vue-chartjs";
  
  export default {
    extends: Pie,
    props: {
      data: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        chartData: {
          labels: ["Encrypted Data (%)", "Unencrypted Data (%)"],
          datasets: [
            {
              backgroundColor: ["#0074D9", "#FF4136"],
              data: [this.data, 100 - this.data],
            },
          ],
        },
      };
    },
  };
  </script>