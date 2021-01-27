from PyQt5.QtWidgets import (QPlainTextEdit, QMainWindow, QApplication, QPushButton, QLineEdit, qApp)
from PyQt5 import (uic, QtCore, QtGui)
from PyQt5.QtGui import (QIcon, QImage, QPixmap, QIcon)
from PyQt5.QtCore import (Qt, QFile)
import sys, os, requests, json
from datetime import datetime
from os.path import expanduser
from easysettings import EasySettings

try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'pythonexplained.python.weather.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass
#pyinstaller
def resource_path(relative_path):
    """for pyinstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


wea_gui = resource_path("./gui/main.ui")
wea_app = resource_path("./gui/appbg.png")
wea_logo = resource_path("./gui/logo.png")
userfold = expanduser("~")
config = EasySettings(userfold+"/weather.conf")
wea_API = config.get("key")
wea_url = "https://api.openweathermap.org/data/2.5/weather?appid="+wea_API+"&units=metric"
wea_url_ico = "http://openweathermap.org/img/wn/"


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        UIFile = QFile(wea_gui)
        UIFile.open(QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()
        wea_bg = QPixmap(wea_app)
        self.appbg.setPixmap(wea_bg)

        self.wea_get.clicked.connect(self.fetch_temp)



    def fetch_temp(self):
        """Fetches the wanted values from the openweather API"""
        try:
            location = self.wea_qloc.text()
            if location != "":
                complete_url = wea_url + "&q=" + location

                response = requests.get(complete_url)
                print(complete_url)

                x = response.json() 
                if x["cod"] != "404":
                    y = x["main"]
                    ico = x["weather"]

                    temp = y["temp"]
                    wea_icon = ico[0]["icon"]
                    wea_png = wea_url_ico + wea_icon + '@2x.png'

                    wea_time = datetime.now()
                    current_time = wea_time.strftime("%H:%M:%S")

                    self.wea_time.setText(str(current_time))
                    self.wea_temp.setText(str(temp)+'°C')
                    self.wea_loc.setText(str(location))
                    image = QImage()
                    image.loadFromData(requests.get(wea_png).content)
                    self.wea_icon.setPixmap(QPixmap(image))


        except ValueError:
            pass
       
style = '''
QLabel {
    color: #eeeeee;
}
'''

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(wea_logo))
app.setStyleSheet(style)
window = UI()
window.show()
app.exec_()