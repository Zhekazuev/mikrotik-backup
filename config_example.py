ap_user = "user"
ap_password = "pass"
hub_user = "user"
hub_password = "pass"
ips_hubs = ["1.1.1.1", "1.1.1.2"]
ips_wlcs = ["2.2.2.1", "2.2.2.2", "2.2.2.3", "2.2.2.4"]


script = ["#Backup configuration Mikrotik\\r\\n",
          "#Get date in format dd-mm-yyyy\\r\\n",
          ":local tmpdate [/system clock get date];\\r\\n",
          ":local months (\\\"jan\\\",\\\"feb\\\",\\\"mar\\\",\\\"apr\\\",\\\"may\\\",\\\"jun\\\",\\\"jul\\\",\\\"aug\\\",\\\"sep\\\",\\\"oct\\\",\\\"nov\\\",\\\"dec\\\");\\r\\n",
          ":local month [ :pick \$tmpdate 0 3 ];\\r\\n",
          ":local mm ([ :find \$months \$month -1 ] + 1);\\r\\n",
          ":if (\$mm < 10) do={ :set mm (\\\"0\\\" . \$mm); }\\r\\n",
          ":local date ([:pick \$tmpdate 4 6] .\\\"-\\\" . \$mm .\\\"-\\\" . [:pick \$tmpdate 7 11])\\r\\n\\r\\n",
          "#Create variables and parameters for FTP\\r\\n\\r\\n",
          ":local myname [/system identity get name]\\r\\n",
          ":local fname (\$myname.\\\"_\\\".\$date);\\r\\n:local bname (\$myname.\\\"_\\\".\$date.\\\".backup\\\");\\r\\n",
          ":local ename (\$myname.\\\"_\\\".\$date.\\\".rsc\\\");\\r\\n",
          ":local ftpuser \\\"user\\\";\\r\\n",
          ":local ftppass \\\"pass\\\";\\r\\n",
          ":local ftpaddr \\\"address\\\";\\r\\n",
          ":local ftppath \\\"ftppath\\\"\\r\\n\\r\\n",
          "#Get system parameters\\r\\n\\r\\n",
          "/system backup save name=\$fname password=\\\"\\\";\\r\\n",
          ":delay 10;\\r\\n",
          "/export file=\$fname\\r\\n",
          ":delay 10;\\r\\n\\r\\n",
          "#Push configuration to FTP\\r\\n\\r\\n",
          "/tool fetch address=\$ftpaddr src-path=\$bname user=\$ftpuser password=\$ftppass port=21 upload=yes mode=ftp dst-path=\\\"\$ftppath/\$bname\\\"\\r\\n",
          ":delay 15;\\r\\n",
          "/tool fetch address=\$ftpaddr src-path=\$ename user=\$ftpuser password=\$ftppass port=21 upload=yes mode=ftp dst-path=\\\"\$ftppath/\$ename\\\"\\r\\n",
          ":delay 15;\\r\\n\\r\\n",
          "#Remove backup on mikrotik\\r\\n",
          "/file remove \$bname;\\r\\n",
          "/file remove \$ename;\\r\\n"]
