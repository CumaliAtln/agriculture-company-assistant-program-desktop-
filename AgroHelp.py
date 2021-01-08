import sys

import mysql.connector
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QPushButton,
                             QRadioButton, QVBoxLayout, QWidget, qApp)
from mysql.connector import connection

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "app"
)

#from connection import connection


class Pesticide():
    connection = connection
    cursor = connection.cursor()

    def __init__(self, isim, fiyat, hastalik, dozaj, kullanim, tip):
        self.isim = isim
        self.fiyat = fiyat
        self.hastalik = hastalik
        self.dozaj = dozaj
        self.kullanim = kullanim
        self.tip = tip


    def savePesticide(isim, fiyat, hastalik, dozaj, kullanim, tip):
        
        isim = isim
        fiyat = fiyat
        hastalik = hastalik
        dozaj = dozaj
        kullanim = kullanim
        tip = tip
        
        sql =  "INSERT INTO tarimsal(isim, fiyat, hastalik, dozaj, kullanim, tip) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (isim, fiyat, hastalik, dozaj, kullanim, tip)
        Pesticide.cursor.execute(sql, value)
        
        try:
            Pesticide.connection.commit()
        except mysql.connector.Error as err:
            print("hata: ", err)
        finally: 
            Pesticide.connection.close()


    @staticmethod
    def savePesticides(list):
        connection = Pesticide.connection
        cursor = Pesticide.cursor
        sql =  "INSERT INTO tarimsal(isim, fiyat, hastalik, dozaj, kullanim, tip) VALUES (%s, %s, %s, %s, %s, %s)"
        values = list
        cursor.executemany(sql, values)

        try:
            connection.commit()
        except mysql.connector.Error as err:
            pass
        finally: 
            connection.close()


    def getDisease(hastalik):
        cursor = Pesticide.cursor
        hastalik = hastalik
        
        cursor.execute("SELECT isim, fiyat, hastalik FROM tarimsal WHERE hastalik LIKE '%"+ str(hastalik) + "%'")
        result = cursor.fetchall()
        
        return result

    
    def getPesticide(isim):
        cursor = Pesticide.cursor
        isim = isim
        
        cursor.execute("SELECT isim, fiyat, hastalik FROM tarimsal WHERE isim LIKE '%"+ str(isim) + "%'")
        result = cursor.fetchall()
        
        return result


    def updatePesticidePrice(isim, fiyat):      
        connection = Pesticide.connection
        cursor = Pesticide.cursor
        isim = isim
        fiyat = fiyat

        sql = "UPDATE tarimsal SET fiyat= %s WHERE isim = %s"
        values = (fiyat, isim)
        cursor.execute(sql, values)

        try:
            connection.commit()
        except mysql.connector.Error as err:
            pass
        finally:
            connection.close()

    def updatePesticideDisease(isim, hastalik):
        connection = Pesticide.connection
        cursor = Pesticide.cursor

        isim = isim
        hastalik = hastalik

        sql = "UPDATE tarimsal SET hastalik= %s WHERE isim = %s"
        values = (hastalik, isim)
        cursor.execute(sql, values)

        try:
            connection.commit()
        except mysql.connector.Error as err:
            pass
        finally:
            connection.close()


    def deletePesticide(isim):
        connection = Pesticide.connection
        cursor = connection.cursor()

        isim = isim
        value = str(isim)

        sql = """delete from tarimsal where isim = %s"""        
        cursor.execute(sql, (value,))
                
        try:
            connection.commit()
        except mysql.connector.Error as err:
            pass
        finally:
            connection.close()

