# -*- coding: UTF-8 -*-
import psutil
import datetime
import sys
import json

"""
check number of java process running
"""
warning = 30
critical = 50


class ProcessCount(object):
    """
    search process name and count
    """

    def __init__(self, name_process="java"):
        self.process_name = name_process
        self.cpt = 0
        self.process_list = {}

    def get_proces(self):
        try:
            for p in psutil.process_iter():
                if p.name() == self.process_name:
                    self.cpt += 1
                    process_start_date = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
                    self.process_list[p.pid] = p.cmdline()[5], process_start_date

        except Exception as e:
            print('error: get process: {}'.format(e))
            sys.exit(2)

    def nagios(self):
        json_data = json.dumps(self.process_list)
        if self.cpt >= warning:
            print("warning: total of process {} is {} | Total={}, process_list={}".format(
                self.process_name, self.cpt, self.cpt, json_data))
            sys.exit(1)
        elif self.cpt >= critical:
            print("critical: total of process {} is {} | Total={}, process_list={}".format(
                self.process_name, self.cpt, self.cpt, json_data))
            sys.exit(2)
        else:
            print("ok: total of process {} is {} | Total={}, process_list={}".format(
                self.process_name, self.cpt, self.cpt, json_data))
            sys.exit(0)


if __name__ == "__main__":
    proc = ProcessCount()
    proc.get_proces()
    proc.nagios()

