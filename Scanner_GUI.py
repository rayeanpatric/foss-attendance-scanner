import sys
import cv2
import re
import numpy as np
import gspread
from pyzbar.pyzbar import decode
from PyQt5.QtWidgets import (
    QApplication,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor
from oauth2client.service_account import ServiceAccountCredentials


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOSS Attendance System")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()
        logo = QLabel(self)
        pixmap = QPixmap(r"D:\FOSS Club\FOSS Initiative\Scanner\club_logo.png")  # Your club logo file
        logo.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        layout.addWidget(logo)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")  # Set background to black


        # Timer to switch to the next screen
        QTimer.singleShot(3000, self.go_to_link_input)  # 2 seconds duration

    def go_to_link_input(self):
        self.parentWidget().setCurrentIndex(1)  # Switch to the LinkInputScreen


# Link Input Screen Class
class LinkInputScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOSS Attendance System")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.link_input = QLineEdit(self)
        self.link_input.setPlaceholderText("Enter Google Sheets URL")
        layout.addWidget(self.link_input)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.go_to_scanning_screen)
        layout.addWidget(self.next_button)
        self.setStyleSheet("background-color: black; color: white;")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: 2px solid white;
                border-radius: 15px;  /* Rounded edges */
                padding: 5px 10px;  /* Small padding for the button */
            }
            QPushButton:hover {
                background-color: #c8ad88;  /* Light brown on hover */
            }
        """)

        self.setLayout(layout)

    def go_to_scanning_screen(self):
        self.parentWidget().scanning_screen.set_sheet_url(self.link_input.text().strip())
        self.parentWidget().setCurrentIndex(2)  # Switch to the ScanningScreen


class ScanningScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOSS Attendance System")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.camera_label = QLabel("Camera Screen", self)
        self.camera_label.setFixedSize(600, 300)  # Set a fixed size for the camera label
        layout.addWidget(self.camera_label)

        self.scan_output = QTextEdit(self)
        self.scan_output.setReadOnly(True)
        layout.addWidget(self.scan_output)

        self.capture_button = QPushButton("Capture", self)
        layout.addWidget(self.capture_button)

        self.setLayout(layout)

        # Set up the camera
        self.cap = cv2.VideoCapture(0)

        # Attempt to set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            print("Error: Camera could not be opened.")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(80)  # Update every 30 milliseconds

        self.sheet_url = ""
        self.scanned_data = None  # To hold the scanned QR code data

        # Connect button signal to capture data method
        self.capture_button.clicked.connect(self.capture_data)

    def set_sheet_url(self, url):
        self.sheet_url = url

    def append_data_to_sheet(self, data):
        if not self.sheet_url:
            print("No Google Sheet URL provided.")
            return

        try:
            # Extract the sheet ID from the URL
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', self.sheet_url)
            if not match:
                print("Invalid Google Sheets URL.")
                return
            sheet_id = match.group(1)

            # Use the service account credentials to authenticate
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            client = gspread.authorize(creds)

            # Open the Google Sheet using the sheet ID
            sheet = client.open_by_key(sheet_id).sheet1  # Access the first worksheet

            # Append the data to the Google Sheet
            sheet.append_row(data)
            print(f"Data {data} scanned and appended to Google Sheet.")
        except Exception as e:
            print(f"Error appending data to sheet: {e}")

    def update_frame(self):
        if not self.cap.isOpened():
            print("Error: Camera could not be opened.")
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return

        # Decode QR codes in the frame
        qr_codes = decode(frame)

        # Display the frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_image))

        # Check if a QR code is detected
        if qr_codes:  # If any QR code is detected
            for qr_code in qr_codes:
                self.scanned_data = qr_code.data.decode('utf-8')  # Store the scanned data
                print(f"QR Code Data: {self.scanned_data}")

                # Draw a rectangle around the detected QR code
                points = qr_code.polygon
                if len(points) == 4:
                    pts = [(point.x, point.y) for point in points]
                    pts = np.array(pts, dtype=np.int32)  # Convert to np.array
                    pts = pts.reshape((-1, 1, 2))  # Reshape for polylines
                    cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                # Show the QR code data on the frame
                cv2.putText(frame, self.scanned_data, (pts[0][0][0], pts[0][0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def capture_data(self):
        if self.scanned_data:  # Only append if there is scanned data
            data_list = self.scanned_data.split(", ")
            if len(data_list) == 5:  # Ensure we have all fields
                print(f"Attempting to append data: {data_list}")  # Debugging statement
                self.append_data_to_sheet(data_list)  # Call the method to append data
                self.scan_output.append(self.scanned_data)  # Display scanned data in the text box
                self.scanned_data = None  # Reset after capturing
            else:
                print("Scanned data does not have the correct number of fields.")
        else:
            print("No QR code detected to capture.")

    def closeEvent(self, event):
        self.cap.release()  # Release the camera when the widget is closed
        event.accept()

# Main Application Class
class MainApplication(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOSS Attendance System")

        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
            }
            QPushButton {
                background-color: #444;
                color: white;
            }
            QLineEdit, QTextEdit {
                background-color: #222;
                color: white;
            }
        """)
        
        self.splash_screen = SplashScreen()
        self.link_input_screen = LinkInputScreen()
        self.scanning_screen = ScanningScreen()

        self.addWidget(self.splash_screen)
        self.addWidget(self.link_input_screen)
        self.addWidget(self.scanning_screen)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())
