import pyshark
import os
import threading


class PCAP:
    def __init__(self):
        self.capture_file = 'packet_capture.pcap'
        print("Generating PCAP file...")
        # threading.Thread(target=lambda: os.system("tshark -i wi-fi -c 2000 -w " + self.capture_file)).start()
        # self.capture = pyshark.FileCapture(self.capture_file)
        # self.tcp_packets = pyshark.FileCapture(self.capture_file, display_filter='tcp.payload')
        # self.udp_packets = pyshark.FileCapture(self.capture_file, display_filter='udp.payload')

        self.TCPpayload = None
        self.TCPdata = ""
        self.Encrypted_counter = 0
        self.Non_encrypted_counter = 0
        self.total = 0

    def generatePCAP(self, device_ips):
        print("PCAP file generated.")
        self.capture = pyshark.FileCapture(self.capture_file)
        device_packets = {}
        for ip in device_ips:
            device_packets[ip] = {
                'tcp': pyshark.FileCapture(self.capture_file,
                                           display_filter='ip.src==' + ip + ' && tcp.payload &&' + 'ip.dst==' + ip),
                'udp': pyshark.FileCapture(self.capture_file,
                                           display_filter='ip.src==' + ip + ' && udp.payload &&' + 'ip.dst==' + ip)
            }
        self.tcp_packets = pyshark.FileCapture(self.capture_file, display_filter='tcp.payload')
        self.udp_packets = pyshark.FileCapture(self.capture_file, display_filter='udp.payload')
        print("Device packets generated.")
        return device_packets

    def tcpPacketAnalysis(self, tcpcap):
        with tcpcap as cap:
            for packet in cap:
                has_encryption_header = hasattr(packet, 'tls') or hasattr(packet, 'ssh') or hasattr(packet, 'ssl')
                if has_encryption_header:
                    self.Encrypted_counter += 1
                else:
                    self.Non_encrypted_counter += 1
        return self.Encrypted_counter, self.Non_encrypted_counter

    def udpPacketAnalysis(self, udpcap):
        with udpcap as cap:
            for packet in cap:
                has_encryption_header = hasattr(packet, 'srtp') or hasattr(packet, 'quic') or hasattr(packet, 'dtls')
                if has_encryption_header:
                    self.Encrypted_counter += 1
                else:
                    self.Non_encrypted_counter += 1
        return self.Encrypted_counter, self.Non_encrypted_counter

    def packetAnalysis(self):
        with self.tcp_packets as tcp:
            for i, packet in enumerate(tcp):
                has_encryption_header = hasattr(packet, 'tls') or hasattr(packet, 'ssh') or hasattr(packet, 'ssl')
                if has_encryption_header:
                    self.Encrypted_counter += 1
                else:
                    self.Non_encrypted_counter += 1
        with self.udp_packets as udp:
            for packet in udp:
                has_encryption_header = hasattr(packet, 'srtp') or hasattr(packet, 'quic') or hasattr(packet, 'dtls')
                if has_encryption_header:
                    self.Encrypted_counter += 1
                else:
                    self.Non_encrypted_counter += 1
        self.total = self.Encrypted_counter + self.Non_encrypted_counter

    def packetCapture(self):
        for packet in self.capture:
            try:
                if 'tls' in packet and 'tcp' in packet or 'quic' in packet:  # In the case that a packet is fully encrypted
                    print('Packet is encrypted.')
                    self.Encrypted_counter += 1
                    self.total += 1
                elif packet.tcp.payload in packet is None:  # In the case that no payload was found/given
                    print("No payload")
                    self.total += 1
                else:
                    self.total += 1  # If the above ifs aren't met, we start counting packets.
                    self.Non_encrypted_counter += 1
                    hex_string = str(self.TCPpayload)
                    hex_split = hex_string.split(":")
                    hex_as_chars = map(lambda hex: chr(int(hex, 16)), hex_split)
                    human_readable = "".join(hex_as_chars)
                    # print(human_readable)
            # print (type(payload))
            # print(str(payload))
            except:
                pass
        # break
        self.capture.close()
        self.dataEncryptionPercent()
        pass  # Best to think of a return value so we can test this function

    def dataEncryptionPercent(self):
        print("Total number of packets analyzed:", self.total)
        Percentage_of_encrypted = (self.Encrypted_counter / (
                self.Non_encrypted_counter + self.Encrypted_counter)) * 100
        print("Percentage of encrypted data ", Percentage_of_encrypted)
        return Percentage_of_encrypted


if __name__ == '__main__':
    PCAP_instance = PCAP()
    PCAP_instance.generatePCAP({})
    PCAP_instance.packetAnalysis()
    # PCAP_instance.packetCapture()
    # PCAP_instance.findTCPpayload()