class PencereHomePage(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        self.etiket = QLabel("Girmek İstediğiniz Sorguyu Seçiniz")
        self.getPesticide_btn = QPushButton("İlaç Sorgulama    ")
        self.getDisease_btn =QPushButton("Hastalık Sorgulama")
        self.save_btn = QPushButton("Yeni Ürün Ekleme  ")
        self.delete_btn = QPushButton("Ürün Silme        ")        
        self.update_btn = QPushButton("Güncelleme        ")
        self.cikis_btn = QPushButton("Çıkış             ")

        g_box = QGridLayout()
        g_box.addWidget(self.etiket, 0,0)
        g_box.addWidget(self.getPesticide_btn, 1,0)
        g_box.addWidget(self.getDisease_btn, 1,1)
        g_box.addWidget(self.save_btn, 2,0)
        g_box.addWidget(self.delete_btn, 2,1)
        g_box.addWidget(self.update_btn, 3,0)
        g_box.addWidget(self.cikis_btn, 3,1)

        self.setLayout(g_box)
        self.setWindowTitle("AgroHelp")
        
        self.getDisease_btn.clicked.connect(lambda: self.getDisease_btn_click(self.getDisease_btn))
        self.getPesticide_btn.clicked.connect(lambda: self.getPesticide_btn_click(self.getPesticide_btn))
        self.save_btn.clicked.connect(lambda: self.save_btn_click(self.save_btn))
        self.delete_btn.clicked.connect(lambda: self.delete_btn_click(self.delete_btn))
        self.update_btn.clicked.connect(lambda: self.update_btn_click(self.update_btn))
        self.cikis_btn.clicked.connect(lambda: self.cikis_btn_click(self.cikis_btn))
        
        self.show()
   
    
    def getDisease_btn_click(self, getDisease_btn):
        if getDisease_btn:
           PencereGetDisease()

            
    def getPesticide_btn_click(self, getPesticide_btn):
        if getPesticide_btn:
            PencereGetPesticide()
            

    def save_btn_click(self, save_btn):
        if save_btn:
            PencereSave()
    

    def delete_btn_click(self,delete_btn):
        if delete_btn:
            PencereDelete()
    

    def update_btn_click(self, update_btn):
        if update_btn:
            PencereUpdate()
    

    def cikis_btn_click(self, cikis_btn):
        if cikis_btn:
            qApp.quit()


class PencereGetDisease(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        self.etiket =QLabel("Sorgulamak İstediğiniz HASTALIK İçin Bilgi Girişini Yapınız")

        self.hastalik_etiket = QLabel("Hastalık İsmi: ")
        
        self.hastalik_input = QLineEdit("")

        self.sorgu_btn = QPushButton("Sorgula")
        self.cikis_btn = QPushButton("Çıkış")
        self.sonuc_etiket = QLabel("")

        g_box = QGridLayout()
        g_box.addWidget(self.etiket, 0,0)
        g_box.addWidget(self.hastalik_etiket, 1,0)
        g_box.addWidget(self.hastalik_input, 1,1)
        g_box.addWidget(self.sorgu_btn, 2,0)
        g_box.addWidget(self.cikis_btn, 2,1)
        g_box.addWidget(self.sonuc_etiket, 3,0)

        self.setLayout(g_box)
        self.setWindowTitle("AgroHelp Hastalıklara Göre Sorgu")
        
        self.sorgu_btn.clicked.connect(lambda: self.sorgu_btn_click(self.hastalik_input))
        self.cikis_btn.clicked.connect(lambda: self.cikis_btn_click(self.cikis_btn))
        self.show()

    def sorgu_btn_click(self, hastalik_input):
        hastalik = self.hastalik_input.text()

        result = Pesticide.getDisease(hastalik)
        for i in result:
            self.sonuc_etiket.setText(f'isim: {i[0]} fiyat: {i[1]} hastalik: {i[2]}')
    
    def cikis_btn_click(self, cikis_btn):
        if cikis_btn:
            qApp.quit()


class PencereGetPesticide(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        self.etiket =QLabel("Sorgulamak İstediğiniz ÜRÜN İçin Bilgi Girişini Yapınız")

        self.isim_etiket = QLabel("Ürün İsmi: ")
        
        self.isim_input = QLineEdit("")

        self.sorgu_btn = QPushButton("Sorgula")

        self.sonuc_etiket = QLabel("")

        g_box = QGridLayout()
        g_box.addWidget(self.etiket, 0,0)
        g_box.addWidget(self.isim_etiket, 1,0)
        g_box.addWidget(self.isim_input, 1,1)
        g_box.addWidget(self.sorgu_btn, 2,0)
        g_box.addWidget(self.sonuc_etiket, 3,0)

        self.setLayout(g_box)
        self.setWindowTitle("AgroHelp: Ürüne Göre Sorgu")
        
        self.sorgu_btn.clicked.connect(lambda: self.sorgu_btn_click(self.isim_input))

        self.show()

    def sorgu_btn_click(self, isim_input):
        isim = self.isim_input.text()

        result = Pesticide.getPesticide(isim)
        for i in result:
            self.sonuc_etiket.setText(f'isim: {i[0]} fiyat: {i[1]} hastalik: {i[2]}')


class PencereSave(QWidget):

    def __init__(self):

        super().__init__()
        
        self.init_ui()

    def init_ui(self):
        self.etiket = QLabel("Ürün Kaydı İçin Gerekli Bilgi Girişini Yapınız")

        self.isim_etiket = QLabel("Ürün İsmi: ")
        self.fiyat_etiket = QLabel("Ürün Fiyatı: ")
        self.hastalik_etiket = QLabel("Hastalık: ")
        self.dozaj_etiket = QLabel("Kullanım Dozajı: ")
        self.kullanim_etiket = QLabel("Kullanım Talimatı: ")
        self.tip_etiket = QLabel("Ürün Tipi: ")

        self.isim_input = QLineEdit("")
        self.fiyat_input = QLineEdit("")
        self.hastalik_input = QLineEdit("")
        self.dozaj_input = QLineEdit("")
        self.kullanim_input = QLineEdit("")
        self.tip_input = QLineEdit("")

        self.kaydet_btn = QPushButton("Kaydet")

        g_box = QGridLayout()
        g_box.addWidget(self.etiket, 0,0)
        g_box.addWidget(self.isim_etiket, 1,0)
        g_box.addWidget(self.fiyat_etiket, 2,0)
        g_box.addWidget(self.hastalik_etiket, 3,0)
        g_box.addWidget(self.dozaj_etiket, 4,0)
        g_box.addWidget(self.kullanim_etiket, 5,0)
        g_box.addWidget(self.tip_etiket, 6,0)

        g_box.addWidget(self.isim_input, 1,1)
        g_box.addWidget(self.fiyat_input, 2,1)
        g_box.addWidget(self.hastalik_input, 3,1)
        g_box.addWidget(self.dozaj_input, 4,1)
        g_box.addWidget(self.kullanim_input, 5,1)
        g_box.addWidget(self.tip_input, 6,1)
        g_box.addWidget(self.kaydet_btn, 7,0)

        self.setLayout(g_box)
        self.setWindowTitle("AgroHelp Ürün Kayıt")

        self.kaydet_btn.clicked.connect(lambda: self.kaydet_btn_click(self.isim_input, self.fiyat_input, self.hastalik_input, self.dozaj_input, self.kullanim_input, self.tip_input))



        self.show()

    def kaydet_btn_click(self, isim_input, fiyat_input, hastalik_input, dozaj_input, kullanim_input, tip_input):
        isim = self.isim_input.text()
        fiyat = self.fiyat_input.text()
        hastalik = self.hastalik_input.text()
        dozaj = self.dozaj_input.text()
        kullanim = self.kullanim_input.text()
        tip = self.tip_input.text()

        Pesticide.savePesticide(isim, fiyat, hastalik, dozaj, kullanim, tip)


class PencereUpdate(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.etiket = QLabel("Güncellemek istediğiniz bölümleri işaretleyiniz")

        self.isim_radio = QRadioButton("Ürün ismi")
        self.fiyat_box = QCheckBox("Ürün fiyatı")
        
        self.isim_input = QLineEdit("")
        self.fiyat_input = QLineEdit("")
        
        self.isim_yazi_alani = QLabel("")
        self.fiyat_yazi_alani = QLabel("")
        
        self.sec_btn = QPushButton("Seç") 
        self.guncelle_btn = QPushButton("Güncelle")
        self.cikis_btn = QPushButton("Çıkış")

        g_box = QGridLayout() 
        g_box.addWidget(self.etiket, 0,0)
        g_box.addWidget(self.isim_radio, 1,0)
        g_box.addWidget(self.fiyat_box, 2,0)
        
        g_box.addWidget(self.isim_yazi_alani, 1,2)
        g_box.addWidget(self.fiyat_yazi_alani, 2,2)
        

        g_box.addWidget(self.sec_btn, 7,0)
        g_box.addWidget(self.guncelle_btn, 7,1)
        g_box.addWidget(self.cikis_btn, 7,2)
        self.setLayout(g_box)

        self.setWindowTitle("AgroHelp")

        self.sec_btn.clicked.connect(lambda: self.sec_isim_click(self.isim_radio.isChecked(), self.isim_yazi_alani, g_box))
        self.sec_btn.clicked.connect(lambda: self.sec_fiyat_click(self.fiyat_box.isChecked(), self.fiyat_yazi_alani, g_box)) 
        
        self.guncelle_btn.clicked.connect(lambda: self.gnc_isim_click(self.isim_radio.isChecked(), self.isim_yazi_alani, self.isim_input))
        self.guncelle_btn.clicked.connect(lambda: self.gnc_fiyat_click(self.fiyat_box.isChecked(), self.fiyat_yazi_alani, self.isim_input, self.fiyat_input))
        self.cikis_btn.clicked.connect(lambda: self.cikis_btn_click(self.cikis_btn))
        self.show()


    def sec_isim_click(self, isim_radio, isim_yazi_alani, g_box): 
        if isim_radio:
            g_box.addWidget(self.isim_input, 1,1)
            isim_yazi_alani.setText("Ürün İsmi")
        else:
            isim_yazi_alani.setText("")


    def gnc_isim_click(self, isim_radio, isim_yazi_alani, isim_input):
        if isim_radio:
            a = self.isim_input.text()
            isim_yazi_alani.setText("%s"%(a))
    

    def sec_fiyat_click(self, fiyat_box, fiyat_yazi_alani, g_box):
        if fiyat_box:
            fiyat_yazi_alani.setText("Ürün Fiyatı")
            g_box.addWidget(self.fiyat_input, 2,1)
        else:
            fiyat_yazi_alani.setText("")


    def gnc_fiyat_click(self, fiyat_box, isim_yazi_alani, isim_input, fiyat_input):
        ad = self.isim_input.text()
        fiyat = self.fiyat_input.text()
        Pesticide.updatePesticidePrice(ad, fiyat)
        if fiyat_box:
            a = self.isim_input.text()      
            isim_yazi_alani.setText("%s"%(a))

    
    def cikis_btn_click(self, cikis_btn):
        if cikis_btn:
            qApp.quit()
class PencereDelete(QWidget):

    def __init__(self):

        super().__init__()
        
        self.init_ui()
    
    def init_ui(self):
        self.etiket = QLabel("Ürün Silmek İçin 'Ürün İsmi'ni Giriniz")
        
        self.isim_etiket = QLabel("Ürün İsmi: ")
        self.isim_input = QLineEdit("")
        
        self.delete_btn = QPushButton("Sil")
        self.cikis_btn = QPushButton("Çıkış")
        self.sonuc_etiket = QLabel("")

        h_box = QHBoxLayout()
        v_box = QVBoxLayout()
        v_box.addWidget(self.etiket)
        
        
        v_box.addWidget(self.isim_etiket)
        h_box.addWidget(self.isim_input)
        h_box.addWidget(self.delete_btn)
        h_box.addWidget(self.cikis_btn)
        h_box.addWidget(self.sonuc_etiket)
        
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle("AgroHelp Ürün Silme Ekranı")

        self.delete_btn.clicked.connect(lambda: self.delete_btn_click(self.isim_input))
        self.cikis_btn.clicked.connect(lambda: self.cikis_btn_click(self.cikis_btn))

        self.show()

    def delete_btn_click(self, isim_input):
        isim = isim_input.text()

        Pesticide.deletePesticide(isim)
        self.sonuc_etiket.setText("İşlem Başarılı...")
    
    def cikis_btn_click(self, cikis_btn):
        if cikis_btn:
            qApp.quit()

app = QApplication(sys.argv)
pencere = PencereHomePage()
sys.exit(app.exec_())