__author__ = 'flg8r96'

from rgb import Pixelate

def main():
    # check the director for files
    # go one at a time until all files have been pixelated
    dir = "/Users/flg8r96/development/pytesting/flamevideos/"
    filenameroot = "flame2_10_"
    start_index = 1
    end_index = 205
    file_ext = ".jpg"
    for index in range(start_index,end_index):
        file = dir + filenameroot +str("%04d" % index) + file_ext
        new_file = dir + filenameroot +"gray_" +str("%04d" % index) + file_ext
        lined_file = dir + filenameroot +"gray_lines_" +str("%04d" % index) + file_ext
        pxl_file = dir + filenameroot +"gray_lines_pixel_" +str("%04d" % index) + file_ext
        #print file
        t = Pixelate(file=file,
                new_file=new_file,
                lined_file=lined_file,
                pxl_file=pxl_file)
        print t.pixelatefile()

if __name__ == "__main__":
    print "Main:In __name__ of main()"
    main()