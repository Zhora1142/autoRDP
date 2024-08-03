import tkinter
from tkinter import messagebox
from pywinauto.application import Application
from PgIL import Image
from pystray import MenuItem as item
import pystray
import pyperclip
import re


def connect(host, user, password):
    app = Application(backend='uia').start("mstsc.exe")

    dlg = app.window(title_re="Подключение к удаленному рабочему столу")

    dlg.child_window(auto_id="5017", control_type="ToolBar").child_window(control_type="Button").click()
    dlg.child_window(auto_id="13050", control_type="Edit").set_text(host)
    dlg.child_window(auto_id="13064", control_type="Edit").set_text(user)
    dlg.child_window(auto_id="1", control_type="Button").click()

    dlg2 = dlg.child_window(control_type="Window")
    dlg2.child_window(auto_id="PasswordField_2", control_type="Edit").set_text(password)
    dlg2.child_window(auto_id="OkButton", control_type="Button").click()

    try:
        dlg3 = dlg.child_window(title="Подключение к удаленному рабочему столу", control_type="Window")
        dlg3.child_window(title="Да", auto_id="14004", control_type="Button").click()
    except:
        pass


def try_connect(icon: pystray.Icon, item_):
    buffer = pyperclip.paste().replace('\r', '')
    pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}(:\d{1,5})?\n\w+\n\w+$')
    if bool(pattern.match(buffer)):
        host, user, password = buffer.split('\n')

        try:
            connect(host, user, password)
        except:
            root = tkinter.Tk()
            root.wm_attributes("-topmost", 1)
            root.withdraw()
            messagebox.showerror(title='AutoRDP', message=f'Не удалось выполнить подключение', parent=root)
    else:
        root = tkinter.Tk()
        root.wm_attributes("-topmost", 1)
        root.withdraw()
        messagebox.showerror(title='AutoRDP', message=f'Данные сервера в буфере обмена не соответствуют формату', parent=root)


def close_app(icon: pystray.Icon, item_):
    icon.stop()


def main():
    menu = (item('Подключиться', try_connect), item('Закрыть', close_app))

    icon = pystray.Icon("AutoRDP")
    icon.icon = Image.open('icon.png')
    icon.title = "AutoRDP"
    icon.menu = menu

    icon.run()


if __name__ == '__main__':
    main()
