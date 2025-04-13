import cv2 as cv
import numpy as np

VELIKOST_SKATLE = 20


def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina))


def izris_kvadrata(slika, levo_zgoraj, desno_spodaj):
    '''Izriše kvadrat na sliki z barvo barva.'''
    return cv.rectangle(slika, levo_zgoraj, desno_spodaj, (0, 255, 0), 2)


def nared_skatle_na_sliki(slika, sirina_skatle, visina_skatle) -> list:
    '''Naredi škatle na sliki.'''
    skatle = []
    for i in range(0, slika.shape[1], sirina_skatle):
        for j in range(0, slika.shape[0], visina_skatle):
            levo_zgoraj = (i, j)
            desno_spodaj = (min(i + sirina_skatle, slika.shape[1]), min(j + visina_skatle, slika.shape[0]))
            skatle.append((levo_zgoraj, desno_spodaj))
    return skatle


def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    counter = 0
    scaler = 40
    for i in range(slika.shape[0]):
        for j in range(slika.shape[1]):
            upper = barva_koze[0] + scaler, barva_koze[1] + scaler, barva_koze[2] + scaler
            lower = barva_koze[0] - scaler, barva_koze[1] - scaler, barva_koze[2] - scaler

            if (slika[j][i][0] <= upper[0]) and (slika[j][i][0] >= lower[0]) and (slika[j][i][1] <= upper[1]) and (
                    slika[j][i][1] >= lower[1]) and (slika[j][i][2] <= upper[2]) and (slika[j][i][2] >= lower[2]):
                counter += 1

    return counter


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

    return int(b / counter), int(g / counter), int(r / counter)


def main():
    cam = cv.VideoCapture(0)
    ret, frame1 = cam.read()
    frame1 = zmanjsaj_sliko(frame1, 240, 320)
    # doloci sredino slike
    sredina = (frame1.shape[1] // 2, frame1.shape[0] // 2)
    x_10 = frame1.shape[0] / 7
    y_10 = frame1.shape[1] / 5
    levo_zgoraj_box = (int(sredina[0] - x_10), int(sredina[1] - y_10))
    desno_spodaj_box = (int(sredina[0] + x_10), int(sredina[1] + y_10))

    barva = doloci_barvo_koze(frame1, levo_zgoraj_box, desno_spodaj_box)

    prev_tick = cv.getTickCount()
    while True:
        ret, frame = cam.read()
        ret, frame1 = cam.read()
        frame = zmanjsaj_sliko(frame, 240, 320)
        frame1 = zmanjsaj_sliko(frame1, 240, 320)
        if not ret:
            print("Can't receive frame (stream end?)")
            break
        frame = cv.flip(frame, 1)
        frame1 = cv.flip(frame1, 1)

        current_tick = cv.getTickCount()
        time_diff = (current_tick - prev_tick) / cv.getTickFrequency()
        fps = 1 / time_diff
        prev_tick = current_tick

        cv.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

        skatle = nared_skatle_na_sliki(frame, VELIKOST_SKATLE, VELIKOST_SKATLE)
        for levo_zgoraj, desno_spodaj in skatle:
            enbox = frame[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]
            piksli = prestej_piklse_z_barvo_koze(enbox, barva)
            if piksli > int(VELIKOST_SKATLE * VELIKOST_SKATLE / 2):
                cv.rectangle(frame, levo_zgoraj, desno_spodaj, (0, 255, 0), 1)
            else:
                cv.rectangle(frame, levo_zgoraj, desno_spodaj, (0, 0, 255), 1)
        izris_kvadrata(frame1, levo_zgoraj_box, desno_spodaj_box)
        cv.imshow('frame', frame)
        cv.imshow('frame1', frame1)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            ret, frame1 = cam.read()
            frame1 = zmanjsaj_sliko(frame1, 240, 320)
            frame1 = cv.flip(frame1, 1)
            barva = doloci_barvo_koze(frame1, levo_zgoraj_box, desno_spodaj_box)
            izris_kvadrata(frame1, levo_zgoraj_box, desno_spodaj_box)
    cam.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
