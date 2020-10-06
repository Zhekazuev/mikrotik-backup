import paramiko
import config
import re

user = config.user
password = config.password


def get_aps_ips(ip_address):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip_address, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command("interface eoip print detail where running")
    eoip_interfaces = stdout.read().decode("utf8")
    ip_address = re.findall(r"\s+remote-address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+", eoip_interfaces)
    ssh.close()
    return ip_address


def main():
    script = config.script
    ips_hubs = config.ips_hubs
    ap_addresses = []
    for ip_hub in ips_hubs:
        ap_addresses.extend(get_aps_ips(ip_hub))
    ap_addresses = set(ap_addresses)

    for ap_address in ap_addresses:
        print(f"Work with {ap_address}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ap_address, username=user, password=password)
        stdin, stdout, stderr = ssh.exec_command(f"system script add name=autobackup source=\"{script}\"")
        script_create_result = stdout.read().decode("utf8")
        print(f"\tCreated backup script result: {script_create_result}")
        stdin, stdout, stderr = ssh.exec_command(f"system scheduler add name=config_backup "
                                                 f"on-event=\"/system script run autobackup\" "
                                                 f"policy=ftp,read,write,test,password,romon,sniff,policy,sensitive "
                                                 f"start-time=\"05:00:00\" interval=\"1d 00:00:00\"")
        schedule_create_result = stdout.read().decode("utf8")
        print(f"\tCreated schedule result: {schedule_create_result}")
        print(f"End with {ap_address}")
        ssh.close()


if __name__ == '__main__':
    main()
