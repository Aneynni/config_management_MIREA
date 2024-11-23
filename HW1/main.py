#!/bin/python3
import csv
import zipfile
import os
import calendar
import time
import re
import datetime
import xml.etree.ElementTree as ET

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.current_directory = '/'
        self.zip_file = zipfile.ZipFile(zip_path, 'r')

    def list_directory(self, path=''):
        current_prefix = self.current_directory.lstrip('/')
        if current_prefix and not current_prefix.endswith('/'):
            current_prefix += '/'
        
        entries = set()
        
        for file_info in self.zip_file.infolist():
            filename = file_info.filename
            if filename.startswith(current_prefix) and filename != current_prefix:
                relative_path = filename[len(current_prefix):].strip('/')
                if '/' in relative_path:
                    next_entry = relative_path.split('/', 1)[0]
                else:
                    next_entry = relative_path
                entries.add(next_entry)

        for entry in sorted(entries):
            print(entry, end = ' ')
        print()
    def change_directory(self, path):
        if path == '/':
            self.current_directory = '/'
        elif path == '..' or path == '../':
                if self.current_directory != '/':
                    self.current_directory = '/'.join(self.current_directory.rstrip('/').split('/')[:-1]) or '/'
        else:
            new_path = os.path.join(self.current_directory, path).replace('\\', '/')
            if any(file_info.filename.startswith(new_path.lstrip('/')) for file_info in self.zip_file.infolist()):
                self.current_directory = new_path
            else:
                print("Directory not found")

    def find(self, search_name):
        for file_info in self.zip_file.infolist():
            if search_name in os.path.basename(file_info.filename):
                print(file_info.filename)
                return
        print("No such directory or file")

def show_calendar():
    today = datetime.date.today()
    year  = today.year
    month = today.month
    thism = calendar.month(year,month)    # current month
    date  = today.day.__str__().rjust(2)
    rday  = ('\\b' + date + '\\b').replace('\\b ', '\\s')
    rdayc = "\033[7m" + date + "\033[0m"
    print( re.sub(rday,rdayc,thism))

    #now = datetime.datetime.now()
    #cal = calendar.TextCalendar()
    #print(cal.formatmonth(now.year, now.month))

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        with open(self.log_path, "wb") as log_file:
            log_file.write(b"<?xml version='1.0' encoding='UTF-8'?>\n<session>\n</session>")
    
    def log_action(self, user, command):
        now = datetime.datetime.now()
        log_entry = ET.Element("log_entry")
        ET.SubElement(log_entry, "user").text = user
        ET.SubElement(log_entry, "command").text = command
        ET.SubElement(log_entry, "timestamp").text = now.strftime("%Y-%m-%d %H:%M:%S")

        tree = ET.ElementTree(log_entry)
        with open(self.log_path, "ab") as log_file:
            log_file.write(ET.tostring(log_entry) + b"\n")

def read_config(config_path):
    with open(config_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        config = next(reader)
        return config

def process_command(command, vfs, logger, user):
    logger.log_action(user, command)
    if command == 'ls':
        vfs.list_directory()
    elif command.startswith('cd'):
        path = command.split(maxsplit=1)[1] if len(command.split()) > 1 else '/'
        vfs.change_directory(path)
    elif command == 'cal':
        show_calendar()
    elif command.startswith('find'):
        search_name = command.split(maxsplit=1)[1] if len(command.split()) > 1 else ''
        vfs.find(search_name)
    elif command == 'exit':
        print("Exiting...")
        return False
    else:
        print("Not a command")
    return True

if __name__ == '__main__':
    config = read_config('config.csv')
    vfs = VirtualFileSystem(config['file_system_path'])
    logger = Logger(config['log_path'])

    running = True
    while running:
        command = input(f"{config['user']}@{config['hostname']}:~{vfs.current_directory}$ ")
        running = process_command(command, vfs, logger, config['user'])
