import time
import math
import locale

import PyQt5
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QLabel, QWidget, QCheckBox, QVBoxLayout, QSizePolicy, QHBoxLayout, QScrollArea
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QMargins, Qt
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

        self.hOverviewWidgetLayout = QHBoxLayout(self)
        self.hOverviewWidgetLayout.addWidget(hourlyOverview(main, "01d", .21, 1619877600, 20, 21))

        hOverviewSAWrapper = QWidget(self)
        hOverviewSAWrapper.setLayout(self.hOverviewWidgetLayout)
        hOverviewSAWrapper.setObjectName("hOverviewSA")

        hOverviewSA = QScrollArea(self)
        hOverviewSA.setWidgetResizable(True)
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

        cloudIcon.setFixedSize(self.cloudPerc.fontMetrics().height(), self.cloudPerc.fontMetrics().height())
        cloudIcon.setPixmap(QPixmap(getWeatherIcon("04d")))
        cloudIcon.setScaledContents(True)
        windIcon.setFixedSize(self.windDirection.fontMetrics().height(), self.windDirection.fontMetrics().height())
        windIcon.setPixmap(QPixmap("Resources/weather_icons/wind.png"))
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
        tempSplitter.setFixedWidth(tempSplitter.fontMetrics().boundingRect(tempSplitter.text()).width())

        # Styling - Hourly Overview
        hOverviewLayout.setContentsMargins(0,15,0,15)
        hOverviewSAWrapper.setContentsMargins(0,5,0,5)
        hOverviewSA.setVerticalScrollBarPolicy  (Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        hOverviewSA.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        hOverviewSA.setFrameShape(QtWidgets.QFrame.NoFrame)

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
        self.weatherIcon.setPixmap(getWeatherIcon(iconName))

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
        windDirections = ["North", "North East", "East", "South East", "South", "South West", "West", "North West"]
        self.windDirection.setText(windDirections[math.floor((windDirection + 22.5) / 45)])
        self.windSpeed.setText(str(round(windSpeed * 3.6, 1)) + " km/h")

    def setUVI(self, uvi):
        self.uvi.setText(str(uvi) + " UVI")

    def setCloudiness(self, cloudiness):
        self.cloudPerc.setText(str(cloudiness * 100) + "%")

class hourlyOverview(QWidget):
    def __init__(self, parent, wIconName, pop, _time, _temp, _fltemp):
        super().__init__()

        icon = QLabel("W Icon", self)
        rainIcon = QLabel("R Icon", self)
        pop = QLabel(str(int(pop * 100)) + "%", self)
        temperature = QLabel(str(_temp) + "°", self)
        tempSplitter = QLabel("  /  ", self)
        flTemperature = QLabel(str(_fltemp) + "°", self)
        curTime = QLabel(str(time.localtime(_time).tm_hour) + ":00", self)

        icon.setFixedSize(70,70)
        icon.setPixmap(getWeatherIcon(wIconName))
        icon.setScaledContents(True)

        rainIcon.setFixedSize(pop.size().height(), pop.size().height())
        rainIcon.setPixmap(getWeatherIcon("09d"))
        rainIcon.setScaledContents(True)
        rainLayout = QHBoxLayout()
        rainLayout.addWidget(rainIcon)
        rainLayout.addWidget(pop)

        tempLayout = QHBoxLayout()
        tempLayout.addWidget(temperature)
        tempLayout.addWidget(tempSplitter)
        tempLayout.addWidget(flTemperature)

        layout = QVBoxLayout(self)
        layout.addWidget(icon)
        layout.addLayout(rainLayout)
        layout.addLayout(tempLayout)
        layout.addWidget(curTime)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setColor(QColor(0,0,0,64))
        shadow.setOffset(0, 5)

        self.setGraphicsEffect(shadow)

        # Styling
        tempSplitter.setProperty("css-class", "text-light-gray")
        flTemperature.setProperty("css-class", "text-light-gray")
        tempSplitter.setFixedWidth(tempSplitter.fontMetrics().boundingRect(tempSplitter.text()).width())

        layout.setSpacing(0)
        pop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temperature.setAlignment(Qt.AlignmentFlag.AlignRight)
        tempSplitter.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        flTemperature.setAlignment(Qt.AlignmentFlag.AlignLeft)
        curTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.show()

class dailyOverview(QWidget):
    def __init__(self, parent, wIconName, _wName, _date, _temp, _flTemp, _pop):
        super().__init__()

        self.setParent(parent)

        wIcon     = QLabel("wIcon"      , self)
        wName     = QLabel(_wName      , self)
        __time = time.localtime()
        date      = QLabel(time.strftime("%a %d %b", __time), self)
        temp      = QLabel(str(_temp) + "°", self)
        tempSplit = QLabel("  /  "          , self)
        flTemp    = QLabel(str(_flTemp) + "°", self)
        popIcon   = QLabel("pop Icon"   , self)
        pop       = QLabel(str(int(_pop * 100)) + "%", self)

        wIcon.setPixmap(getWeatherIcon(wIconName))
        wIcon.setScaledContents(True)
        wIcon.setFixedSize(50, 50)
        popIcon.setPixmap(getWeatherIcon("09d"))
        popIcon.setScaledContents(True)
        popIcon.setFixedSize(pop.size().height(), pop.size().height())

        temp.setFixedWidth(temp.fontMetrics().boundingRect(temp.text()).width() + 2)
        tempSplit.setFixedWidth(tempSplit.fontMetrics().boundingRect(tempSplit.text()).width())
        flTemp.setFixedWidth(flTemp.fontMetrics().boundingRect(flTemp.text()).width() + 2)
        pop.setFixedWidth(pop.fontMetrics().boundingRect(pop.text()).width())
        tempSplit.setProperty("css-class", "text-light-gray")
        flTemp.setProperty("css-class", "text-light-gray")
        temp.setAlignment(Qt.AlignmentFlag.AlignRight)
        tempSplit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        flTemp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #layout stuff
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        tempPopWrapper = QWidget(self)
        tempPopWrapper.setObjectName("doTempPopWrapper")
        tempPopWrapper.setContentsMargins(10,5,10,0)
        lGenInfo    = QVBoxLayout()
        lStatsInfo  = QVBoxLayout()
        lStatsInfo.setSpacing(0)
        lStatsInfo.setContentsMargins(0,0,0,0)
        lTemp = QHBoxLayout()
        lPop = QHBoxLayout()
        lTemp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lPop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lGenInfo.addWidget(wName)
        lGenInfo.addWidget(date)
        
        lTemp.addWidget(temp)
        lTemp.addWidget(tempSplit)
        lTemp.addWidget(flTemp)

        lPop.addWidget(popIcon)
        lPop.addWidget(pop)

        lStatsInfo.addLayout(lTemp)
        lStatsInfo.addLayout(lPop)
        tempPopWrapper.setLayout(lStatsInfo)
        tempPopWrapper.setFixedWidth(temp.size().width() + tempSplit.size().width() + flTemp.size().width() + 20)

        layout.addWidget(wIcon)
        layout.addLayout(lGenInfo)
        layout.addWidget(tempPopWrapper)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setColor(QColor(0,0,0,64))
        shadow.setOffset(0, 5)

        self.setGraphicsEffect(shadow)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.show()

def getWeatherIcon(iconName: str):
    iconName = iconName.replace("n","d")
    return QPixmap(f"./Resources/weather_icons/{iconName}.png")


def main():
    app = QApplication([])
    main = WeatherApp()
    app.setStyleSheet(open("./Resources/stylesheets/WeatherApp.css").read())
    #for testing purposes
    main.setTemperature(16, 16) 
    main.setWeatherName("heavy shower rain and drizzle")
    main.setWeatherIcon("10d")
    main.addHOElements([hourlyOverview(main, "01n", .21, 1619877600, 20, 21) for i in range(12)])
    main.addDOElements([dailyOverview(main, "09d", "Clouds", 1619802000, 16, 15, .23) for i in range(3)])
    
    main.setWind(50, 6.3)
    main.setUVI(2.5)
    main.setCloudiness(.24)

    app.exec_()
    

if __name__ == '__main__':
    main()
