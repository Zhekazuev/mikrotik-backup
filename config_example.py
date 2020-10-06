user = "user"
password = "password"
ips_hubs = ["1.1.1.1", "1.1.1.2", "1.1.1.3"]


script = """#Backup configuration Mikrotik\r\n
#Get date in format dd-mm-yyyy\n\r
:local tmpdate [/system clock get date];\r\n"""
