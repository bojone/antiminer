#! -*- coding: utf-8 -8-
# 监控查杀挖矿病毒
# 更新日期：2022-04-04

import os
import psutil
import datetime
import time
import sys
import logging

filename = os.path.split(os.path.realpath(__file__))[0] + '/scan.log'
logging.basicConfig(
    filename=filename,
    filemode='a+',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def check(p):
    path, _ = os.path.split(p.exe())
    if os.path.exists(path + '/lolMiner.cfg'):
        return 1
    if os.path.exists(p.cwd() + '/lolMiner.cfg'):
        if p.exe().startswith('/tmp'):
            return 1
        else:
            return 2
    if p.exe().startswith('/tmp') and 'ssh' in p.exe():
        return 1
    if p.exe().startswith('/tmp') and 'socat' in p.exe():
        return 1
    return 0


def do(p):
    code = check(p)
    if code == 0:
        return None
    logging.warning('cwd: %s, exe: %s' % (p.cwd(), p.exe()))
    p.kill()
    if code == 1:
        os.system('sudo rm -rf %s' % log['exe'])
        os.system('sudo touch %s' % log['exe'])
        os.system('sudo chattr +i %s' % log['exe'])


for p in psutil.process_iter():
    try:
        do(p)
    except:
        pass

logging.info('scan has completed')
