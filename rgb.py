__author__ = 'mperkins'

__author__ = 'flg8r96'

import traceback
from PIL import Image
import numpy
import glob, os
# documentation for PIL:
# http://effbot.org/imagingbook/image.htm

class Pixelate:
    def __init__(self, *args,**kwargs):
        self.args = args
        self.kwargs = kwargs
        self.file = self.kwargs['file']
        self.new_file = self.kwargs['new_file']
        self.lined_file = self.kwargs['lined_file']
        self.pxl_file = self.kwargs['pxl_file']
        print self.kwargs
        print self.file

    def pixelatefile(self):
        im = Image.open(self.file)
        width, height = im.size

        gray = im.convert("L")     #grayscale
        #gray = im.convert("1")     #black and white
        print gray
        msg = gray.save(self.new_file)
        print "Error in writing file: " +str(msg)
        gwidth, gheight = gray.size
        print "gray size: " + str(gwidth) +"x" +str(gheight)

        new_width = 0
        new_height = 0
        # if the image size isn't divisible by 16 and 32 on width and height we need to crop the image
        if height%32 == 0:
            row_deviations = 32
        else:
            for max_hpixel in range(height, height - 32,-1):
                #print "maxhpixel: " +str(max_hpixel)
                if max_hpixel%32 == 0:
                    row_deviations = 32
                    new_height = max_hpixel

        if width%16 == 0:
            col_deviations = 16
            print "asdflj"
        else:
            # figure out how to cut the pixels
            for max_wpixel in range(width, width - 16,-1):
                #print "maxwpixwl: " +str(max_wpixel)
                if max_wpixel%16 == 0:
                    col_deviations = 16
                    print "ysasdf"
                    new_width = max_wpixel

        #adjust the image
        if new_height:
            hpixel_diff = height - new_height
            print hpixel_diff
            if hpixel_diff%2 != 0:
                hrange = range(hpixel_diff/2,height - hpixel_diff/2)
            else:
                hrange = range(hpixel_diff/2,height - hpixel_diff/2 + 1)
        if new_width:
            wpixel_diff = width - new_width
            if wpixel_diff%2 != 0:
                wrange = range(wpixel_diff/2,width - wpixel_diff/2)
            else:
                wrange = range(wpixel_diff/2,width - wpixel_diff/2 + 1)

        #print hrange
        if new_width and new_height:
            grayscale = Image.new("L",(new_width,new_height), color=None)
            for a in range(hrange[:]):
                for b in range(wrange[:]):
                    grssi = gray.getpixel((b, a))
                    grayscale.putpixel((b, a), grssi)
        elif new_width and not new_height:
            grayscale = Image.new("L",(new_width,height), color=None)
            for a in range(height):
                for b in range(wrange[:]):
                    grssi = gray.getpixel((b, a))
                    grayscale.putpixel((b, a), grssi)
        elif not new_width and new_height:
            grayscale = Image.new("L",(width,new_height), color=None)
            print grayscale.size
            print hrange
            n = hrange[hrange.__len__()-1]-1
            q = hrange[0]+1
            print q, n
            for a in range(q,n):
                for b in range(width):
                    grssi = gray.getpixel((b, a))
                    #print a, b
                    grayscale.putpixel((b, a-hrange[0]), grssi)




        col_cnt = 0
        row_cnt = 0
        gwidth, gheight = grayscale.size
        print gwidth, gheight
        print col_deviations, row_deviations
        #row_deviations = 4
        #col_deviations = 4
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
                #print row_cnt, col_cnt
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
        msg = grayscale.save(self.lined_file)
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
            msg2 = pixelated.save(self.pxl_file)
            msg = "Pixelated file saved!"
            print msg
        except Exception, err:
            print traceback.format_exc()
            msg = "Save of pixelated file didn't work"
            print msg

        return msg

def main():
    file = "/Users/flg8r96/development/pytesting/flamevideos/flame3_10_0001.jpg"
    new_file = "/Users/flg8r96/development/pytesting/flamevideos/flame3_10_0001_gray.jpg"
    lined_file = "/Users/flg8r96/development/pytesting/flamevideos/flame3_0001_10_gray_lines.jpg"
    pxl_file = "/Users/flg8r96/development/pytesting/flamevideos/flame3_0001_10_gray_pixel.jpg"

    t = Pixelate(file=file,
                new_file=new_file,
                lined_file=lined_file,
                pxl_file=pxl_file)
    print "Calling Pixelate"
    t.pixelatefile()

if __name__ == "__main__":
    print "Main:In __name__ of main()"
    main()
