import os
import time 

lubang=dict.fromkeys((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23),0)  #dict is faster than list 
def gotoxy(x,y):
    print ("%c[%d;%df" % (0x1B, y, x), end='')

def reset_papan (biji1,biji2):	
		#Isi 11 biji pada pemain 1
    for i in reversed(range(0,10+1)):	
    		#Memindahkan 11 biji kesetiap lubang kecil 
        #Lubang yang hangus (-1) tidak boleh digunakan lagi
        if biji1>=11 and lubang[i]>=0:
            lubang[i]=11
            biji1-=11
        else :
        #Jika biji kurang dari 11, maka lubang akan hangus dan kita tandai dengan -1
            lubang[i]=-1
    #Menaruh sisa biji kedalam lubang besar/Rumah
    lubang[11]=biji1
		
    #Mengisi 11 biji pada pemain 2
    for i in reversed(range(12,22+1)):
    		#Memindahkan 11 biji kesetiap lubang kecil
        if biji2>=11 and lubang[i]>=0:
            lubang[i]=11
            biji2-=11
        else :
        #Jika biji kurang dari 11, maka lubang akan hangus dan kita tandai dengan -1
            lubang[i]=-1
    lubang[23]=biji2

def cetak_papan (): 
    os.system('cls')
    print("______A_____B_____C_____D_____E_____F_____G_____H_____I_____J_____K_____\n\n")  
    print('    ',end='')
    # Lubang kecil di atas
    for i in reversed(range(12,22+1)): 
        if lubang[i]==-1: 
            print('(XX) ',end='')
        else : 
            print(f'({lubang[i]})  ',end='')
    print('\n')
    # Lubang besar di kiri dan kanan
    print(f"  ({lubang[23]})                                                               ({lubang[11]})\n" )
    # Lubang kecil di bawah
    print('    ',end='')
    for i in range(0,10+1): 
        if lubang[i]==-1: 
            print('(XX) ',end='')
        else : 
            print(f'({lubang[i]})  ',end='')

def cetak_genggaman(index,jumlah): 
    if 12 <= index <=22 : 
        gotoxy((5+6*(22-index)),3)
    elif 0 <= index <= 10: 
        gotoxy((5+6*index),9)
    elif index==11 : 
        gotoxy(68,7)
    else : 
        gotoxy(1,7)
    print(f'[{jumlah}]',flush=True)

def distribusi_biji (index, pemain):
	# Memindahkan Biji ke genggaman
    genggaman = lubang[index]
    lubang[index]=0
	# Perbaharui papan dan beri jeda waktu 0,3 detik sebelum melanjutkan
    cetak_papan()
    cetak_genggaman(index, genggaman)
    time.sleep(0.3)
	# Distribusikan biji berlawanan arah jarum jam
    while (genggaman > 0):
  # Geser index ke lubang di sampingnya
        index = (index + 1) % 24
  # Jika index berada di lubang besar pemain lawan, lompati lubang tersebut
        while ((pemain == 1 and index == 23) or (pemain == 2 and index == 11) or (lubang[index] == -1)):
            index = (index + 1) % 24  
  # Pindahkan satu biji dari genggaman ke lubang
        lubang[index] += 1
        genggaman -=1
	# Perbaharui papan dan beri jeda waktu 0,3 detik sebelum melanjutkan
        cetak_papan()
        cetak_genggaman(index,genggaman)
        time.sleep(0.3)
    return index

def menembak_biji (index, pemain):
	# Lubang bernilai -1 tidak dapat ditembak
    if (lubang[index]== -1):
        return
  # Pindahkan biji ke genggaman
    genggaman = lubang[index]
    lubang[index] = 0
    
    cetak_papan()
    cetak_genggaman(index, genggaman)
    time.sleep(0.3)
 # Indeks rumah milik pemain:
 # pemain 1 = lubang[11]
 # pemain 2 = lubang[23]
    if (pemain == 1):
        index = 11
    else:
        index = 23
    lubang[index] += genggaman
    genggaman = 0

    cetak_papan()
    cetak_genggaman(index, pemain)
    time.sleep(0.3)

