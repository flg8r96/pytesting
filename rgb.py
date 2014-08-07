__author__ = 'mperkins'

__author__ = 'flg8r96'

import traceback
from PIL import Image
import numpy
import glob, os
# documentation for PIL:
# http://effbot.org/imagingbook/image.htm

#file = "/Users/flg8r96/love.jpg"
#new_file = "/Users/flg8r96/love_gray.jpg"
#lined_file = "/Users/flg8r96/love_gray_lines.jpg"

#file = "/Users/flg8r96/bar.jpg"
#new_file = "/Users/flg8r96/bar_gray.jpg"
#lined_file = "/Users/flg8r96/bar_gray_lines.jpg"

file = "/Users/mperkins/awarepoint_logo.jpg"
new_file = "/Users/mperkins/awarepoint_logo_gray.jpg"
lined_file = "/Users/mperkins/awarepoint_logo_gray_lines.jpg"
pxl_file = "/Users/mperkins/awarepoint_logo_pixelated.jpg"

#file = "/Users/mperkins/checker_large.gif"
#new_file = "/Users/mperkins/checker_large_gray.gif"
#lined_file = "/Users/mperkins/checker_large_gray_lines.gif"

#file = "/Users/mperkins/flame.jpg"
#new_file = "/Users/mperkins/flame_gray.jpg"
#lined_file = "/Users/mperkins/flame_gray_lines.jpg"

im = Image.open(file)
width, height = im.size

#grayscale = im.convert("L")     #grayscale
grayscale = im.convert("1")     #black and white
print grayscale
#msg = grayscale.save("/Users/flg8r96/love_gray.jpg")
msg = grayscale.save(new_file)
print "Error in writing file: " +str(msg)
gwidth, gheight = grayscale.size
print "Grayscale size: " + str(gwidth) +"x" +str(gheight)


row_deviations = 10
col_deviations = 10

col_cnt = 0
row_cnt = 0

# create an array of summed pixel values
# initialize the array
#light = [0 for x in xrange(0, col_deviations)] # col in array
#sumlight = [light for x in xrange(0, row_deviations)] # row in array
sumlight = [[0]*col_deviations for x in range(row_deviations)] # row in array



# search accross and then down for the grid line indexes
for row in xrange(0, gheight):
    col_cnt = 0;
    for col in xrange(0, gwidth):

        # get current color value and add it to the sumlight for the grid that this pixel is in
        pixelrssi = grayscale.getpixel((col, row))

        # not sure this does a damn thing
        if col_cnt == 0 and row%(gheight/row_deviations) != 0 and col == gwidth-1:
            row_cnt += 1

        #print "pixel for col/row: "  +str(col) +"/" +str(row) +"-" +str(pixelrssi) +" col_cnt/row_cnt:"  +str(col_cnt) +"/" +str(row_cnt)
        if pixelrssi > 250:
            # add nothing if white
            a = float(0)

        else:
            # add 1 if black
            a = float(1)
            # row and col are flipped when referencing the array
        sumlight[row_cnt][col_cnt] += 255 - float(pixelrssi)
            #sumlight[row_cnt][col_cnt] += a

        #sumlight[col_cnt][row_cnt] += pixelrssi/float(255)
        #sumlight[col_cnt][row_cnt] += a

        # draw horizontal line on the image to see where the larger pixels are located
        if row%(gheight/row_deviations) == 0:
            #print "row/col: " +str(row) +"/" +str(col)
            grayscale.putpixel((col, row), 0) # black horizontal line
            # increment row_cnt but don't do it after the first real pixel row
            if col == 0 and row != 0:
                row_cnt += 1

        if col%(gwidth/col_deviations) == 0:
            #print "Changing a col pixel"
            grayscale.putpixel((col, row), 0) # black vertical line
            # increment col_cnt
            if col != 0:
                col_cnt += 1

#msg = grayscale.save("/Users/flg8r96/love_gray_lines.jpg")
msg = grayscale.save(lined_file)
print "Error in writing file: " +str(msg)
print "row_cnt/col_cnt:" +str(row_cnt) +"/" +str(col_cnt)
print sumlight

#determine how many pixels are in each square
row_pixels = gheight/float(row_deviations)
col_pixels = gwidth/float(col_deviations)
pixels_per_square = row_pixels * col_pixels
#norm_sumlight = [ x/10 for x in sumlight]
norm_sumlight = numpy.divide(sumlight,pixels_per_square)
#print norm_sumlight

norm_sumlight = numpy.around(norm_sumlight, decimals=0)
print norm_sumlight

raw_input("enter")

print "Starting to create the pixelated file"
pixelated = Image.new("L",(gwidth,gheight), color=None)
# write this out to a pixelated file of equal size as the original
for row in xrange(0, gheight):
    col_cnt = 0;
    for col in xrange(0, gwidth):

        # get current color value and add it to the sumlight for the grid that this pixel is in
#try:
    #if norm_sumlight[row_cnt][col_cnt] != 0:
        print col_cnt, row_cnt
        val1 = (norm_sumlight[row_cnt][col_cnt])
        val2 = val1*255/101
        val = int(val2)
        print val1, val2, val
        if val > 128:
            raw_input("ENTER")
        #print val
        pixelated.putpixel((col, row), val)   # black pixel
        print "pixel for col/row: "  +str(col) +"/" +str(row) +"-" +str(val1) +str("..") +str(val)  +" col_cnt/row_cnt:"  +str(col_cnt) +"/" +str(row_cnt)
    #else:
    #    pixelated.putpixel((col, row), 255) # white pixel
#except Exception, err:
    #print traceback.format_exc()

        # not sure this does a damn thing
        #if col_cnt == 0 and row%(gheight/row_deviations) != 0 and col == gwidth-1:
        #    row_cnt += 1

        # draw horizontal line on the image to see where the larger pixels are located
        """if row%(gheight/row_deviations) == 0:
            if col == 0 and row != 0:
                row_cnt += 1
"""
        if col%(gwidth/col_deviations) == 0:
            if col != 0:
                col_cnt += 1
                #raw_input("enter")

try:
    msg2 = pixelated.save(pxl_file)
except Exception, err:
    print traceback.format_exc()
    print "Save of pixelated file didn't work"