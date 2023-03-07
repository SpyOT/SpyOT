<template>
    <div class="wrapper">
        <div class="header">
            <h1>Dashboard</h1>
        </div>
        <div class="body">
            <div class="dev-sel-container">
                <h2>Device:</h2>
                <button>TEMPORARY THING FOR DEVICE LIST</button>
            </div>
            <div class="table-container">
                <Table
                :headers="headers"
                :items="items"
            />
            </div>
            <div class="row-container">
                <div class="graph-container">
                    <h2>Graph Container</h2>
                </div>
                <div class="vuln-container">
                    <h2>Vulnerabilities Container</h2>
                </div>
            </div>


        </div>
        
    </div>
</template>

<script>
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
      }
    },
    };

</script>


<style>
h1 {
    color: var(--secondary-color);
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
    width: 100%;

}
.body .row-container .graph-container{
    width: 50%;
    float: left;
    border-radius: 4px;
    border: solid;
    border-color: var(--primary-color);
    
}
.body .row-container .vuln-container{
    width: 50%;
    float:right;
    border-radius: 4px;
    border: solid;
    border-color: var(--primary-color);
    
}

</style>