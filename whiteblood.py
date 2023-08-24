import os, psutil, time, subprocess, winreg, socket, servicemanager, win32event, win32service, win32serviceutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WhiteBlood(win32serviceutil.ServiceFramework):
    _svc_name_ = "WhiteBlood"
    _svc_display_name_ = "WhiteBlood"
    _svc_description_ = "Monitoramento de arquivos armadilha"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        arq_folder = 'C:\\arquivos'
        log_folder = os.path.join('C:\\Log')
        if not os.path.exists(arq_folder):
            os.makedirs(arq_folder)
            for i in range(5):
                arq = f"arquivo_{i}.txt"
                filepath = os.path.join(arq_folder, arq)
                with open(filepath, "w") as f:
                    f.write("abc.")
        if not os.path.exists(log_folder):
                        os.makedirs(log_folder)
        class Watcher:
            def __init__(self):
                self.observer = Observer()
            def run(self):
                event_handler = Handler()
                self.observer.schedule(event_handler, path=arq_folder, recursive=True)
                self.observer.start()
                try:
                    while True:
                        time.sleep(0.0000001)
                except:
                    self.observer.stop()
                    print("Error")
                self.observer.join()
        class Handler(FileSystemEventHandler):
            @staticmethod
            def on_key_created(event):
                print(f'Chave do registro criada: {event.KeyName}')
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, event.KeyName)
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'WhiteBlood\\Monitor')
            winreg.CloseKey(key)
            handle = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            winreg.NotifyChangeEventLog(handle, event_callback=on_key_created)
            def on_any_event(event):
                if event.is_directory:
                    return None
                else:
                    process_name = psutil.Process(os.getpid()).name()
                    print(f'Processo: {process_name} capturou o evento {event.event_type} no arquivo {event.src_path}')
                    # Código de log
                    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    with open(os.path.join(log_folder, "log.txt"), "a") as arquivo:
                        arquivo.write(f"{data_hora_atual} - Processo: {process_name} capturou o evento {event.event_type} no arquivo {event.src_path}\n")
                    subprocess.call(["taskkill", "/F", "/IM", f"{process_name}"])
        if __name__ == '__main__':
            w = Watcher()
            w.run()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WhiteBlood)
