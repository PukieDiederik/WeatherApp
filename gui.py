import time

import PyQt5
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QCheckBox, QVBoxLayout, QSizePolicy, QHBoxLayout, QScrollArea
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

# starting every class which is a gui element off with a 'G'
# TODO:
# - implement better stylesheets

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Widgets
        # Quick Overview
        self.weatherIcon = QLabel("Weather Icon", self)
        self.weatherName = QLabel("Weather name", self)

        self.currentTemp = QLabel("Current Temp", self)
        tempSplitter     = QLabel("/", self)
        self.flTemp      = QLabel("Feels like Temp", self)

        # Quick Overview - temperature display
        tempLayout = QHBoxLayout() #for the current temp, splitter and feels like temp
        tempLayout.addWidget(self.currentTemp)
        tempLayout.addWidget(tempSplitter)
        tempLayout.addWidget(self.flTemp)
        

        # Hourly Overview
        self.hOverviewTitle = QLabel("Hourly overview", self)

        hOverviewSA = QScrollArea(self)
        hOverviewSA.setWidgetResizable(True)
        hOverviewSA.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.hOverviewLayout = QHBoxLayout(self)
        self.hOverviewLayout.addWidget(hourlyOverview(main, "01d", .21, 1619877600))

        hOverviewWrapper = QWidget(self)
        hOverviewWrapper.setLayout(self.hOverviewLayout)

        hOverviewSA.setWidget(hOverviewWrapper)
        hOverviewSA.setFixedHeight(hOverviewWrapper.geometry().height() + 5) #TODO figure out this height after fixing everything

        # Layout - Quick Overview
        layout = PyQt5.QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.weatherIcon)
        layout.addWidget(self.weatherName)
        layout.addLayout(tempLayout)

        # Layout - Hourly Overview
        layout.addWidget(self.hOverviewTitle)
        layout.addWidget(hOverviewSA)

        # Set stuff for the window
        self.setFixedWidth(300)
        self.setContentsMargins(0,0,0,0)
        self.setWindowTitle("main window")
        self.show()


    # change values functions
    # - Quick overview
    def setTemperature(self, temp, feelsLike):
        self.flTemp.setText(str(feelsLike) + "°")
        self.currentTemp.setText(str(temp) + "°")

    def setWeatherName(self, name):
        self.weatherName.setText(str(name))

    def setWeatherIcon(self, iconName):
        self.weatherIcon.setPixmap(QPixmap("Resources/weather_icons/" + str(iconName)))

    # - Hourly Overview
    def addHOElement(self, element):
        self.hOverviewLayout.addWidget(element)
    
    def addHOElements(self, elements):
        for e in elements:
            self.hOverviewLayout.addWidget(e)
        
    def removeHOElement(self, index):
        element = self.hOverviewLayout.itemAt(index).widget()
        self.hOverviewLayout.removeWidget(element)
        element.setParent(None)
        del element

    def clearHOElements(self):
        for index in reversed(range(self.hOverviewLayout.count())):
            element = self.hOverviewLayout.itemAt(index).widget()
            self.hOverviewLayout.removeWidget(element)
            element.setParent(None)
            del element


class hourlyOverview(QWidget):
    def __init__(self, parent, wIconName, pop, _time):
        super().__init__()

        icon = QLabel("W Icon", self)
        rainIcon = QLabel("R Icon", self)
        pop = QLabel(str(pop) + "%", self)
        curTime = QLabel(str(time.localtime(_time).tm_hour) + ":00", self)

        icon.setFixedSize(70,70)
        icon.setPixmap(QPixmap(f"./Resources/weather_icons/{wIconName}.png"))
        icon.setScaledContents(True)
        

        rainIcon.setFixedSize(pop.size().height(), pop.size().height())
        rainIcon.setPixmap(QPixmap("./Resources/weather_icons/09d.png"))
        rainIcon.setScaledContents(True)
        rainLayout = QHBoxLayout()
        rainLayout.addWidget(rainIcon)
        rainLayout.addWidget(pop)


        layout = QVBoxLayout(self)
        layout.addWidget(icon)
        layout.addLayout(rainLayout)
        layout.addWidget(curTime)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.setStyleSheet("border: 1px solid white; background-color: #0a142e; color: white;")
        self.setFixedWidth(70)
        self.show()


def main():
    app = QApplication([])
    #gOverview = GOverviewQuick(None)
    #Gprecipitation = GprecipitationGraph()
    main = WeatherApp()
    main.setContentsMargins(0,0,0,0)
    app.setStyleSheet(open("./Resources/stylesheets/WeatherApp.css").read())
    #for testing purposes
    main.setTemperature(16, 16) 
    main.setWeatherName("light rain")
    main.setWeatherIcon("10d")
    main.addHOElements([hourlyOverview(main, "01d", .21, 1619877600) for i in range(10)])
    app.exec_()

if __name__ == '__main__':
    main()
