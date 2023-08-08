import win32serviceutil, win32service, win32event, servicemanager, os

user_folder = os.path.expanduser("~")
documents_folder = os.path.join(user_folder, "Documentos")
honeypots_folder = os.path.join(documents_folder, "honeypots")

class WhiteBloodService(FileMonitorHandler, win32serviceutil.ServiceFramework):
    _svc_name_ = "WhiteBlood"
    _svc_display_name_ = "White Blood"
    _svc_description_ = "Monitora um diretório em busca de ransomware usando análise estatística"
    _svc_deps_ = []

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.folder_path = honeypots_folder

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))



# Registrar e instalar o serviço usando a biblioteca pywin32
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WhiteBloodService)
