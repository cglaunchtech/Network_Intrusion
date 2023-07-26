import datetime
import threading
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTextEdit

import xml.etree.ElementTree as ET

import scan_thread
from page_handler import PageWindow

log_directory = "/home/dhara-it/Projects/Network-Detection/log"


class Dashboard(PageWindow):
    def __init__(self, home):
        super(Dashboard, self).__init__()
        self.table = None
        uic.loadUi('dashboard.ui', self)

        self.home = home

        self.data.mousePressEvent = lambda event: self.goto_page('data')
        self.startBtn.clicked.connect(self.start_scan)
        self.stopBtn.clicked.connect(self.stop_scan)

        self.pingTable = self.findChild(QTextEdit, 'table1')
        self.pingTable.setReadOnly(True)  # Make the QTextEdit widget read-only

        self.scan_threads = []

    def closeEvent(self, event):
        # Stop the scan thread and wait for it to finish before closing the GUI
        if scan_thread in self.scan_threads:
            scan_thread.quit()
            scan_thread.wait()

    def goto_page(self, event):
        self.goto(event)

    # Function to update the ping table widget with scan results
    def update_ping_table(self, results):
        print("Updating ping table:", results)

        text = ""
        for xml_file in results:
            time.sleep(0.5)

            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for host in root.findall(".//host"):
                    starttime = datetime.datetime.fromtimestamp(int(host.get("starttime"))).strftime(
                        "%Y-%m-%d %H:%M:%S")
                    endtime = datetime.datetime.fromtimestamp(int(host.get("endtime"))).strftime("%Y-%m-%d %H:%M:%S")
                    text += f"Start Time: {starttime}\n"
                    text += f"End Time: {endtime}\n"

                    status = host.find("status")
                    state = status.get("state")
                    reason = status.get("reason")
                    reason_ttl = status.get("reason_ttl")
                    text += f"Status: {state}\n"
                    text += f"Reason: {reason}\n"
                    text += f"Reason TTL: {reason_ttl}\n"

                    for address in host.findall("address"):
                        addr = address.get("addr")
                        addrtype = address.get("addrtype")
                        text += f"{addrtype.capitalize()} Address: {addr}\n"

                        vendor = address.get("vendor")
                        if vendor:
                            text += f"Vendor: {vendor}\n"

                    for hostname in host.findall("hostnames/hostname"):
                        name = hostname.get("name")
                        text += f"Hostname: {name}\n"

                    ports = host.find("ports")
                    if ports is not None:
                        extraports = ports.find("extraports")
                        if extraports is not None:
                            extraports_state = extraports.get("state")
                            extraports_count = extraports.get("count")
                            text += f"Extraports State: {extraports_state}\n"
                            text += f"Extraports Count: {extraports_count}\n"

                        for port in ports.findall("port"):
                            protocol = port.get("protocol")
                            portid = port.get("portid")
                            text += f"Protocol: {protocol}\n"
                            text += f"Port ID: {portid}\n"

                            state = port.find("state")
                            state_state = state.get("state")
                            state_reason = state.get("reason")
                            text += f"State: {state_state}\n"
                            text += f"State Reason: {state_reason}\n"

                            service = port.find("service")
                            service_name = service.get("name")
                            service_method = service.get("method")
                            text += f"Service Name: {service_name}\n"
                            text += f"Service Method: {service_method}\n"

                    times = host.find("times")
                    if times is not None:
                        srtt = times.get("srtt")
                        rttvar = times.get("rttvar")
                        to = times.get("to")
                        text += f"SRTT: {srtt}\n"
                        text += f"RTTVAR: {rttvar}\n"
                        text += f"To: {to}\n"

                    text += "\n"

            except Exception as e:
                print(f"Error parsing XML file: {xml_file}")
                print(str(e))

        self.pingTable.setPlainText(text)

    def handle_ping_scan_completed(self, results):
        if results:  # Check if there are any results before updating the table
            self.update_ping_table(results)

    def start_scan(self):
        if self.scan_threads:
            print("Scan is already in progress.")
            return

        print("Start scan button clicked")

        self.stop_flag = False

        def run_scans():
            ping_scan_thread = scan_thread.ScanThread()
            self.scan_threads.append(ping_scan_thread)

            ping_scan_thread.ping_scan_completed.connect(self.handle_ping_scan_completed)
            ping_scan_thread.set_data([log_directory])

            ping_scan_thread.perform_ping_scan()

        threading.Thread(target=run_scans).start()

    def stop_scan(self):
        print("Stop scan button clicked")
        self.stop_flag = True


if __name__ == "__main__":
    import sys

    # Create the main application
    app = QApplication(sys.argv)

    # Create an instance of the Dashboard
    dashboard = Dashboard(None)

    # Show the Dashboard window
    dashboard.show()

    dashboard.start_scan()

    # Run the application event loop
    sys.exit(app.exec_())
