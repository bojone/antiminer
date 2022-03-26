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
        return True
    if os.path.exists(p.cwd() + '/lolMiner.cfg'):
        return True
    if p.exe().startswith('/tmp') and 'ssh' in p.exe():
        return True


def do(p):
    log = {'time': str(datetime.datetime.now()), 'path': p.exe()}
    print(log)
    fw.write(json.dumps(log) + '\n')
    fw.flush()
    p.kill()
    os.system('sudo rm %s' % log['path'])
    os.system('sudo touch %s' % log['path'])
    os.system('sudo chattr +i %s' % log['path'])


def wait(n):
    for i in range(1, n + 1):
        sys.stdout.write(u'\r监控中' + '.' * i)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + ' ' * 100 + '\r')


while True:
    for p in psutil.process_iter():
        if check(p):
            do(p)
    wait(5)
