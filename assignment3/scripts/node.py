#!/usr/bin/env python

import numpy as np
import cv2 as cv
import time, sys
import rospy
import roslib
from sensor_msgs.msg import CompressedImage, Image

if __name__ == '__main__':
    rospy.init_node('image')
    image_pub = rospy.Publisher("/detected/debug_img", Image, queue_size=10)
    image_pub = rospy.Publisher("/detected/debug_img/compressed", CompressedImage, queue_size=10)
    
    def display(ros_data):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
        
        #pre-processing
        blurred_frame = cv.GaussianBlur(img, (5, 5), 0)
        
        
        #colour space changed to HSV
        img_hsv = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
        
        
        # thresholding
        mask = cv.inRange(img_hsv, (160, 20, 20), (200, 255, 255))
        
        #morphological operations
        kernel = np.ones((5,5),np.uint8)
        img_morph = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)     # SET OPERATOR
        
        #contouring
        image_new, contours, hierarchy = cv.findContours(img_morph, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)     # find contours
        
        #convert back to BGR
        image_with_colour = cv.bitwise_and(img, img, mask=mask)
        
        # draw all contours on original image
        img_contours = cv.drawContours(image_with_colour, contours, -1, (255,0,0), 4)
        
        #(bounding box filtering)
        for c in contours:
            rect = cv.boundingRect(c) # get the bounding box of this contour
            x, y, w, h = rect  # the bounding box is described with 4 numbers
            cv.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 3) # draw the rectangle on your image
            cv.putText(img_contours, str(cv.contourArea(c)), (x + 10, y - 10), 0, 0.7, (0, 255, 0)) # print its area
        
        #creating overlay of image
        mask_inv = cv.bitwise_not(mask)
        img1_bg = cv.bitwise_and(img,img, mask = mask_inv)
        dst = cv.add(img1_bg,img_contours)
        
        cv.imwrite("target.png", dst) #test
        
        #Publish your output to the topic '/detected/debug_img/compressed'
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "png"
        msg.data = np.array(cv.imencode('.png', dst)[1]).tostring()
        image_pub.publish(msg)
        
        #Publish your output to the topic '/detected/debug_img' as an Image.msg
        #msg = Image()
        #msg.header.stamp = rospy.Time.now()
        #msg.format = "png"
        #msg.data = np.array(cv.imencode('.png', image_with_colour)[1]).tostring()
        #image_pub.publish(msg)
        
    rospy.Subscriber('/auv/bot_cam/image_color/compressed', CompressedImage, display)

    rospy.spin()

    print("Shutting Down")
    print("Done")
    

