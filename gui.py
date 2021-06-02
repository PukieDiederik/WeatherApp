import time
import math

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor, QPixmap

# starting every class which is a gui element off with a 'G'

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Quick Overview
        qOverviewWrapper = QWidget()
        qOverviewWrapper.setProperty("depth", 1)
        qOverviewWrapper.setProperty("rounded", True)
        qOverviewWrapper.setGraphicsEffect(getShadowEffect())

        self.weatherIcon = QLabel(qOverviewWrapper)
        self.weatherName = QLabel(qOverviewWrapper, objectName="qoWeatherName")
        self.weatherIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherName.setAlignment(QtCore.Qt.AlignCenter)

        self.currentTemp = QLabel(qOverviewWrapper)
        self.currentTemp.setAlignment(QtCore.Qt.AlignRight)
        tempSplitter     = QLabel("/"              , qOverviewWrapper)
        tempSplitter.setFixedWidth(tempSplitter.fontMetrics().boundingRect(tempSplitter.text()).width())
        self.flTemp      = QLabel(qOverviewWrapper)

        tempSplitter.setProperty("text-color", "alternate")
        self.flTemp .setProperty("text-color", "alternate")

        # Quick Overview - Temperature display
        tempLayout = QHBoxLayout()
        tempLayout.addWidget(self.currentTemp)
        tempLayout.addWidget(tempSplitter)
        tempLayout.addWidget(self.flTemp)
        
        # Quick Overview - Adding everything to a layout
        qoLayout = QVBoxLayout(qOverviewWrapper)
        qoLayout.addWidget(self.weatherIcon)
        qoLayout.addWidget(self.weatherName)
        qoLayout.addLayout(tempLayout)


        # Hourly Overview
        hOverviewWrapper = QWidget()
        hOverviewWrapper.setProperty("depth", 1)
        hOverviewWrapper.setProperty("rounded", True)
        hOverviewWrapper.setGraphicsEffect(getShadowEffect())

        # Hourly Overview - Where the hourlyOverview widgets are located
        hOverviewWidgetsWrapper = QWidget(self, objectName="hOverviewSA")
        hOverviewWidgetsWrapper.setContentsMargins(0,5,0,5)
        self.hOverviewWidgetLayout = QHBoxLayout(hOverviewWidgetsWrapper)

        # Hourly Overview - Scrollable area
        hOverviewSA = QScrollArea()
        hOverviewSA.setVerticalScrollBarPolicy  (QtCore.Qt.ScrollBarAlwaysOff)
        hOverviewSA.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        hOverviewSA.setFrameShape(QtWidgets.QFrame.NoFrame)
        hOverviewSA.setWidget(hOverviewWidgetsWrapper)
        hOverviewSA.setWidgetResizable(True)
        hOverviewSA.setFixedHeight(180)

        # Hourly Overview - Final layout
        hOverviewLayout = QVBoxLayout(hOverviewWrapper)
        hOverviewLayout.addWidget(hOverviewSA)
        hOverviewLayout.setContentsMargins(0,15,0,15)


        # Daily Overview
        dOverviewWrapper = QWidget()
        dOverviewWrapper.setProperty("depth", 1)
        dOverviewWrapper.setProperty("rounded", True)
        dOverviewWrapper.setGraphicsEffect(getShadowEffect())
        self.doLayout = QVBoxLayout(dOverviewWrapper) #Where the dailyOverview widgets are located


        # Other Info
        otherInfoWrapper = QWidget()
        otherInfoWrapper.setProperty("depth", 1)
        otherInfoWrapper.setProperty("rounded", True)
        otherInfoWrapper.setGraphicsEffect(getShadowEffect())
        otherInfoLayout = QVBoxLayout(otherInfoWrapper)

        cloudIcon      = QLabel(self)
        self.cloudPerc = QLabel(self)
        self.uvi       = QLabel(self)

        windIcon           = QLabel(self)
        self.windDirection = QLabel(self)
        self.windSpeed     = QLabel(self)

        # Other Info - setting icons
        cloudIcon.setFixedSize(self.cloudPerc.fontMetrics().height(), self.cloudPerc.fontMetrics().height())
        cloudIcon.setPixmap(QPixmap(getWeatherIcon("04d"))) # Cloud icon
        cloudIcon.setScaledContents(True)
        windIcon.setFixedSize(self.windDirection.fontMetrics().height(), self.windDirection.fontMetrics().height())
        windIcon.setPixmap(QPixmap("Resources/weather_icons/wind.png"))
        windIcon.setScaledContents(True)

        # Other Info - cloud percentage and uvi
        genInfo = QHBoxLayout()
        genInfo.addWidget(cloudIcon)
        genInfo.addWidget(self.cloudPerc)
        genInfo.addWidget(self.uvi)

        windInfo = QHBoxLayout()
        windInfo.addWidget(windIcon)
        windInfo.addWidget(self.windDirection)
        windInfo.addWidget(self.windSpeed)

        # Other Info - adding everything to final layout
        otherInfoLayout.addLayout(genInfo)
        otherInfoLayout.addLayout(windInfo)

        # Overall wrapper
        allLayout = QVBoxLayout(self)
        allLayout.setContentsMargins(0,0,0,0)
        allWrapper = QWidget(objectName="allWrapper")
        allWrapper.setProperty("depth", 0)

        allScrollArea = QScrollArea()
        allScrollArea.setWidget(allWrapper)
        allScrollArea.setWidgetResizable(True)
        allScrollArea.setVerticalScrollBarPolicy  (QtCore.Qt.ScrollBarAlwaysOff)
        allScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        allScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        allLayout.addWidget(allScrollArea)

        # Layout
        layout = QVBoxLayout(allWrapper)
        layout.setSpacing(10)
        layout.addWidget(qOverviewWrapper)
        layout.addWidget(hOverviewWrapper)
        layout.addWidget(dOverviewWrapper)
        layout.addWidget(otherInfoWrapper)

        # Set stuff for the window
        self.setFixedWidth(300) # TODO: needs to be changed to have no fixed width (for phone this should just be able to have fullscreen)
        self.setContentsMargins(0,0,0,0)
        self.setWindowTitle("main window")
        self.setMinimumHeight(500)
        self.show()


    # change values functions
    # - Quick overview
    def setTemperature(self, temp, feelsLike):
        self.flTemp.setText(str(round(feelsLike)) + "°")
        self.currentTemp.setText(str(round(temp)) + "°")

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
        self.uvi.setText(str(round(uvi)) + " UVI")

    def setCloudiness(self, cloudiness):
        self.cloudPerc.setText(str(cloudiness) + "%")

