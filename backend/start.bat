@echo off
echo Starting Attendance System...

:: Start Backend
start cmd /k "cd C:\projects\attendance_system\backend && python app.py"

:: Wait 3 seconds for backend to start
timeout /t 3

:: Start Flutter
start cmd /k "cd C:\projects\attendance_system\flutter_app\attendance_app && flutter run -d chrome"

echo Both started successfully!