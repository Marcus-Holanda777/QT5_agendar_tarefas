import threading
from Designer import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QDateTimeEdit, QFileDialog, QLineEdit, QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget, QMessageBox
import sys
from datetime import datetime, timedelta
from time import sleep
import subprocess


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        super().setupUi(self)

        ''' ESTILO '''
        self.lineFile.setDisabled(True)

        ''' DATA E HORA ATUAL '''
        self.dtMarca.setDateTime(datetime.now())

        ''' BOTOES E FUNCOES '''
        self.btnFile.clicked.connect(self.btn_executar)
        self.btnAgenda.clicked.connect(self.btn_inserir)

    def btn_executar(self):
        line: QLineEdit = self.lineFile
        nome_arq, _ = QFileDialog.getOpenFileName(filter=('*.py'))
        line.setText(nome_arq)

    def schedular(self, periodo: datetime, comando):
        print(f'Arquivo: {comando}, Agendado para --> > {periodo}\n')
        while True:
            if datetime.now() > periodo:
                self.comando_agendar(periodo, comando)
                break
            sleep(1)

    def comando_agendar(self, periodo: datetime, comando_comp):
        cam = '\\'.join(comando_comp.split('/')[:-1])
        arq = comando_comp.split('/')[-1]
        comando = 'python %s' % arq

        print(f'Caminho: {cam}, comando: {comando}')
        subprocess.Popen(comando, cwd=cam, shell=True).wait()

        novoAgenda = periodo + timedelta(days=1)

        self.schedular(novoAgenda, comando_comp)

    def btn_inserir(self):
        dtMarca: QDateTimeEdit = self.dtMarca

        if self.lineFile.text() != '' and dtMarca.dateTime().toPyDateTime() > datetime.now():
            msg = f'Tarefa: {self.lineFile.text()}, para: {self.dtMarca.text()}'
            resposta = QMessageBox.warning(self, 'Agendar', 'Deseja agendar ?\n' + msg,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if resposta == QMessageBox.Yes:

                tblAgenda: QTableWidget = self.tblAgenda

                lin = tblAgenda.rowCount()
                tblAgenda.insertRow(lin)

                tblAgenda.setItem(
                    lin, 0, QTableWidgetItem(self.lineFile.text()))
                tblAgenda.setItem(lin, 1, QTableWidgetItem(dtMarca.text()))

                ''' AJUSTAR LINHAS E COLUNAS  '''
                tblAgenda.resizeColumnsToContents()
                tblAgenda.resizeRowsToContents()

                job = threading.Thread(target=self.schedular, args=[
                    dtMarca.dateTime().toPyDateTime(), self.lineFile.text()])
                job.start()
        else:
            QMessageBox.critical(
                self, 'ERRO', 'Hora ou arquivo errado !', QMessageBox.Yes)

    def closeEvent(self, event):
        reply = QMessageBox.critical(self, 'Sair ?',
                                     'Deseja Realmente sair ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if not type(event) == bool:
                event.accept()

            else:
                sys.exit()

        else:
            if not type(event) == bool:
                event.ignore()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = App()
    app.show()
    qt.exec_()
