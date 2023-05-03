<template>
  <div class="wrapper">
    <div class="header">
      <h1>Dashboard</h1>
    </div>
    <div class="body">
      <div class="reports">
        <select v-model="selectedReport">
          <option disabled value="">Please select a report</option>
          <option
            v-for="(report, index) in reports"
            :key="index"
            :value="report"
          >
            {{ report.name }}
          </option>
        </select>
      </div>
      <div class="dev-sel-container">
      </div>
      <div class="table-container">
        <h1>Device Status:</h1>
        <select v-model="selectedDevice" v-if="selectedReport">
          <option disabled value="">Please select a device</option>
          <option
            v-for="(device, index) in selectedReport.content"
            :key="index"
            :value="device"
          >
            {{ index }}
          </option>
        </select>
        <div class="device-info">
          <ul v-if="selectedDevice">
            <li>IP Address: {{ selectedDevice.ip }}</li>
            <li>MAC Address: {{ selectedDevice.mac }}</li>
            <li>
              Ports:
              {{
                Object.entries(selectedDevice.ports)
                  .map(([port, status]) => `${port}: ${status}\n`)
                  .join("")
              }}
            </li>
            <li>Status: {{ selectedDevice.status }}</li>
          </ul>
        </div>
      </div>
      <div class="row-container">
        <!-- <div class="graph-container">
          <h2>Overall Data Encrypted (%)</h2>
        </div> -->
        <div class="vuln-container" v-if="selectedDevice && selectedDevice.status">
          <h2>Potential Vulnerabilities</h2>
          <img  v-on:click="mirai" src="../../assets/skull.PNG" alt="skull" />
          <h3>Click for more information</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "vue3-easy-data-table/dist/style.css";
import Vue3EasyDataTable from "vue3-easy-data-table";

import { getAuth } from "firebase/auth";
import { ref, child, get } from "firebase/database";
import { db } from "../../main.js";

export default {
  components: {
    Table: Vue3EasyDataTable,
  },
  created() {
    const auth = getAuth();
    auth.onAuthStateChanged((user) => {
      if (user) {
        console.log("User is logged in!");
        this.loggedIn = true;
        this.user = user;
        this.getInfo(user);
      }
      // } else {
      //     console.log('User is not logged in!');
      //     this.loggedIn = false;
      //     this.user = null;
      //     this.reports = [];
      // }
    });
  },
  data() {
    return {
      headers: [
        { text: "IP ADDRESS", value: "ip_address", sortable: true },
        { text: "OPEN PORTS", value: "open_ports", sortable: true },
        { text: "MAC ADDRESS", value: "mac_address", sortable: true },
      ],
      items: [
        { ip_address: "192.523.21", open_ports: [30, 190], mac_address: 77 },
        { ip_address: "314.321.32", open_ports: 180, mac_address: 75 },
        { ip_address: "412.521.63", open_ports: 181, mac_address: 73 },
      ],
      click: "",
      // reports: ["1", "2"],
      user: null,
      info: [],
      reports: [],
      selectedReport: null,
      selectedDevice: null,
      error: null,
    };
  },

  methods: {
    mirai() {
      this.$router.push("/dashboard/info");
      console.log("PUT INFO HERE");
    },
    getInfo(user) {
      const userRef = ref(db, `users/${user.uid}`);

      get(userRef)
        .then((snapshot) => {
          const data = snapshot.val();
          if (data) {
            this.info = Object.entries(data)
              .slice(6)
              .map(([key, value]) => {
                return {
                  name: key,
                  content: value,
                };
              });
            console.log(this.info);
            this.getReports();
          } else {
            this.info = [];
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getReports() {
      if (this.info.length) {
        for (const report of this.info) {
          const key = report.name;
          const value = report.content;
          if (key.startsWith("report-")) {
            this.reports.push({
              name: key,
              content: value,
            });
          }
        }
        console.log(this.reports);
      } else {
        this.reports = [];
      }
    },
  },
  watch: {
    selectedReport(newValue) {
      console.log("Selected report:", newValue);
      this.selectedDevice = null;
    },
    selectedDevice(newValue) {
      console.log("Selected object:", newValue);
    },
  },
  computed: {
  deviceImage() {
    if (this.selectedDevice && this.selectedDevice.status === 'Secure') {
      return '/path/to/secure-image.png';
    } else {
      return '/path/to/bad-image.png';
    }
  }
}



};
</script>

<style scoped>
.header h1 {
  color: var(--primary-color);
}
.table-container h1 {
  color: var(--primary-color);
}
li {
  color: var--primary-color);
  font-size: 1.5em;
}

h3 {
  font-weight: bold;
  color: var(--primary-color);
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
.body .dev-sel-container h2 {
  justify-content: left;
  text-align: left;
}
.body .row-container {
  display: flex;
  margin-top: 6em;
  width: 100%;
  /* align-content: center; */
  /* align-items: center; */
  justify-content: center;
}
.device-info {
  padding: 1em;
  background-color: var(--color-background);
  border-radius: 5px;
  width: 50%;
  margin-top: 1em;
}

.device-info ul {
  color: var(--primary-color);
  list-style-type: none;
  padding: 0;
}

.device-info li {
  color: var(--primary-color);
  font-size: 1.2em;
  margin-bottom: 0.5em;
}
.body .row-container .graph-container {
  width: 50%;
  float: left;
  border-radius: 1px;
  border: solid;
  border-color: var(--primary-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 300px;
}
img .skull {
  height: 200px;
  border: 1px solid red;
  margin-bottom: 2em;
}
.body .row-container .vuln-container {
  display: flex;
  flex-direction: column;
  width: 40%;
  height: 20em;
  /* margin-right: 5em; */
  float: right;
  border-radius: 1px;
  border: solid;
  border-color: var(--primary-color);
  align-items: center;
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
