import cv2 as cv
import numpy as np


def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    pass


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]].
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    pass


def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere.
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.    '''
    b = 0
    g = 0
    r = 0
    counter = 0
    for i in range(levo_zgoraj[0], desno_spodaj[0]):
        for j in range(levo_zgoraj[1], desno_spodaj[1]):
            b += int(slika[j][i][0])
            g += int(slika[j][i][1])
            r += int(slika[j][i][2])
            counter += 1

    # print(int(b / counter), int(g / counter), int(r / counter))
    return int(b / counter), int(g / counter), int(r / counter)

def main():
    cam = cv.VideoCapture(0)
    # prvi frame
    ret, frame1 = cam.read()
    # doloci sredino slike
    sredina = (frame1.shape[1] // 2, frame1.shape[0] // 2)
    x_10 = frame1.shape[0] / 7.5
    y_10 = frame1.shape[1] / 7.5
    levo_zgoraj = (int(sredina[0] - x_10), int(sredina[1] - y_10))
    desno_spodaj = (int(sredina[0] + x_10), int(sredina[1] + y_10))
    barva_koze = doloci_barvo_koze(frame1, levo_zgoraj, desno_spodaj)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Can't receive frame (stream end?)")
            break
        frame = cv.flip(frame, 1)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cam.release()


if __name__ == '__main__':
    main()
