import pymysql.cursors, PyQt5
from PyQt5.QtWidgets import QTableWidgetItem
from window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

ui.tableWidget.setSortingEnabled(True)
ui.spinBox.setMinimum(1)

# ПОДКЛЮЧЕНИЕ К БД #
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='sadgirl18',
                             db='Учет_средств',
                             charset='utf8mb4')
with connection.cursor() as cursor:
    cursor.execute("""show tables""")
    a = cursor.fetchall()

# СОЗДАНИЕ ВЫПАДАЮЩЕГО СПИСКА #
i = 0
while i != len(a):
    b = str(a[i])
    c = b[2:]
    d = len(c)
    c = c[:len(c)-3]
    c = str(c)
    ui.comboBox.addItem(c)
    i += 1

# ОТОБРАЖЕНИЕ ШАПКИ ТАБЛИЦЫ #
def showTableName():
    a = ui.comboBox.currentText()
    with connection.cursor() as cursor:
        cursor.execute("""SHOW COLUMNS FROM """ + str(a))
        b = cursor.fetchall()
    i = 0
    c =[]
    x = len(b)
    while i != x:
        c.append(str(b[i][0]))
        i += 1
    return c

# ПОКАЗ НИЖНЕЙ ТАБЛИЦЫ ДЛЯ ВВОДА НОВЫХ ДАННЫХ #
def addTable():
    c = showTableName()
    if c[0] == 'Номер_роли' or c[0] == 'Код_местоположения_СЗИ' or c[0] == 'Код_сотрудника' or c[0] == 'Код_типа_обновления' or c[0] == 'Код_типа_ремонта' or c[0] == 'Код_типа_решения' or c[0] == 'Код_типа_СЗИ':
        c.pop(0)
    ui.tableWidget_2.setColumnCount(len(c))
    ui.tableWidget_2.setRowCount(1)
    ui.tableWidget_2.setHorizontalHeaderLabels(c)
    i = 0
    while i != len(c) - 1:
        ui.tableWidget_2.resizeColumnToContents(i)
        i += 1
    i = 0
    while i != len(c):
        dd = ''
        cellinfo = QTableWidgetItem(dd)
        ui.tableWidget_2.setItem(0, i, cellinfo)
        i += 1

# ОТОБРАЖЕНИЕ ТАБЛИЦЫ ИЗ БД #
def showTable():
    addTable()
    a = ui.comboBox.currentText()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM """ + str(a))
        a = cursor.fetchall()
    i = 0
    ui.tableWidget.clear()
    if len(a) != 0:
        ui.tableWidget.setColumnCount(len(a[0]))
        ui.tableWidget.setRowCount(len(a))
        c = showTableName()
        ui.tableWidget.setHorizontalHeaderLabels(c)
        i = 0
        while i != len(a):
            j = 0
            while j != len(a[i]):
                cellinfo = QTableWidgetItem(str(a[i][j]))
                ui.tableWidget.setItem(i, j, cellinfo)
                j += 1
            i += 1
    else:
        c = showTableName()
        ui.tableWidget.setHorizontalHeaderLabels(c)
        ui.tableWidget.setColumnCount(len(c))
        ui.tableWidget.setRowCount(1)
        c = showTableName()
        ui.tableWidget.setHorizontalHeaderLabels(c)
    i = 0
    while i != len(c) - 1:
        ui.tableWidget.resizeColumnToContents(i)
        i += 1

# ДОБАВЛЕНИЕ #
def add():
    ui.label_4.setText('')
    ii = ui.tableWidget_2.columnCount()
    if ii == 0:
        ui.label_4.setText('ОШИБКА')
        return 0
    a = ui.comboBox.currentText()
    with connection.cursor() as cursor:
        cursor.execute("""SHOW COLUMNS FROM """ + str(a))
        b = cursor.fetchall()
    i = 0
    x = []
    kk = ''
    while i != len(b):
        kk += str(b[i][0]) + ', '
        i += 1
    kk = kk[:len(kk) - 2]
    i = 0
    k = len(b)
    if b[0][0] == 'Номер_роли' or b[0][0] == 'Код_местоположения_СЗИ' or b[0][0] == 'Код_сотрудника' or b[0][0] == 'Код_типа_обновления' or b[0][0] == 'Код_типа_ремонта' or b[0][0] == 'Код_типа_решения' or b[0][0] == 'Код_типа_СЗИ':
        k = len(b) - 1
        cc = len(kk) - len(b[0][0])
        cc = len(kk) - cc
        kk = kk[cc+2:]
    val = ''
    while i != k:
        d = ui.tableWidget_2.item(0, i)
        d = d.text()
        x.append(d)
        val += '"' + x[i] + '", '
        i += 1
    val = val[:len(val) - 2]
    try:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO """ + str(a) + """(""" + str(kk) + """) VALUES(""" + str(val) + """)""")
        connection.commit()
        showTable()
    except:
        ui.label_4.setText('ОШИБКА')

