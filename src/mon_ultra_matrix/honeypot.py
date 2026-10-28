"""HoneyRoot-X - SSH honeypot log analysis: brute-force attempts, top attackers/creds tried."""
import re
from collections import Counter
LINE = re.compile(r"(?P<ip>\d+\.\d+\.\d+\.\d+).*?(?:user|username)[:= ]+(?P<user>\S+).*?(?:pass|password)[:= ]+(?P<password>\S+)", re.I)
def parse_log(text):
    ips=Counter(); users=Counter(); passwords=Counter(); total=0
    for line in text.splitlines():
        m=LINE.search(line)
        if m: total+=1; ips[m.group("ip")]+=1; users[m.group("user")]+=1; passwords[m.group("password")]+=1
    return {"attempts": total, "top_ips": ips.most_common(5), "top_users": users.most_common(5), "top_passwords": passwords.most_common(5)}
def bait_note(): return "HoneyRoot-X uses root-access bait: every login attempt is hostile by definition - log, never allow."
