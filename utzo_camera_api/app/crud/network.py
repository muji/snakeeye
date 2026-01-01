
import os
import subprocess

def list_interfaces():
    result = []
    for iface in os.listdir('/sys/class/net'):
        if iface == 'lo': continue
        info = {'interface': iface, 'connected': False, 'ip': None, 'mac': None}
        try:
            ip = subprocess.check_output(['ip', '-4', 'addr', 'show', iface]).decode()
            if 'inet ' in ip:
                info['connected'] = True
                info['ip'] = ip.split('inet ')[1].split('/')[0]
        except:
            pass
        try:
            mac = open(f'/sys/class/net/{iface}/address').read().strip()
            info['mac'] = mac
        except:
            pass
        result.append(info)
    return result

def configure_wifi(data):
    conf = f'''
network={{
    ssid="{data.ssid}"
    psk="{data.password}"
}}
'''
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as f:
        f.write(conf)

    subprocess.run(["wpa_cli", "-i", data.interface, "reconfigure"])
    if not data.use_dhcp and data.static_ip:
        subprocess.run(["ip", "addr", "add", data.static_ip, "dev", data.interface])
        subprocess.run(["ip", "route", "add", "default", "via", data.gateway])
    return True

def configure_ethernet(data):
    if not data.use_dhcp and data.static_ip:
        subprocess.run(["ip", "addr", "flush", "dev", data.interface])
        subprocess.run(["ip", "addr", "add", data.static_ip, "dev", data.interface])
        subprocess.run(["ip", "route", "add", "default", "via", data.gateway])
    else:
        subprocess.run(["dhclient", data.interface])
    return True

def get_interface_status(interface):
    status = {'interface': interface, 'connected': False, 'ip': None, 'mac': None, 'ssid': None, 'signal_strength': None}
    try:
        ip = subprocess.check_output(['ip', '-4', 'addr', 'show', interface]).decode()
        if 'inet ' in ip:
            status['connected'] = True
            status['ip'] = ip.split('inet ')[1].split('/')[0]
    except:
        pass
    try:
        status['mac'] = open(f'/sys/class/net/{interface}/address').read().strip()
    except:
        pass
    try:
        scan = subprocess.check_output(['iwconfig', interface]).decode()
        for line in scan.splitlines():
            if "ESSID" in line:
                status['ssid'] = line.split("ESSID:")[1].strip().replace('"', '')
            if "Signal level" in line:
                level = line.split("Signal level=")[1].split(' ')[0]
                status['signal_strength'] = int(level)
    except:
        pass
    return status
