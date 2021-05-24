import time
import math

import PyQt5
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QLabel, QWidget, QCheckBox, QVBoxLayout, QSizePolicy, QHBoxLayout, QScrollArea
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap

# starting every class which is a gui element off with a 'G'

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Widgets
        # Quick Overview
        qOverviewWrapper = QWidget(self)
        qOverviewWrapper.setProperty("css-class", "wrapper")
        qoLayout = QVBoxLayout()

        self.weatherIcon = QLabel("Weather Icon", qOverviewWrapper)
        self.weatherIcon.setObjectName("qoWeatherIcon")
        self.weatherName = QLabel("Weather name", qOverviewWrapper)
        self.weatherName.setObjectName("qoWeatherName")

        self.currentTemp = QLabel("Current Temp", qOverviewWrapper)
        tempSplitter     = QLabel("/", qOverviewWrapper)
        self.flTemp      = QLabel("Feels like Temp", qOverviewWrapper)

        tempSplitter.setProperty("css-class", "text-light-gray")
        self.flTemp .setProperty("css-class", "text-light-gray")

        # Quick Overview - temperature display
        tempLayout = QHBoxLayout() #for the current temp, splitter and feels like temp
        tempLayout.addWidget(self.currentTemp)
        tempLayout.addWidget(tempSplitter)
        tempLayout.addWidget(self.flTemp)
        
        # Quick Overview - adding everything to wrapper
        qoLayout.addWidget(self.weatherIcon)
        qoLayout.addWidget(self.weatherName)
        qoLayout.addLayout(tempLayout)

        qOverviewWrapper.setLayout(qoLayout)

        # Hourly Overview
        hOverviewWrapper = QWidget(self)
        hOverviewWrapper.setProperty("css-class", "wrapper")
        hOverviewLayout = QVBoxLayout()


        hOverviewSA = QScrollArea(self)
        hOverviewSA.setWidgetResizable(True)
        hOverviewSA.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.hOverviewWidgetLayout = QHBoxLayout(self)
        self.hOverviewWidgetLayout.addWidget(hourlyOverview(main, "01d", .21, 1619877600, 20))

        hOverviewSAWrapper = QWidget(self)
        hOverviewSAWrapper.setLayout(self.hOverviewWidgetLayout)

        hOverviewSA.setWidget(hOverviewSAWrapper)
        hOverviewSA.setFixedHeight(hOverviewSAWrapper.geometry().height() + 20) #TODO figure out this height after fixing everything

        hOverviewLayout.addWidget(hOverviewSA)
        hOverviewWrapper.setLayout(hOverviewLayout)

        # Daily overview
        dOverviewWrapper = QWidget(self)
        dOverviewWrapper.setProperty("css-class", "wrapper")
        self.doLayout = QVBoxLayout()
        dOverviewWrapper.setLayout(self.doLayout)

        # Other info
        otherInfoWrapper = QWidget()
        otherInfoWrapper.setProperty("css-class", "wrapper")
        otherInfoLayout = QVBoxLayout()

        cloudIcon = QLabel("cloudI", self)
        self.cloudPerc = QLabel("cloud%", self)
        self.uvi       = QLabel("uvi%", self)

        windIcon  = QLabel("windIcon", self)
        self.windDirection  = QLabel("WINDDIR", self)
        self.windSpeed  = QLabel("WINDSPEED", self)

        cloudIcon.setPixmap(QPixmap("insert image here"))
        cloudIcon.setScaledContents(True)
        windIcon.setPixmap(QPixmap("insert image here"))
        windIcon.setScaledContents(True)

        genInfo = QHBoxLayout()
        genInfo.addWidget(cloudIcon)
        genInfo.addWidget(self.cloudPerc)
        genInfo.addWidget(self.uvi)

        windInfo = QHBoxLayout()
        windInfo.addWidget(windIcon)
        windInfo.addWidget(self.windDirection)
        windInfo.addWidget(self.windSpeed)

        otherInfoLayout.addLayout(genInfo)
        otherInfoLayout.addLayout(windInfo)
        otherInfoWrapper.setLayout(otherInfoLayout)


        # Styling - Quick Overview
        self.weatherIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weatherName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.currentTemp.setAlignment(Qt.AlignmentFlag.AlignRight)
        tempSplitter.setFixedWidth(20) #set this number because it looked right

        # Styling - Applying dropshadows
        for x in [qOverviewWrapper, hOverviewWrapper, dOverviewWrapper, otherInfoWrapper]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            shadow.setColor(QColor(0,0,0,64))
            shadow.setOffset(0, 5)

            x.setGraphicsEffect(shadow)


        # Layout
        layout = PyQt5.QtWidgets.QVBoxLayout(self)
        layout.setSpacing(10)

        # Layout - Quick Overview
        layout.addWidget(qOverviewWrapper)

        # Layout - Hourly Overview
        layout.addWidget(hOverviewWrapper)

        # Layout - Daily overview
        layout.addWidget(dOverviewWrapper)

        # Layout - Other info
        layout.addWidget(otherInfoWrapper)

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
        self.hOverviewWidgetLayout.addWidget(element)
    
    def addHOElements(self, elements):
        for e in elements:
            self.hOverviewWidgetLayout.addWidget(e)
        
    def removeHOElement(self, index):
        element = self.hOverviewWidgetLayout.itemAt(index).widget()
        self.hOverviewWidgetLayout.removeWidget(element)
        element.setParent(None)
        del element

    def clearHOElements(self):
        for index in reversed(range(self.hOverviewWidgetLayout.count())):
            element = self.hOverviewWidgetLayout.itemAt(index).widget()
            self.hOverviewWidgetLayout.removeWidget(element)
            element.setParent(None)
            del element

    # - Daily Overview
    def addDOElement(self, element):
        self.doLayout.addWidget(element)

    def addDOElements(self, elements):
        for e in elements:
            self.doLayout.addWidget(e)

    def removeDOElement(self, index):
        element = self.doLayout.itemAt(index).widget()
        self.doLayout.removeWidget(element)
        element.setParent(None)
        del element

    def clearDOElements(self):
        for index in reversed(range(self.doLayout.count())):
            element = self.doLayout.itemAt(index).widget()
            self.doLayout.removeWidget(element)
            element.setParent(None)
            del element

    # - Other Info
    def setWind(self, windDirection, windSpeed):
        #modify windDirection from degrees to text:
        windDirections = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        self.windDirection.setText(windDirections[math.floor((windDirection + 22.5) / 45)])
        self.windSpeed.setText(str(round(windSpeed * 3.6, 1)) + " km/h")

    def setUVI(self, uvi):
        self.uvi.setText(str(uvi) + " UVI")

    def setCloudiness(self, cloudiness):
        self.cloudPerc.setText(str(cloudiness * 100) + "%")

