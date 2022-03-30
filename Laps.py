import sys, os, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, laps):
        self.laps = laps

    def on_modified(self, event):
        #print(f'Event type: {event.event_type}  path : {event.src_path}')

        if event.src_path == self.laps.out_path:
            print("[LAPS] " + self.laps.computer_name + " password retrieved")
            time.sleep(0.2)
            f = open(self.laps.out_path, "r")
            print(f.readlines())
            self.laps.set_password(f.readline())
            f.close()
            self.laps.observer.stop()
        

class LAPS():
    def __init__(self):
        self.password = None
        self.in_path = "C:/temp/in.laps"
        self.out_path = "C:/temp/out.laps"
        self.event_handler = MyHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path='C:/temp/', recursive=False)
        self.observer.start()


    def start(self, computer_name):
        self.computer_name = computer_name
        f = open(self.in_path, "w")
        f.write(self.computer_name)
        f.close()
        print("[LAPS] " + self.computer_name + " password requested")
    
    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password
