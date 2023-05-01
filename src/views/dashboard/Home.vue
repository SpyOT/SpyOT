<template>
    <div class="wrapper">
        <div class="header">
            <h1>Dashboard</h1>
        </div>
        <div class="body">
            <div class="dev-sel-container">
                <ul>
                    <li>Number of Devices: 3</li>
                    <li>Overall Data Encrypted: 85</li>
                    <li>Potential Vulnerabilities: 1</li>
                </ul>

                <!-- <button>TEMPORARY THING FOR DEVICE LIST</button> -->
            </div>
            <div class="table-container">
                <h1>Device Status:</h1>
                <Table
                table-class-name="dash"
                :headers="headers"
                :items="items"
                border-cell
            />
            </div>
            <div class="row-container">
                <div class="graph-container">
                    <h2>Data Encrypted (%)</h2>
                    <img src="../../assets/chart.PNG" alt="chart">
                </div>
                <div class="vuln-container">
                    <h2>Potential Vulnerabilities</h2>
                    <img v-on:click="mirai" src="../../assets/skull.PNG" alt="skull">
                    <h3>Click on the vulnerabilites for more information</h3>
                </div>
            </div>


        </div>
        
    </div>
</template>

<script>
import 'vue3-easy-data-table/dist/style.css';
import { Pie } from 'vue-chartjs';
import Vue3EasyDataTable from 'vue3-easy-data-table';
    export default {
        components: {
            Table: Vue3EasyDataTable,
    },
    data () {
      return {
        headers:[
          { text: "IP ADDRESS", value: "ip_address", sortable: true },
          { text: "OPEN PORTS", value: "open_ports", sortable: true },
          { text: "MAC ADDRESS", value: "mac_address", sortable: true },
        ],
        items: [
          { "ip_address": "192.523.21", "open_ports": [30, 190], "mac_address": 77},
          { "ip_address": "314.321.32", "open_ports": 180, "mac_address": 75},
          { "ip_address": "412.521.63", "open_ports": 181, "mac_address": 73}
        ],
        click: ""
      }
    },
    methods: {
        mirai(){
            this.$router.push("/dashboard/info");
            console.log("PUT INFO HERE");
        }
    }
    };
    

</script>


<style>
.header h1 {
    color: white;
}
.table-container h1 {
    color: white;
}
li {
    color: white;
    font-size: 1.5em;
}

h3 {
    font-weight: bold;
}

.body {
    display: flex;
    flex-direction: column;
}

.body .dev-sel-container {
    display: flex;
}
.body .dev-sel-container button {
    font-size: 0.8em;
}
.body .dev-sel-container h2{
    justify-content: left;
    text-align: left;
}
.body .row-container {
    margin-top: 6em;
    width: 100%;

}
.body .row-container .graph-container{
    width: 50%;
    float: left;
    border-radius: 1px;
    border: solid;
    border-color: white;
    display:flex;
    flex-direction: column;
    align-items: center;
    height: 300px;
    
}
img .skull {
    height: 200px;
    border: 1px solid red;
}
.body .row-container .vuln-container{
    display:flex;
    flex-direction: column;
    width: 40%;
    height: 300px;
    /* margin-right: 5em; */
    float:right;
    border-radius: 1px;
    border: solid;
    border-color: white;
    align-items: center
    
}

.dash {
    border: 1px solid var(--primary-color);
    /* border-top: 1px solid var(--primary-color); */
    --easy-table-header-background-color: var(--primary-color);
    --easy-table-body-row-background-color: black;
    --easy-table-body-row-font-color: white;
    --easy-table-footer-background-color: black;
    --easy-table-footer-font-color: white;
    /* header-background-color: red; */
}


</style>