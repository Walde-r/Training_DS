import PySimpleGUI as sg
layout = [[sg.Text("Привет, мир!")], [sg.Button("OK")]]
window = sg.Window("Пример PySimpleGUI", layout)
event, values = window.read()
window.close()