class hourlyOverview(QWidget):
    def __init__(self, parent, wIconName, pop, _time, _temp, _fltemp):
        super().__init__()

        icon          = QLabel(self)

        rainIcon      = QLabel(self)
        pop           = QLabel(str(int(pop * 100)) + "%", self)

        temperature   = QLabel(str(round(_temp)) + "°", self)
        tempSplitter  = QLabel("  /  ", self)
        flTemperature = QLabel(str(round(_fltemp)) + "°", self)

        curTime       = QLabel(str(time.localtime(_time).tm_hour) + ":00", self)

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
        layout.setSpacing(0)
        layout.addWidget(icon)
        layout.addLayout(rainLayout)
        layout.addLayout(tempLayout)
        layout.addWidget(curTime)

        tempSplitter.setProperty ("text-color", "alternate")
        flTemperature.setProperty("text-color", "alternate")
        tempSplitter.setFixedWidth(tempSplitter.fontMetrics().boundingRect(tempSplitter.text()).width())

        pop          .setAlignment(QtCore.Qt.AlignCenter)
        temperature  .setAlignment(QtCore.Qt.AlignRight)
        tempSplitter .setAlignment(QtCore.Qt.AlignHCenter)
        flTemperature.setAlignment(QtCore.Qt.AlignLeft)
        curTime      .setAlignment(QtCore.Qt.AlignCenter)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setProperty("depth", 2)
        self.setProperty("rounded", True)
        self.setGraphicsEffect(getShadowEffect())
        self.show()

