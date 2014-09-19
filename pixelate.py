__author__ = 'mperkins'

__author__ = 'flg8r96'

import traceback
from PIL import Image
import numpy
import glob, os
# documentation for PIL:
# http://effbot.org/imagingbook/image.htm

file = "/Users/flg8r96/development/pytesting/flamevideos/flame2_0001.jpg"
new_file = "/Users/flg8r96/development/pytesting/flamevideos/flame2_0001_gray.jpg"
lined_file = "/Users/flg8r96/development/pytesting/flamevideos/flame2_0001_gray_lines.jpg"
pxl_file = "/Users/flg8r96/development/pytesting/flamevideos/flame2_0001_gray_pixel.jpg"

#file = "/Users/flg8r96/love.jpg"
#new_file = "/Users/flg8r96/love_gray.jpg"
#lined_file = "/Users/flg8r96/love_gray_lines.jpg"
#pxl_file = "/Users/flg8r96/love_gray_pixel.jpg"

#file = "/Users/flg8r96/a.jpg"
#new_file = "/Users/flg8r96/a_gray.jpg"
#lined_file = "/Users/flg8r96/a_gray_lines.jpg"
#pxl_file = "/Users/flg8r96/a_gray_pixel.jpg"

#file = "/Users/flg8r96/bar.jpg"
#new_file = "/Users/flg8r96/bar_gray.jpg"
#lined_file = "/Users/flg8r96/bar_gray_lines.jpg"

#file = "/Users/mperkins/awarepoint_logo.jpg"
#new_file = "/Users/mperkins/awarepoint_logo_gray.jpg"
#lined_file = "/Users/mperkins/awarepoint_logo_gray_lines.jpg"
#pxl_file = "/Users/mperkins/awarepoint_logo_pixelated.jpg"

#file = "/Users/mperkins/checker_large.gif"
#new_file = "/Users/mperkins/checker_large_gray.gif"
#lined_file = "/Users/mperkins/checker_large_gray_lines.gif"

#file = "/Users/mperkins/flame.jpg"
#new_file = "/Users/mperkins/flame_gray.jpg"
#lined_file = "/Users/mperkins/flame_gray_lines.jpg"

im = Image.open(file)
width, height = im.size

grayscale = im.convert("L")     #grayscale
#grayscale = im.convert("1")     #black and white
print grayscale
#msg = grayscale.save("/Users/flg8r96/love_gray.jpg")
msg = grayscale.save(new_file)
print "Error in writing file: " +str(msg)
gwidth, gheight = grayscale.size
print "Grayscale size: " + str(gwidth) +"x" +str(gheight)


row_deviations = 71
col_deviations = 8

col_cnt = 0
row_cnt = 0

# create an array of summed pixel values
# initialize the array - HOW THIS ARRAY IS CREATED IS IMPORTANT
# IF YOU DON'T CREATE THE ARRAY AS SHOWN BELOW, THE ELEMENTS CAN'T BE ACCESSED BY ROW/COL
sumlight = [[0]*col_deviations for x in range(row_deviations)] # row in array

##### Extract the pixels from the photo anc create an interpolated version
# row, col represent the row, col for each pixel in the original image
# row_cnt, col_cnt represent the pixels in the downsampled (pixelated) "image" - this image will be
# represented by the array of LEDs
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

        # THIS CAN BE USED TO CREATE A BLACK AND WHITE PIXEL GRID
        if pixelrssi < 254:
            # add nothing if white
            a = float(0)
        else:
            # add 1 if black
            a = float(255)
            #sumlight[row_cnt][col_cnt] += a


        # row and col are flipped when referencing the array
        #sumlight[row_cnt][col_cnt] += float(pixelrssi)
        sumlight[row_cnt][col_cnt] += float(a)

        # draw horizontal line on the image to see where the larger pixels are located
        if row%(gheight/row_deviations) == 0:
            grayscale.putpixel((col, row), 0) # black horizontal line
            # increment row_cnt but don't do it until after the first real pixel row
            if col == 0 and row != 0:
                row_cnt += 1

        if col%(gwidth/col_deviations) == 0:
            #print "Changing a col pixel"
            grayscale.putpixel((col, row), 0) # black vertical line
            if col != 0:
                col_cnt += 1

#
msg = grayscale.save(lined_file)
print "Error in writing file: " +str(msg)
print "row_cnt/col_cnt:" +str(row_cnt) +"/" +str(col_cnt)
print sumlight

#determine how many pixels are in each square
row_pixels = gheight/float(row_deviations)
col_pixels = gwidth/float(col_deviations)
pixels_per_square = row_pixels * col_pixels
norm_sumlight = numpy.divide(sumlight,pixels_per_square)
norm_sumlight = numpy.around(norm_sumlight, decimals=0)
print norm_sumlight

rssimax = norm_sumlight.max()
# pause the processing to visually inspect the result of the pixelated picture
#raw_input("enter")

# reconstruct a pixelated image for final inspection (this is what it will look like
# ... when the led array is used)
col_cnt=0
row_cnt=0
print "Starting to create the pixelated file"
pixelated = Image.new("L",(gwidth,gheight), color=None)
# write this out to a pixelated file of equal size as the original
for row in xrange(0, gheight):
    col_cnt = 0;
    for col in xrange(0, gwidth):

        # get current color value and add it to the sumlight for the grid that this pixel is in
        #print col_cnt, row_cnt, norm_sumlight[row_cnt][col_cnt]
        val = int((norm_sumlight[row_cnt][col_cnt])*255/rssimax)
        """if val < 127:
            pixelated.putpixel((col, row), 0)   # black pixel
        else:
            pixelated.putpixel((col, row), 255)   # black pixel
            """
        pixelated.putpixel((col, row), val)   # black pixel

        # draw horizontal line on the image to see where the larger pixels are located
        if row%(gheight/row_deviations) == 0:
            if col == 0 and row != 0:
                row_cnt += 1

        if col%(gwidth/col_deviations) == 0:
            if col != 0:
                col_cnt += 1

try:
    msg2 = pixelated.save(pxl_file)
    print "Pixelated file saved!"
except Exception, err:
    print traceback.format_exc()
    print "Save of pixelated file didn't work"