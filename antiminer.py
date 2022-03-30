#! -*- coding: utf-8 -8-
# 监控查杀挖矿病毒

import os
import psutil
import datetime
import json
import time
import sys

fw = open('kill.log', 'a+')


def check(p):
    path, _ = os.path.split(p.exe())
    if os.path.exists(path + '/lolMiner.cfg'):
        return 1
    if os.path.exists(p.cwd() + '/lolMiner.cfg'):
        return 2
    if p.exe().startswith('/tmp') and 'ssh' in p.exe():
        return 2
    if p.exe().startswith('/tmp') and 'socat' in p.exe():
        return 2
    return 0


def do(p):
    code = check(p)
    if code == 0:
        return None
    log = {'time': str(datetime.datetime.now()), 'cwd': p.cwd(), 'exe': p.exe()}
    print(log)
    fw.write(json.dumps(log) + '\n')
    fw.flush()
    p.kill()
    if code == 1:
        os.system('sudo rm -rf %s' % log['exe'])
        os.system('sudo touch %s' % log['exe'])
        os.system('sudo chattr +i %s' % log['exe'])


def wait(n):
    for i in range(1, n + 1):
        sys.stdout.write(u'\r监控中' + '.' * i)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + ' ' * 100 + '\r')


while True:
    for p in psutil.process_iter():
        try:
            do(p)
        except:
            pass
    wait(5)