class dailyOverview(QWidget):
    def __init__(self, parent, wIconName, _wName, _date, _temp, _flTemp, _pop):
        super().__init__()

        wIcon     = QLabel(self)
        wName     = QLabel(_wName, self)
        
        temp      = QLabel(str(round(_temp))   + "°", self)
        flTemp    = QLabel(str(round(_flTemp)) + "°", self)
        tempSplit = QLabel("  /  ", self)

        popIcon   = QLabel(self)
        pop       = QLabel(str(int(_pop * 100)) + "%", self)

        date      = QLabel(time.strftime("%a %d %b", time.localtime()), self)

        wIcon.setPixmap(getWeatherIcon(wIconName))
        wIcon.setScaledContents(True)
        wIcon.setFixedSize(50, 50)
        popIcon.setPixmap(getWeatherIcon("09d"))
        popIcon.setScaledContents(True)
        popIcon.setFixedSize(pop.size().height(), pop.size().height())

        temp     .setFixedWidth(temp     .fontMetrics().boundingRect(temp     .text()).width() + 2)
        tempSplit.setFixedWidth(tempSplit.fontMetrics().boundingRect(tempSplit.text()).width())
        flTemp   .setFixedWidth(flTemp   .fontMetrics().boundingRect(flTemp   .text()).width() + 2)
        pop      .setFixedWidth(pop      .fontMetrics().boundingRect(pop      .text()).width())

        tempSplit.setProperty("text-color", "alternate")
        flTemp   .setProperty("text-color", "alternate")

        temp     .setAlignment(QtCore.Qt.AlignRight)
        tempSplit.setAlignment(QtCore.Qt.AlignHCenter)
        flTemp   .setAlignment(QtCore.Qt.AlignLeft)
        pop      .setAlignment(QtCore.Qt.AlignCenter)

        #layout stuff
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        lGenInfo    = QVBoxLayout()
        lGenInfo.addWidget(wName)
        lGenInfo.addWidget(date)

        tempPopWrapper = QWidget(self, objectName="doTempPopWrapper")
        tempPopWrapper.setContentsMargins(10,5,10,0)
        lStatsInfo  = QVBoxLayout(tempPopWrapper)
        lStatsInfo.setSpacing(0)
        lStatsInfo.setContentsMargins(0,0,0,0)

        layout.addWidget(wIcon)
        layout.addLayout(lGenInfo)
        layout.addWidget(tempPopWrapper)

        lPop = QHBoxLayout()
        lPop.setAlignment(QtCore.Qt.AlignCenter)
        lPop.addWidget(popIcon)
        lPop.addWidget(pop)        
        
        lTemp = QHBoxLayout()
        lTemp.setAlignment(QtCore.Qt.AlignCenter)
        lTemp.addWidget(temp)
        lTemp.addWidget(tempSplit)
        lTemp.addWidget(flTemp)

        lStatsInfo.addLayout(lTemp)
        lStatsInfo.addLayout(lPop)

        tempPopWrapper.setFixedWidth(temp.size().width() + tempSplit.size().width() + flTemp.size().width() + 20)

        self.setParent(parent)
        self.setProperty("depth", 2)
        self.setProperty("rounded", True)
        self.setGraphicsEffect(getShadowEffect())
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.show()

def getWeatherIcon(iconName: str):
    iconName = iconName.replace("n","d")
    return QPixmap(f"./Resources/weather_icons/{iconName}.png")

def getShadowEffect():
    shadow = QtWidgets.QGraphicsDropShadowEffect()
    shadow.setBlurRadius(5)
    shadow.setColor(QColor(0,0,0,64))
    shadow.setOffset(0, 5)

    return shadow

# this is called when this file is being run
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