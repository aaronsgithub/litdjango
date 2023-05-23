import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"Event type: {event.event_type}  path : {event.src_path}")
        print("Running nbdev_export...")
        subprocess.run(["nbdev_export"])


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path="./nbs", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
