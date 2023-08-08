import os, psutil, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


user_folder = os.path.expanduser("~")
documents_folder = os.path.join(user_folder, "Documentos")
honeypots_folder = os.path.join(documents_folder, "honeypots")


if not os.path.exists(honeypots_folder):
    os.makedirs(honeypots_folder)
    for i in range(5):
        arq = f"arquivo_{i}.txt"
        filepath = os.path.join(honeypots_folder, arq)
        with open(filepath, "w") as f:
            f.write("Este é um arquivo de texto genérico.")


def kill_process(process_name):
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                parent = psutil.Process(proc.pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.kill()
                parent.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, path=honeypots_folder, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            process_name = psutil.Process(os.getpid()).name()
            process_pid = os.getpid()
            print(f'Processo: {process_name} (PID: {process_pid}) modificou o arquivo {event.src_path}')
            kill_process(process_name)

if __name__ == '__main__':
    w = Watcher()
    w.run()