# УДАЛЕНИЕ #
def delete():
    ui.label_4.setText('')
    a = ui.comboBox.currentText()
    with connection.cursor() as cursor:
        cursor.execute("""SHOW COLUMNS FROM """ + str(a))
        b = cursor.fetchall()
    i = ui.tableWidget.currentRow()
    if i == -1:
        ui.label_4.setText('ОШИБКА')
    else:
        x = ui.tableWidget.item(i, 0)
        x = x.text()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM """ + str(a) + """ WHERE """ + str(b[0][0]) + """=""" + str(x))
        connection.commit()
        showTable()
        ui.label_4.setText('')
    except:
        ui.label_4.setText('ОШИБКА')

# РЕДАКТИРОВАНИЕ #
def update():
    ui.label_4.setText('')
    c = showTableName()
    a = ui.comboBox.currentText()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM """ + str(a))
        b = cursor.fetchall()
    x = []
    if ui.tableWidget.rowCount() == 0:
        ui.label_4.setText('ОШИБКА')
        return 0
    i = 0
    while i != ui.tableWidget.rowCount():
        j = 0
        y = []
        while j != ui.tableWidget.columnCount():
            yy = ui.tableWidget.item(i, j)
            yy = yy.text()
            y.append(yy)
            j += 1
        x.append(y)
        i += 1
    i = 0
    while i != ui.tableWidget.rowCount():
        j = 0
        while j != ui.tableWidget.columnCount():
            if str(b[i][j]) != str(x[i][j]):
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""UPDATE """ + str(a) + """ SET """ + str(c[j]) + """='""" + str(x[i][j]) + """' WHERE """ + str(c[j]) + """ = '""" + str(b[i][j]) + """'""")
                    connection.commit()
                    showTable()
                except:
                    ui.label_4.setText('ОШИБКА')
            j += 1
        i += 1

# ПОИСК #
def search():
    ui.label_4.setText('')
    x = ui.lineEdit.text()
    if len(x) == 0:
        ui.label_4.setText('ОШИБКА')
        return 0
    a = ui.comboBox.currentText()
    with connection.cursor() as cursor:
        cursor.execute("""SHOW COLUMNS FROM """ + str(a))
        b = cursor.fetchall()
    ui.spinBox.setMaximum(len(b))
    kk = ui.spinBox.value()
    if kk > len(b):
        ui.label_4.setText('ОШИБКА')
        return 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM """ + str(a) + """ WHERE """ + str(b[kk-1][0]) + """ LIKE '%""" + str(x) + """%'""")
            k = cursor.fetchall()
    except:
        ui.label_4.setText('ОШИБКА')
        return 0
    if len(k) == 0:
        ui.label_4.setText('ОШИБКА')
        return 0
    ui.tableWidget.clear()
    ui.tableWidget.setColumnCount(len(k[0]))
    ui.tableWidget.setRowCount(len(k))
    c = showTableName()
    ui.tableWidget.setHorizontalHeaderLabels(c)
    i = 0
    while i != len(k):
        j = 0
        while j != len(k[0]):
            cellinfo = QTableWidgetItem(str(k[i][j]))
            ui.tableWidget.setItem(i, j, cellinfo)
            j += 1
        i += 1

# ОБЪЕДИНЕНИЕ #
def join():
    ui.label_4.setText('')
    a = ui.comboBox.currentText()
    if a == 'сотрудники':
        sotrudniki()
    if a == 'сзи':
        szi()
    if a == 'использование_сзи':
        useSzi()
    if a == 'ремонт_и_обновление_сзи':
        repairAndRenewal()
    if a == 'внутренний_аудит_сзи':
        audit()

