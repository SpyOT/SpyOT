import systems as SIsys

class MainMenu:
    def __init__(self):
        self.title = "Main Menu"
        self.user_choice = True
        self.options = {0:{"isAvailable":True, "output":"Exit Program"},
                        1:{"isAvailable":True, "output":"About"},
                        2:{"isAvailable":True, "output":"Setup Network"},
                        3:{"isAvailable":False, "output":"View Network"}}
        self.network = None

    def loop(self):
        while self.user_choice:
            self.state_output()
            self.state_input()
            self.update()

    def state_output(self):
        print(self.title)
        print("Options")
        for opt in self.options:
            if self.options[opt]["isAvailable"]:
                print(str(opt) + ":", self.options[opt]["output"])

    def state_input(self):
        self.user_choice = int(input("Input: "))
        print()
        match self.user_choice:
            case 0:
                print("Goodbye!")
            case 1:
                self.about()
            case 2:
                self.network = SIsys.NetworkManager()
            case 3:
                pass
            case _:
                print("\n!Error: Input", self.user_choice, "is not a valid choice. Please enter")
                print("one of the options listed.\n")

    def update(self):
        if self.network:
            self.options[3]["isAvailable"] = self.network.isSetup

    def about(self):
        print(
            """
            Background: For this senior project, we attempt to tackle the beginning of a cybersecurity problem that user networks 
            face when having a vast IoT environment that malicious software can manipulate and take advantage of by informing the 
            user of the threats that are associated with the vulnerabilities of their network. In order to inform the user, first we 
            need to identify connected IoT devices that are on a user’s network. Once those devices are detected and the data is 
            compiled into a list or graph, there needs to be a simple and easy to understand way of displaying that information of 
            the detected devices to the user so that the user can understand which devices are at risk of malicious software. As 
            the user is informed of their at-risk devices, then the user can begin the steps towards improving their network 
            security in order to prevent malicious software from attaching themselves to their network of IoT devices.

            Purpose: Our project’s mission towards network security is to improve a user’s network. To improve the user’s network, a 
            layer of security can be provided by supplying the user readable knowledge of their network’s vulnerabilities towards 
            bad-agents that use malware and malicious software to access that user’s network. If that user is able to see their 
            network, understand and utilize what information they have then the project has successfully completed its mission.

            Mission: With the amount of IoT environments that are available to the non-technical public comes the great need for 
            security and a way to monitor that environment. Our project will provide that peace of mind that users with 
            non-technical knowledge will likely desire without taking a more expensive route for security measures on just detecting 
            vulnerabilities and threats.
                    
            - Back-End Boys
            """)
