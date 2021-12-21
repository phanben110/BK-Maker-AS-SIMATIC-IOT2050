import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QLineSeries, QChart, QChartView, QCategoryAxis
from PyQt5.QtCore import QPoint
from PyQt5.Qt import QPen, QFont, Qt, QSize
from PyQt5.QtGui import QColor, QBrush, QLinearGradient, QGradient, QPainter

class MyChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chart Formatting Demo')
        self.resize(1200, 800)

        self.initChart()

        self.setCentralWidget(self.chartView)

    def initChart(self):
        series = QLineSeries()
        series2 = QLineSeries()
        data = [
            QPoint(0, 6),
            QPoint(9, 4),
            QPoint(15, 20),
            QPoint(18, 12),
            QPoint(28, 25),
            QPoint(35,30)
        ]

        data2 = [
            QPoint(10, 6),
            QPoint(10, 4),
            QPoint(10, 20),
            QPoint(10, 12),
            QPoint(10, 25),
            QPoint(10,30)
        ]

        series.append(data)

        # creating chart object
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)

        series2.append(data2)
        setpoint = QChart ()
        setpoint.legend().hide()
        setpoint.addSeries(series2)


        pen = QPen(QColor(200, 200, 200))
        pen.setWidth(5)
        series.setPen(pen)

        pen2 = QPen(QColor(200,0, 0))
        pen2.setWidth(5)
        series2.setPen(pen2)


        font = QFont('Open Sans')
        font.setPixelSize(40)
        font.setBold(True)
        chart.setTitleFont(font)
        chart.setTitleBrush(QBrush(Qt.yellow))
        chart.setTitle('Custom Chart Demo')

        # setpoint.setTitleFont(font)
        # setpoint.setTitleBrush(QBrush(Qt.yellow))
        # setpoint.setTitle('Custom Chart Demo')       


        backgroundGradient = QLinearGradient()
        backgroundGradient.setStart(QPoint(0, 0))
        backgroundGradient.setFinalStop(QPoint(0, 1))
        backgroundGradient.setColorAt(0.0, QColor(175, 201, 182))
        backgroundGradient.setColorAt(1.0, QColor(51, 105, 66))
        backgroundGradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        chart.setBackgroundBrush(backgroundGradient)


        plotAreaGraident = QLinearGradient()
        plotAreaGraident.setStart(QPoint(0, 1))
        plotAreaGraident.setFinalStop(QPoint(1, 0))
        plotAreaGraident.setColorAt(0.0, QColor(222, 222, 222))
        plotAreaGraident.setColorAt(1.0, QColor(51, 105, 66))
        plotAreaGraident.setCoordinateMode(QGradient.ObjectBoundingMode)
        chart.setPlotAreaBackgroundBrush(plotAreaGraident)
        chart.setPlotAreaBackgroundVisible(True)
        setpoint.setPlotAreaBackgroundVisible(True)
        # customize axis
        axisX = QCategoryAxis()
        axisY = QCategoryAxis()

        labelFont = QFont('Open Sans')
        labelFont.setPixelSize(25)

        axisX.setLabelsFont(labelFont)
        axisY.setLabelsFont(labelFont)

        axisPen = QPen(Qt.white)
        axisPen.setWidth(2)

        axisX.setLinePen(axisPen)
        axisY.setLinePen(axisPen)   

        axixBrush = QBrush(Qt.white)
        axisX.setLabelsBrush(axixBrush)
        axisY.setLabelsBrush(axixBrush)

        axisX.setRange(0, 30)
        axisX.append('low', 10)
        axisX.append('medium', 20)
        axisX.append('high', 30)

        axisY.setRange(0, 30)
        axisY.append('slow', 10)
        axisY.append('average', 20)
        axisY.append('fast', 30)

        axisX.setGridLineVisible(False)
        axisY.setGridLineVisible(False)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        series.attachAxis(axisX)
        series.attachAxis(axisY)

        self.chartView = QChartView(chart)
        self.chartView2 = QChartView(setpoint)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView2.setRenderHint(QPainter.Antialiasing)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    chartDemo = MyChart()
    chartDemo.show()

    sys.exit(app.exec_())