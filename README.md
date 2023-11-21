# TriVirus File Transfer Protocol
### [insert description here]

### How to use the tool
1. The victim and the attacker device should have a working TFTP server. For the victim, they must utilize tftpd64 which can be downloaded here https://tftpd64.software.informer.com/download/. Meanwhile, the attacker who is using Kali LInux can use tftp-hpa, which can be installed via the terminal.

2. The attacker must have information about the victim’s IP address.This can be identified through the scanning tool, nmap and using zenmap to inspect the open ports and its corresponding services.

3. The attacker runs the application TFTP by running the python code given. To be specific, the attacker must run GUIDriver.py.

4. Through the application, the attacker inputs the victim’s IP address, selects where the .exe file is located within the attacker’s files, and creates a new file name to be sent to the victim’s device.

5. The attacker should click the “Upload” button to be able to send the infected .exe file.

6. The attacker must check the log if the file was successfully sent. If it is not, recheck the IP address, server or the file being sent.

7. When the file is successfully sent to the victim’s device, the victim must click on the .exe file for the attacker to successfully hack the victim’s device.

8. Once the .exe file executes, the attacker can now access the victim’s device through Metasploit to run commands such as using its privilege escalation, screenshot capture, file manipulation, and other various actions.