class hourlyOverview(QWidget):
    def __init__(self, parent, wIconName, pop, _time, _temperature):
        super().__init__()

        icon = QLabel("W Icon", self)
        rainIcon = QLabel("R Icon", self)
        pop = QLabel(str(int(pop * 100)) + "%", self)
        temperature = QLabel(str(_temperature) + "°", self)
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
        layout.addWidget(temperature)
        layout.addWidget(curTime)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setFixedWidth(70)
        self.show()

class dailyOverview(QWidget):
    def __init__(self, parent, wIconName, _wName, _date, _temp, _flTemp, _pop):
        super().__init__()

        self.setParent(parent)

        wIcon     = QLabel("wIcon"      , self)
        wName     = QLabel(_wName      , self)
        date      = QLabel(time.strftime("%a %d %b", time.localtime(_date)), self)
        temp      = QLabel(str(_temp) + "°", self)
        tempSplit = QLabel("/"          , self)
        flTemp    = QLabel(str(_flTemp) + "°", self)
        popIcon   = QLabel("pop Icon"   , self)
        pop       = QLabel(str(int(_pop * 100)) + "%", self)

        wIcon.setPixmap(QPixmap(f"./Resources/weather_icons/{wIconName}.png"))
        wIcon.setScaledContents(True)
        popIcon.setPixmap(QPixmap("./Resources/weather_icons/09d.png"))
        popIcon.setScaledContents(True)

        #layout stuff
        layout = QHBoxLayout(self)
        lGenInfo    = QVBoxLayout()
        lStatsInfo  = QVBoxLayout()
        lTemp = QHBoxLayout()
        lPop = QHBoxLayout()
        
        lGenInfo.addWidget(wName)
        lGenInfo.addWidget(date)
        
        lTemp.addWidget(temp)
        lTemp.addWidget(tempSplit)
        lTemp.addWidget(flTemp)

        lPop.addWidget(popIcon)
        lPop.addWidget(pop)

        lStatsInfo.addLayout(lTemp)
        lStatsInfo.addLayout(lPop)

        layout.addWidget(wIcon)
        layout.addLayout(lGenInfo)
        layout.addLayout(lStatsInfo)

        self.setFixedHeight(70)
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
    main.addHOElements([hourlyOverview(main, "01d", .21, 1619877600, 20) for i in range(12)])
    main.addDOElements([dailyOverview(main, "09d", "mildly cloudy", 1619802000, 16, 15, .23) for i in range(3)])
    
    main.setWind(50, 6.3)
    main.setUVI(2.5)
    main.setCloudiness(.24)
    
    app.exec_()
    

if __name__ == '__main__':
    main()
