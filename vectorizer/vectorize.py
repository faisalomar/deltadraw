#!/usr/bin/python2

import cv

#INPUT = '4.1.05.tiff'
#INPUT = 'test2.jpg'
#INPUT = 'test4.png'
#INPUT = 'test4.jpg'
INPUT = 'test5.jpg'
#INPUT = 'test3.png'
#INPUT = 'lena.bmp'
#INPUT = 'test_pattern.jpg'
RES_X = 160

res_gray = None 
res_smooth = None 
canny = None 
contour_in = None
contour_out = None
contours = None
a_storage = None
c_storage = None

canny_lo = 30
canny_hi = 70
canny_apeture = 3

poly_acc = 3

def main():
    global res_gray, res_smooth, canny, contour_in, contour_out, c_storage, a_storage

    orig = cv.LoadImageM(INPUT)

    newX = RES_X
    newY = int(float(newX) / orig.cols * orig.rows)

    res = cv.CreateMat(newY, newX, cv.CV_8UC3)
    res_gray = cv.CreateMat(newY, newX, cv.CV_8UC1)
    res_smooth = cv.CreateMat(newY, newX, cv.CV_8UC1)
    canny = cv.CreateMat(newY, newX, cv.CV_8UC1)
    contour_in = cv.CreateMat(newY, newX, cv.CV_8UC1)
    contour_out = cv.CreateMat(newY, newX, cv.CV_8UC3)
    c_storage = cv.CreateMemStorage()
    a_storage = cv.CreateMemStorage()
    cv.NamedWindow('Canny', cv.CV_WINDOW_NORMAL)
    cv.NamedWindow('Contours', cv.CV_WINDOW_NORMAL)

    cv.CreateTrackbar('smooth', 'Canny', 3, 10, smooth_callback)
    cv.CreateTrackbar('apeture', 'Canny', 0, 2, canny_apeture_callback)
    cv.CreateTrackbar('lowThreshold', 'Canny', 30, 100, canny_lo_callback)
    cv.CreateTrackbar('highThreshold', 'Canny', 70, 100, canny_hi_callback)
    cv.CreateTrackbar('poly acc', 'Contours', 300, 1000, poly_acc_callback)

    cv.Resize(orig, res)
    cv.CvtColor(res, res_gray, cv.CV_RGB2GRAY)
    cv.Copy(res, contour_out)

    smooth_callback(3)

    key = cv.WaitKey()
    while not key == ord('q'):
        key = cv.WaitKey()

def refresh_poly():
    global poly_acc, contours, a_storage
    polys = cv.ApproxPoly(contours, a_storage, cv.CV_POLY_APPROX_DP, poly_acc, -1)

    con = polys
    index = 0
    polyc = 0
    while not con == None:
        index += len(con)
        polyc += 1
        con = con.h_next()
    print '%d polygons'%polyc
    print '%d points'%index

    cv.SetZero(contour_out)
    cv.DrawContours(contour_out, polys, cv.Scalar(255, 0, 0), cv.Scalar(0, 0, 255), 99)

    cv.ShowImage('Contours', contour_out)


def refresh_canny():
    global res_smooth, canny, canny_lo, canny_hi, canny_apeture, contour_in, contour_out, c_storage, contours
    cv.Canny(res_smooth, canny, canny_lo, canny_hi, canny_apeture)
    cv.ShowImage('Canny', canny)
    cv.Copy(canny, contour_in)
    contours = cv.FindContours(contour_in, c_storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_NONE)
    refresh_poly()

def poly_acc_callback(value):
    global poly_acc
    poly_acc = value/100.0
    refresh_poly()

def smooth_callback(value):
    global res_gray, res_smooth
    value = value * 2 + 1
    cv.Smooth(res_gray, res_smooth, cv.CV_GAUSSIAN, value, value)
    refresh_canny()

def canny_lo_callback(value):
    global canny_lo
    canny_lo = value
    refresh_canny()

def canny_hi_callback(value):
    global canny_hi
    canny_hi = value
    refresh_canny()

def canny_apeture_callback(value):
    global canny_apeture
    canny_apeture = value * 2 + 3
    refresh_canny()

if __name__ == '__main__':
    main()