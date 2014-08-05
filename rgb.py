__author__ = 'mperkins'

__author__ = 'flg8r96'

from PIL import Image
import numpy
import glob, os

#file = "/Users/flg8r96/love.jpg"
#new_file = "/Users/flg8r96/love_gray.jpg"
#lined_file = "/Users/flg8r96/love_gray_lines.jpg"

#file = "/Users/flg8r96/bar.jpg"
#new_file = "/Users/flg8r96/bar_gray.jpg"
#lined_file = "/Users/flg8r96/bar_gray_lines.jpg"

im = Image.open(file)
width, height = im.size

grayscale = im.convert("L")
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
light = [0 for x in xrange(0, col_deviations)] # col in array
sumlight = [light for x in xrange(0, row_deviations)] # row in array



# search accross and then down for the grid line indexes
for row in range(1,gheight):
  for col in range(1,gwidth):

    # get current color value and add it to the sumlight for the grid that this pixel is in
    pixelrssi = grayscale.getpixel((col,row))
    #print "pixel for row/col: " +str(row) +"/" +str(col) +"-" +str(pixelrssi) +" col/row_cnt:" +str(col_cnt) +"/" +str(row_cnt)

    sumlight[row_cnt][col_cnt] += pixelrssi

    if row%(gheight/row_deviations) == 0:
      #print "row/col: " +str(row) +"/" +str(col)
      # increment row_cnt
      if col == 1:
          col_cnt += 1
      grayscale.putpixel((col,row), 0) # black horizontal line

    else:
      #print "Not a mod! row/col: " + str(row) +"/" +str(col)
      #print "col mod gwidth/9 = " +str(col%(gwidth/9)) +" because col:" +str(col) +" gwidth:" +str(gwidth)
      if col%(gwidth/row_deviations) == 0:
        #print "Changing a col pixel"
        grayscale.putpixel((col,row), 0) # black vertical line
        # increment col_cnt
        if row == 1:
            row_cnt += 1

  # increment row_cnt
  #row_cnt += 1


#msg = grayscale.save("/Users/flg8r96/love_gray_lines.jpg")
msg = grayscale.save(lined_file)
print "Error in writing file: " +str(msg)
print "row_cnt/col_cnt:" +str(row_cnt) +"/" +str(col_cnt)
print sumlight

#determine how many pixels are in each square
row_pixels = gheight/row_deviations
col_pixels = gwidth/col_deviations
pixels_per_square = row_pixels * col_pixels
#norm_sumlight = [ x/10 for x in sumlight]
norm_sumlight = numpy.divide(sumlight,pixels_per_square*255)
print norm_sumlight