<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <!-- <TheWelcome></TheWelcome> -->
    <h1>SpyOT</h1>
    <h3>CS 426 Senior Project in Computer Science</h3>
    <br>
    <h2>Department of Computer Science & Engineering</h2>
    <h3>University of Nevada, Reno - Spring 2023</h3>
    <br>
    <div>
      <article>
        <h2> Team 19 - The Backend Bois'</h2>
        <p>
          <ul>
            <li>Kenneth Peterson</li>
            <li>Kenneth Escovilla</li>
            <li>Rameen Feda</li>
            <li>Javier Perez</li>
          </ul>          
        </p>
        <h2>Instructors</h2>
        <p>
          <ul>
            <li>Dr. Sergiu Dascalu</li>
            <li>Dr. David Feil-Seifer</li>
            <li>Devrin Lee</li>
          </ul>
        </p>
        <h2>External Advisor</h2>
        <p>
          <ul>
            <li>
              Dr. Batyr Charyyev: UNR Assistant Professor - CSE Department
            </li>
          </ul>
        </p>
      </article>
    </div>
    <br>
    <div>
      <article id="description">
        <h2>Project Desciption</h2>
        <p>
          &emsp;&emsp;The main goal of this project is to create a cybersecurity program that identifies security vulnerabilities on a user’s network/IoT environment with attached IOT and smart devices. With this program, we’ll be able to collect data that can be used to inform the user of potential vulnerabilities in their network.These vulnerabilities are typically linked to malicious attacks or creating larger botnets.
          <br>
          &emsp;&emsp;The initial objective is to first identify the devices connected on a user’s network. Once all devices are accounted for via IP, the next objective will be to compile this data into a list and/or graph that can be easily understood by the user. Once the user has an understanding of all connected devices in their network, the last objective is to inform the user of suggestions to improve the network's security, which can be used to prevent malicious attacks on the network and its connected IOT devices.
          <br>
          &emsp;&emsp;Users that are concerned with the quality of their home or commercial smart devices may want to know if their devices are at-risk of being used without permission. Some families or commercial businesses may want to double down on paying for higher end security devices given the level of protection one product has to offer from another. Commercial businesses that are concerned with potential vulnerabilities in their IoTs may want to get a proper diagnosis of their smart devices to see if action is worth taking. Families who are concerned with the state of their smart devices might want to strengthen their sense of comfort by assuring that none of their devices are capable of being used for a botnet.
        </p>
      </article>
    </div>
    <br>
    <div id="resources">
      <h2>Resoures</h2>
      <ul>
        <li><a href="https://www.holmsecurity.com/blog/what-is-nmap" target="_blank">
          Thelberg, Stefan. HolmSecurity. “Nmap -What is it and how does it work”</a></li>
        <li><a href="https://linuxhint.com/zenmap_scan_network/" target="_blank">
          Adams, David. Linuxhint. “How to use Zenmap to Scan a network”</a></li>
        <li><a href="https://linuxhint.com/unicornscan_beginner_tutorial/" target="_blank">
          Said, Younis. Linuxhint. “Unicornscan: A beginner’s guide”</a></li>
      </ul>
    </div>
  </main>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    /* display: flex; */
    /* align-items: center; */
  }
}
h1 {
  text-align: center;
  font-size: 4rem;
}
h3, h2, article {
  text-align: center;
}
li {
  list-style:none;
}
#description h2, p{
  text-align: left;
}
#resources h2 {
  text-align: left;
}
</style>