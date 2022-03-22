import subprocess
import re


class WifiConfigurator:
    ssid = ''
    psk = None

    def __init__(self, ssid, psk=None):
        self.ssid = ssid
        self.psk = psk

    def reconfigure(self):
        if not self.ssid:
            raise Exception("SSID must not be empty")
            return

        print("Updating Wifi Configuration")
        base_command = "wpa_cli -i wlan0 "
        network_number = '1'
        successful = False
        try:
            result = self.execute_command(base_command + "get_network " + network_number + " ssid")
            if result.startswith('FAIL'):
                print("network does not exist... creating")
            else:
                print("network exists... removing then recreating")
                if self.execute_command(base_command + "remove_network 1").startswith('FAIL'):
                    raise Exception("Error: Could not remove old network")

            self.execute_command(base_command + "save_config")

            num = self.execute_command(base_command + "add_network")
            if num.startswith('FAIL'):
                raise Exception("Error: Could not add new network")
            else:
                network_number = re.sub("\D", "", num)

            if not self.execute_command(base_command + "set_network " + network_number + " ssid '\"" + self.ssid + "\"'").startswith('OK'):
                raise Exception("Error: Could not set SSID")

            if self.psk is None:
                if not self.execute_command(base_command + "set_network " + network_number + " key_mgmt NONE").startswith('OK'):
                    raise Exception("Error: Could not set key management to NONE")
            else:
                if not self.execute_command(base_command + "set_network " + network_number + " key_mgmt WPA-PSK").startswith('OK'):
                    raise Exception("Error: Could not set key management to WPA-PSK")
                if not self.execute_command(base_command + "set_network " + network_number + " psk '\"" + self.psk + "\"'").startswith('OK'):
                    raise Exception("Error: Unable to set PSK")

            if not self.execute_command(base_command + "enable_network " + network_number).startswith('OK'):
                raise Exception("Error: Failed to enable network")

            successful = True
            print("Update Successful")
        except Exception as ex:
            print(ex)
            print("Update Failed")
        finally:
            self.execute_command(base_command + "save_config")
            self.execute_command(base_command + "reconfigure")
            return successful

    def execute_command(self, command):
        output, error = subprocess.Popen(command, universal_newlines=True, shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        #print("executing command, " + command + " -> " + output)
        return output

