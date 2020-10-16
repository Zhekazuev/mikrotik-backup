import paramiko
import config
import re


hub_user = config.hub_user
hub_password = config.hub_password
ap_user = config.ap_user
ap_password = config.ap_password


def get_aps_ips_wlc(ip_address):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip_address, username=hub_user, password=hub_password)
    stdin, stdout, stderr = ssh.exec_command("caps-man remote-cap print detail terse")
    caps_interfaces = stdout.read().decode("utf8")
    ip_address = re.findall(r"\s+address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d+\s+", caps_interfaces)
    ssh.close()
    return ip_address


def get_aps_ips_hubs(ip_address):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip_address, username=hub_user, password=hub_password)
    stdin, stdout, stderr = ssh.exec_command("interface eoip print detail without-paging where running")
    eoip_interfaces = stdout.read().decode("utf8")
    ip_address = re.findall(r"\s+remote-address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+", eoip_interfaces)
    ssh.close()
    return ip_address


def main():
    lines = config.script
    script = ""
    for line in lines:
        script += line

    ap_addresses = []

    ips_wlcs = config.ips_wlcs
    for ip_wlc in ips_wlcs:
        print(f"Work with {ip_wlc}")
        ap_addresses.extend(get_aps_ips_wlc(ip_wlc))
        print(f"The addresses from {ip_wlc} were successfully taken")

    ips_hubs = config.ips_hubs
    for ips_hub in ips_hubs:
        print(f"Work with {ips_hub}")
        ap_addresses.extend(get_aps_ips_hubs(ips_hub))
        print(f"The addresses from {ips_hub} were successfully taken")

    ap_addresses = set(ap_addresses)
    print(f"Total AP: {len(ap_addresses)}")

    for ap_address in ap_addresses:
        print(f"Work with {ap_address}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=ap_address, username=ap_user, password=ap_password)
            print(f"Problem with {ap_address}")
            stdin, stdout, stderr = ssh.exec_command(f"system script add name=autobackup source=\"{script}\"")
            script_create_result = stdout.read().decode("utf8")
            print(f"\tCreated backup script result: {script_create_result}")
            stdin, stdout, stderr = ssh.exec_command(f"system scheduler add name=autobackup "
                                                     f"on-event=\"/system script run autobackup\" "
                                                     f"policy=ftp,read,write,test,password,romon,sniff,policy,sensitive "
                                                     f"start-time=\"05:00:00\" interval=\"1d 00:00:00\"")
            schedule_create_result = stdout.read().decode("utf8")
            print(f"\tCreated schedule result: {schedule_create_result}")
            print(f"End with {ap_address}")
        except paramiko.ssh_exception:
            print(f"Problem with {ap_address}")
        ssh.close()


if __name__ == '__main__':
    main()
