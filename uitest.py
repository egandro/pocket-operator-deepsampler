# python -m pip install pysimplegui
# # https://realpython.com/pysimplegui-python/

# https://datatofish.com/executable-pyinstaller/
# as admin: pip install pyinstaller
# pyinstaller --noconsole --onefile uitest.py

import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()