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
        # self.setCentralWidget(self.chartView2)
    
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
            QPoint(9, 4),
            QPoint(12, 20),
            QPoint(15, 12),
            QPoint(18, 25),
            QPoint(20,30)
        ]

        series.append(data)
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)

        series2.append(data2)
        chart2 = QChart()
        chart2.legend().hide()
        chart2.addSeries(series2)

        pen = QPen(QColor(200, 200, 200))
        pen.setWidth(5)
        series.setPen(pen)

        pen2 = QPen(QColor(200, 0, 0))
        pen2.setWidth(5)
        series2.setPen(pen2)

        font = QFont('Open Sans')
        font.setPixelSize(40)
        font.setBold(True)
        chart.setTitleFont(font)
        chart.setTitleBrush(QBrush(Qt.yellow))
        chart.setTitle('Custom Chart Demo')

        self.chartView = QChartView(chart)
        self.chartView2 = QChartView(chart2)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    chartDemo = MyChart()
    chartDemo.show()

    sys.exit(app.exec_())