# отображение связанных таблиц #
def showRelations(a):
    ui.tableWidget.clear()
    ui.tableWidget.setColumnCount(len(a[0]))
    ui.tableWidget.setRowCount(len(a))
    c = showTableName()
    ui.tableWidget.setHorizontalHeaderLabels(c)
    i = 0
    while i != len(a):
        j = 0
        while j != len(a[0]):
            cellinfo = QTableWidgetItem(str(a[i][j]))
            ui.tableWidget.setItem(i, j, cellinfo)
            j += 1
        i += 1

# join для сотрудников #
def sotrudniki():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT сотрудники.Код_сотрудника, сотрудники.Фамилия, сотрудники.Имя, сотрудники.Отчество, роли.Название FROM сотрудники JOIN роли ON роли.Номер_роли = сотрудники.Роли_Номер_роли""")
        a = cursor.fetchall()
    showRelations(a)

# join для сзи #
def szi():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT сзи.Дата_окончания_срока_действия, сзи.Дата_добавления, сзи.Примечание, местоположение_сзи.Название, типы_сзи.Название FROM сзи JOIN местоположение_сзи ON местоположение_сзи.Код_местоположения_СЗИ = сзи.Местоположение_СЗИ_Код_местоположения_СЗИ JOIN типы_сзи ON типы_сзи.Код_типа_СЗИ = сзи.Типы_СЗИ_Код_типа_СЗИ""")
        a = cursor.fetchall()
    showRelations(a)

# join для использования сзи #
def useSzi():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT использование_сзи.Дата_начала_использования, использование_сзи.Примечание, сотрудники.Фамилия, сзи.Дата_окончания_срока_действия, типы_сзи.Название FROM использование_сзи JOIN сотрудники ON сотрудники.Код_сотрудника = использование_сзи.Сотрудники_Код_сотрудника JOIN сзи ON сзи.Дата_окончания_срока_действия = использование_сзи.СЗИ_Дата_окончания_срока_действия JOIN типы_сзи ON типы_сзи.Код_типа_СЗИ = использование_сзи.СЗИ_Типы_СЗИ_Код_типа_СЗИ""")
        a = cursor.fetchall()
    showRelations(a)

# join для ремонт и обновление сзи #
def repairAndRenewal():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT ремонт_и_обновление_сзи.Дата_ремонта_или_обновления, ремонт_и_обновление_сзи.Дата_окончания_срока_действия_СЗИ, типы_сзи.Название, сотрудники.Фамилия, типы_ремонта.Название, типы_обновлений.Название FROM ремонт_и_обновление_сзи JOIN типы_сзи ON типы_сзи.Код_типа_СЗИ = ремонт_и_обновление_сзи.Код_типа_СЗИ JOIN сотрудники ON сотрудники.Код_сотрудника = ремонт_и_обновление_сзи.Код_сотрудника JOIN типы_ремонта ON типы_ремонта.Код_типа_ремонта = ремонт_и_обновление_сзи.Код_типа_ремонта JOIN типы_обновлений ON типы_обновлений.Код_типа_обновления = ремонт_и_обновление_сзи.Код_типа_обновления""")
        a = cursor.fetchall()
    showRelations(a)

# join для внутренний аудит сзи #
def audit():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT внутренний_аудит_сзи.Дата_аудита, типы_решений_по_аудиту.Название, внутренний_аудит_сзи.СЗИ_Дата_окончания_срока_действия, типы_сзи.Название, сотрудники.Фамилия FROM внутренний_аудит_сзи JOIN типы_решений_по_аудиту ON типы_решений_по_аудиту.Код_типа_решения = внутренний_аудит_сзи.Типы_решений_по_аудиту_Код_типа_решения JOIN типы_сзи ON типы_сзи.Код_типа_СЗИ = внутренний_аудит_сзи.СЗИ_Типы_СЗИ_Код_типа_СЗИ JOIN сотрудники ON сотрудники.Код_сотрудника = внутренний_аудит_сзи.Сотрудники_Код_сотрудника""")
        a = cursor.fetchall()
    showRelations(a)

ui.button.clicked.connect(showTable)  # если нажата кнопка Показать
ui.pushButton_4.clicked.connect(delete)  # если нажата кнопка Удалить
ui.pushButton_2.clicked.connect(add)  # если нажата кнопка Добавить
ui.pushButton_3.clicked.connect(update)  # если нажата кнопка Редактировать
ui.pushButton_6.clicked.connect(search)  # если нажата кнопка Поиск
ui.pushButton_5.clicked.connect(join)  # если нажата кнопка Отобразить связанные таблицы


sys.exit(app.exec_())