def pilih_lubang(pemain):
	# Program akan meminta Input
    while True:
        inpu=input("Pilih lubang [A..K]: ")
        if len(inpu) >1 : continue
        if ord('a')<= ord(inpu) <=ord('k') or ord('A')<= ord(inpu) <=ord('K'): 
            inpu=inpu.lower()
            break
    if (pemain == 1):
        index = ord(inpu) - ord('a')
    else:
        index = 22 - (ord(inpu) - ord('a'))
	# Jika lubang yang dipilih kosong, ulangi permintaan input
    if(lubang[index] <= 0):
        return pilih_lubang(pemain)
    else:
        return index


def cek_permainan_selesai():
    # Pengecekam sisi pemain 1
    selesai=1
    i=0
    for i in range(11):
        if lubang[i]>0:
            selesai=0
            break
    # Jika sisi pemain 1 masih terisi, coba cek sisi pemain 2
    if selesai==0:
        selesai=1
        for i in range(12,23) :
            if lubang[i]>0:
                selesai=0
                break
    return selesai

def alur_permainan(pemain):
    index = -1
    # Kontrol Alur Permainan
    while True :
        cetak_papan()
        if index == -1:
            print("GILIRAN PEMAIN #",pemain)
            index = pilih_lubang(pemain)
        
    # lakukan distribusi biji
        index = distribusi_biji(index,pemain)
        if (index == 11 or index == 23) :
            index = -1
        elif lubang[index] > 1 :
            lubang[index]=lubang[index]
        else :
            if ((pemain == 1) and (index >= 0) and (index <= 10)):
                menembak_biji(index, pemain)
                menembak_biji(22 - index, pemain)
            elif ((pemain == 2) and (index >= 12) and (index <= 22)):
                menembak_biji(index, pemain)
                menembak_biji(22 - index, pemain)
            index = -1
            pemain = (pemain % 2) + 1
            pass
        if cek_permainan_selesai() != 0:
            break
    #Jika permainan selesai, gabungkan semua biji di lubang sisi pemain ke rumah miliknya
    for i in range(11) :
     #proses lumbung hangus
        if (lubang[i] == -1):
            continue
    
        lubang[11] += lubang[i]
        lubang[i] = 0
    #proses lumbung hangus
    for i in range(12,23) :
        if lubang[i] == -1 :
            continue
        lubang[23] += lubang[i]
        lubang[i] = 0
    cetak_papan()
            
def cek_babak_selesai():
	#Jika lubang pemain 1 kurang dari 11 atau pemain 2 kurang dari 11 program akan memberikan nilai true
    if ((lubang[11] < 11) or (lubang[23] < 11)) :
        return 1
    else :
        return 0

def alur_babak():
    babak=0
    pemain=1
    
  # Pada awal permainan, beri 121 biji di rumah masing-masing
    lubang[11]=121
    lubang[23]=121
    
  #Reset papan dan tampilkan babak
    while True:
        reset_papan(lubang[11], lubang[23])
        cetak_papan()
        babak+=1
        print("BABAK ", babak)
        time.sleep(1)

  #Memanggil fungsi alur_permainan
        alur_permainan(pemain)
        if (lubang[11] > lubang[23]) :
            pemain = 2
        elif (lubang[23 > lubang[11]]):
            pemain = 1
        else :
            pemain = (pemain % 2)+1
  # Beri jeda selama 1 detik untuk menampilkan posisi akhir sebelum melanjutkan babak berikutnya
        time.sleep(1)
        if(cek_babak_selesai == 0):
            break

alur_babak()
print("permainan selesai")
if lubang[11] > lubang[23]: 
    print('pemain 1 menang')
elif lubang [23] > lubang [11]: 
    print('pemain 2 menang')
else : 
    print('seri')
input()

        
        