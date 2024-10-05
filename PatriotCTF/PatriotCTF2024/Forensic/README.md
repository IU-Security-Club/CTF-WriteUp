[__Simple Exfiltration__](#SimpleExfiltration)
```shell
tshark -r exfiltration_activity_pctf_challenge.pcapng -Y "icmp" -T fields -e 'ip.ttl' | sed 's/128//g' > wierd-ttl.txt
python3 -c "with open('wierd-ttl.txt', 'r') as wttl:print(''.join(chr(int(ttl)) for ttl in wttl if ttl != '\n'))"
```

