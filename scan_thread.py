import subprocess
from PyQt5 import QtCore

log_directory = "C:\\Users\\corey\\PycharmProjects\\pythonProject3\\log"


class ScanThread(QtCore.QThread):
    ping_scan_completed = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.data = None

    def set_data(self, data):
        self.data = data

    # Function to perform the ping scan
    def perform_ping_scan(self):
        try:
            if not self.data:
                print("Ping scan failed. No data provided.")
                return 'Error'

            print("Ping scan started.")
            xml_file = f"{log_directory}/ping.xml"  # Include the file name in the path

            command = ['nmap', '-T4', '--packet-trace', '--disable-arp-ping',
                       '-oX', xml_file, '10.0.0.1/24']

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            process.wait()

            # Emit signal with the scan results (previously it emitted the XML file name)
            self.ping_scan_completed.emit([xml_file])
            print("Ping scan finished.")

        except Exception as e:
            print("Ping scan failed.")
            print(str(e))
            return 'Error'
