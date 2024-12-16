# FOSS Attendance System

## Overview
The FOSS Attendance System is a Python-based desktop application designed to streamline attendance management for events. Built using PyQt5 for the GUI and integrated with Google Sheets for data storage, this application allows participants to register and generate QR codes beforehand. Volunteers can scan these QR codes during the event, and attendance is automatically recorded in a linked Google Sheet. This not only reduces manual effort but also ensures accuracy and efficiency in managing attendance records. 🎉📋✨

## Features
- **Splash Screen:** A welcoming screen with a customizable club logo and smooth transitions.
- **Google Sheet Integration:** Attendance data is directly appended to a specified Google Sheet, simplifying the process of maintaining event records.
- **QR Code Scanning:** Real-time QR code detection and decoding using the device's camera to capture participant details.
- **Data Validation:** Ensures all captured QR codes adhere to the expected format, reducing errors and ensuring reliable data entry.
- **Cross-Platform Compatibility:** Designed to run seamlessly on Windows, Linux, and macOS systems.
- **Camera Feed Preview:** Displays a live camera feed, providing visual feedback while scanning QR codes.

---

## Prerequisites

### Software Requirements
- Python 3.8 or higher
- Google Chrome or any modern browser for Google Sheets compatibility 🌐🐍🖥️

### Libraries and Dependencies
Install the required Python libraries using the following command:
```bash
pip install PyQt5 opencv-python pyzbar gspread oauth2client numpy
```
📦📚⚙️

### Google API Credentials
1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/). 🌩️
2. Enable the Google Sheets API and Google Drive API for your project. ✅
3. Create a service account and download the `credentials.json` file. 🔐
4. Place the `credentials.json` file in the same directory as the application. 📁✨

---

## File Structure
- **Scanner_GUI.py:** Main application code that powers the GUI and core functionality.
- **credentials.json:** Google API credentials (required for Google Sheets integration).
- **club_logo.png:** Your club's logo, displayed prominently on the splash screen.
- **README.md:** Documentation for setting up and using the application.
📁📄🛠️

---

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository/foss-attendance-system.git
   cd foss-attendance-system
   ```
   📥📂🚀
2. Ensure all dependencies are installed as per the requirements mentioned above.
3. Place your `club_logo.png` and `credentials.json` files in the project directory.
4. Launch the application using:
   ```bash
   python Scanner_GUI.py
   ```
   🎯📡🖥️

---

## Usage Workflow
1. **Launch the Application:**
   - The application opens with a visually appealing splash screen displaying your club's logo. 🎨👋💻
2. **Enter Google Sheets Link:**
   - Input the URL of the Google Sheet where attendance data will be stored. 🖋️📊📌
3. **QR Code Scanning:**
   - Point the device camera at a participant's QR code. 🎥📷✅
   - The application detects and decodes the QR code in real time, extracting participant details.
4. **Data Capture:**
   - Validated data from the QR code is appended to the linked Google Sheet and displayed in the GUI for verification. 📜📥📄
5. **Exit:**
   - Closing the application releases all resources, including the camera, ensuring a clean exit. 🚪📸✔️

---

## Code Highlights
### Splash Screen
- Displays a customizable club logo with a sleek black background, setting a professional tone for the application. 🌌📷🏢
- Automatically transitions to the next screen after a short delay, enhancing user experience. 🔄💻⏳

### QR Code Scanning
- Uses `opencv-python` and `pyzbar` libraries for efficient and accurate QR code detection and decoding. 📜📸📈
- Live camera feed is processed frame-by-frame to detect QR codes and overlay bounding boxes. 🎥📋📐

### Google Sheets Integration
- Extracts relevant participant details from the scanned QR codes. 🔍📄📝
- Validates and appends the data to the specified Google Sheet using the `gspread` library. 📊📑✔️
- Automatically handles authentication through the provided `credentials.json` file. 🔐🔗📂

---

## Known Issues and Limitations
- Ensure the camera device is functional and accessible; otherwise, the application cannot start. 📷⚠️🚫
- QR codes must strictly follow the expected format (e.g., specific fields separated by commas). 📜✂️✅
- Currently, only the first worksheet in the specified Google Sheet is accessed. 📑📋🛑
- Limited error feedback for invalid Google Sheet URLs or misconfigured credentials. 🌐📉🛠️

---

## Future Enhancements
- Add support for accessing multiple worksheets within the same Google Sheet. 📈📊🔢
- Improve error handling for scenarios such as invalid QR codes, missing fields, or authentication failures. 🛠️🚦⚙️
- Enable offline data storage with the option to synchronize with Google Sheets when connectivity is restored. 📡📤📥
- Integrate participant registration and QR code generation directly into the application, removing the need for external tools. 📝🎟️🔧
- Support for multiple camera devices and dynamic resolution adjustments. 📷📐🔄

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for complete details. 📝⚖️✔️

---

## Contributions
Contributions are welcome and encouraged! Feel free to fork the repository, make your improvements, and submit a pull request. Suggestions for new features, bug fixes, or enhancements are always appreciated. 🌟🛠️🤝

---

## Acknowledgments
- **Google API Team:** For providing robust tools like the Google Sheets API and Drive API. 🌐🔧🎉
- **FOSS Community:** For fostering a culture of collaboration and supporting open-source initiatives. 🤝🌍📖
- **PyQt5 and OpenCV Developers:** For creating powerful libraries that make projects like this possible. 💻📚✨

---

Happy Scanning and Organizing! 🚀🎉📋

