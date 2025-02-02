#!/bin/env python3
"""
:author @night-raise  from github
cron: 0 0 */7 * *
new Env('随机定时');
"""

import json
import os
import random
import re
import time

from notify_mtr import send
from utils import get_data


def change_db():
    lines = []
    first = True
    with open("/ql/db/crontab.db", "r", encoding="UTF-8") as f:
        for l in f.readlines():
            if l.find("Oreomeow_checkinpanel_master") != -1:
                record = json.loads(l)
                if record.get("isDisabled") == 0:
                    record["schedule"] = change_time(record["schedule"], first)
                if first:
                    first = False
                lines.append(json.dumps(record, ensure_ascii=False) + "\n")
            else:
                lines.append(l)

    time_str = time.strftime("%Y-%m-%d", time.localtime())
    os.system(f"copy /ql/db/crontab.db /ql/db/crontab.db.{time_str}.back")

    with open("/ql/db/crontab.db", "w", encoding="UTF-8") as f:
        f.writelines(lines)


def change_time(time_str: str, first: bool):
    words = re.sub("\\s+", " ", time_str).split()
    if first:
        words[0] = str(random.randrange(60))
        words[1] = "9"
    else:
        words[0] = str(random.randrange(60))
        words[1] = str(random.randrange(22))
    return " ".join(words)


data = get_data()
ran_t = data.get("QL_RANDOM_TIME")
if ran_t:
    change_db()
    os.system("ql check")
    send("随机定时", "处于启动状态的任务定时修改成功！")
