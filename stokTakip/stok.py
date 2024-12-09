import tkinter as tk
from tkinter import ttk
import sqlite3

class StokTakipUygulamasi:
    def __init__(self , root):
        self.root=root
        self.root.title("Stok Takip Uygulamasi")

        self.conn=sqlite3.connect("stokTakip.db")
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stok(
                            id TEXT PRİMARY KEY,
                            urunAdi TEXT,
                            adet INTEGER,
                            birimFiyati REAL,
                            toplamDeger REAL
            )
    """)
        self.conn.commit()

        self.idLabel=tk.Label(root,text="ID")
        self.idLabel.grid(row=0,column=0)
        self.idEntry=tk.Entry(root)
        self.idEntry.grid(row=0,column=1)

        self.urunAdiLabel=tk.Label(root,text="Ürün Adı:")
        self.urunAdiLabel.grid(row=1,column=0)
        self.urunAdiEntry=tk.Entry(root)
        self.urunAdiEntry.grid(row=1,column=1)

        self.adetLabel=tk.Label(root,text="Adet:")
        self.adetLabel.grid(row=2,column=0)
        self.adetEntry=tk.Entry(root)
        self.adetEntry.grid(row=2,column=1)
        
        self.birimFiyatiLabel=tk.Label(root,text="Birim Fiyatı:")
        self.birimFiyatiLabel.grid(row=3,column=0)
        self.birimFiyatiEntry=tk.Entry(root)
        self.birimFiyatiEntry.grid(row=3,column=1)

        self.ekleButton=tk.Button(root,text="Ekle",command=self.ekle)
        self.ekleButton.grid(row=4,column=0,columnspan=1)

        self.duzeltButton=tk.Button(root,text="Düzelt",command=self.duzelt)
        self.duzeltButton.grid(row=4,column=1,columnspan=1)

        self.silButton=tk.Button(root,text="Sil",command=self.sil)
        self.silButton.grid(row=4,column=2,columnspan=1)

        self.temizleButton=tk.Button(root,text="Temizle",command=self.girisleriTemizle)
        self.temizleButton.grid(row=4,column=3,columnspan=1)

        self.aramaLabel=tk.Label(root,text="Ara")
        self.aramaLabel.grid(row=5,column=0)
        self.aramaEntry=tk.Entry(root)
        self.aramaEntry.grid(row=5,column=1)

        self.aramaEntry.bind("<KeyRelease>",self.arama)

        self.tablo=ttk.Treeview(root,columns=("ID","Ürün Adı","Adet","Birim Fiyatı","Toplam Değer"),show="headings")
        self.tablo.heading("ID",text="ID")
        self.tablo.heading("Ürün Adı",text="Ürün Adı")
        self.tablo.heading("Adet",text="Adet")
        self.tablo.heading("Birim Fiyatı",text="Birim Fiyatı")
        self.tablo.heading("Toplam Değer",text="Toplam Değer")
        self.tablo.grid(row=6,column=0,columnspan=4)

        self.tablo.bind("<ButtonRelease-1>",self.satirSec)

        self.verileriYukle()

    def ekle(self):
        id=self.idEntry.get()
        urunAdi=self.urunAdiEntry.get()
        adet=int(self.adetEntry.get())
        birimFiyati=float(self.birimFiyatiEntry.get())
        toplamDeger=adet*birimFiyati
        
        self.cursor.execute("INSERT INTO stok VALUES (?,?,?,?,?)",(id,urunAdi,adet,birimFiyati,toplamDeger))
        self.conn.commit()

        self.tablo.insert("","end",values=(id,urunAdi,adet,birimFiyati,toplamDeger))
        self.girisleriTemizle()

    def girisleriTemizle(self):
        self.idEntry.delete(0,tk.END)
        self.urunAdiEntry.delete(0,tk.END)
        self.adetEntry.delete(0,tk.END)
        self.birimFiyatiEntry.delete(0,tk.END)
    
    def arama(self,event):
        aramaMetni=self.aramaEntry.get().lower()
        for item in self.tablo.get_children():
            values=self.tablo.item(item,"values")
            if aramaMetni in values[0].lower() or aramaMetni in values[1] or aramaMetni in values[2] or aramaMetni in values[3].lower():
                self.tablo.selection_set(item)
                self.tablo.see(item)

            else:
                self.tablo.selection_remove(item)
    def satirSec(self,event):
        secili=self.tablo.selection()
        if secili:
            item=self.tablo.item(secili)
            values=item["values"]
            self.idEntry.delete(0,tk.END)
            self.idEntry.insert(0,values[0])
            self.urunAdiEntry.delete(0,tk.END)
            self.urunAdiEntry.insert(0,values[1])
            self.adetEntry.delete(0,tk.END)
            self.adetEntry.insert(0,values[2])
            self.birimFiyatiEntry.delete(0,tk.END)
            self.birimFiyatiEntry.insert(0,values[3])



    def duzelt(self):
        secili=self.tablo.selection()
        if secili:
            id=self.idEntry.get()
            urunAdi=self.urunAdiEntry.get()
            adet=int(self.adetEntry.get())
            birimFiyati=float(self.birimFiyatiEntry.get())
            toplamDeger=adet*birimFiyati
        
            self.cursor.execute("UPDATE stok VALUES (urunAdi=?,adet=?,birimFiyati=?,toplamDeger=? WHERE  id=?)",(urunAdi,adet,birimFiyati,toplamDeger,id))
            self.conn.commit()
            self.tablo.item(secili,values=(id,urunAdi,adet,birimFiyati,toplamDeger))
            self.girisleriTemizle()
    def sil(self):
        secili=self.tablo.selection()
        if secili:
            id=self.tablo.item(secili)['values'][0]
            self.cursor.execute("DELETE FROM stok WHERE id=?", (id,))
            self.conn.commit()
            self.tablo.delete(secili)
            self.girisleriTemizle()
    def verileriYukle(self):
        for row in self.cursor.execute("SELECT * FROM stok"):
            self.tablo.insert("", "end", values=row)





        






if __name__=="__main__":
    root=tk.Tk()
    app=StokTakipUygulamasi(root)
    root.mainloop()