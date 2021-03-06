#!/usr/bin/python

#https://stackoverflow.com/questions/42381009/convert-arbitrary-bytes-to-any-lossless-common-image-format
#http://www.imagemagick.org/discourse-server/viewtopic.php?t=31451
#https://superuser.com/questions/294270/how-to-view-raw-binary-data-as-an-image-with-given-width-and-height

#https://askubuntu.com/questions/147554/what-software-can-display-raw-bitmaps-on-linux

#palette
#https://www.imagemagick.org/discourse-server/viewtopic.php?t=24682

#http://www.imagemagick.org/discourse-server/viewtopic.php?f=1&t=24193&hilit=clut

ver="4"

imgfmt="png"

import sys, struct, os, md5, hashlib
fileName = "Mili_chaohu.res_3.0."+ver
if len(sys.argv) == 2:
    fileName = sys.argv[1]

#with open('abc.dat', 'rb') as fobj:
#    byte_string, n1, n4 = struct.unpack('4sbI', fobj.read(12)) 
#https://docs.python.org/3/library/struct.html#format-strings

if not os.path.exists("_"+fileName):
    os.mkdir("_"+fileName)

strings_cn = {
    181: "1",
    182: "3",
    183: "2",
    184: "5",
    185: "6",
    186: "Week",
    187: "4",
    188: "Day",

    #timer menu
    112: "B sync'ed",
    #360: "Bsync",
    113: "x disconn",
    #361: "xoff",

    #Main menu
    294: "Alarm",
    296: "Compass",
    298: "Setup",
    300: "Activity",
    302: "Status",
    304: "Timer",
    306: "Weather",

    #timer menu
    308: "Countdown",
    310: "Stop\nwatch",

    #Activity menu
     94: "Sports set",
    317: "Riding",
    319: "History",
    321: "Indoor\nrun",
    323: "Outdoor\nrun",
    325: "Walking"

    #345-362 Cinese2

}


def get_rsrc_addr(idx):
	ptr = (4 * idx + 0x14)
	buf = [ ord(elem) for elem in fileContent[ptr:ptr+4]]
	addr = (buf[0] <<0) + (buf[1] <<8) + (buf[2] << 16) + (buf[3] <<24)
	return addr

def gen_raw():

	bpp = "identify -format '%[bit-depth]' 200_4.png"
	bpp = "identify -format '%[width]' 200_4.png"
	bpp = "identify -format '%[height]' 200_4.png"

	cmd = "convert 000_4.png -depth 8 -format '%c' histogram:info:-"
	os.system(cmd)


def get_bmp(idx):

	start = offs + get_rsrc_addr(idx)
	if idx < max_rsrc:
	    end = offs + get_rsrc_addr(idx + 1)
	else:
	    end = -1

	if fileContent[start:start+2] != "BM":
	    print "ERROR: %d isn't a bitmap resource" % idx
	    return 1

	m = hashlib.md5()
	m.update(fileContent[start:end])
	#filename = "%03d_%s_%s.bmp" % (idx, m.hexdigest(), ver)

	unk = ord(fileContent[start+8:start+9])

	width = ord(fileContent[start+4:start+5])
	height = ord(fileContent[start+6:start+7])

	depth = ord(fileContent[start+0xa:start+0xb])

	print "idx: %d - depth %d bpp - w: %d - h: %d - ??? %d " % (idx, depth, width, height, unk)

	filename = "_"+fileName +  os.path.sep + "%03d_%s" % (idx, ver)
	palette_len = ord(fileContent[start+12:start+13])
	#print DEBUG: palette_len=%d" % palette_len

	newFile = open(filename+".raw", "wb")
	#newFile = open(str(start)+"_"+str(end)+".bmp", "wb")
	#newFile = open("idx_"+str(idx)+"_"+str(start)+".bmp", "wb")
	# write to file
	newFile.write(fileContent[start:end])
	newFile.close()

	#newFile = open(filename+".raw", "wb")
	#newFile = open(str(start)+"_"+str(end)+".bmp", "wb")
	#newFile = open("idx_"+str(idx)+"_"+str(start)+".bmp", "wb")
	# write to file
	#newFile.write(fileContent[start+16+ ( palette_len * 4) :end])
	#newFile.close()

	raw_image = fileContent[start+16+ ( palette_len * 4) :end]
	raw_image_size = len(raw_image)

	#cmd = "convert -size "+str(width)+"x"+str(height)+"+"+str(16 + palette_len * 4) +" -depth 8 -format GRAY rgb:"+filename+".raw " +filename+".png"

	#working
	#cmd = "convert -size "+str(width)+"x"+str(height)+"+"+str(16 + palette_len * 4) +" -depth 8  -alpha off -compress NONE -scale 800% gray:"+filename+".raw " +filename+"." + imgfmt

	#right proportion zoomed
	#cmd = "convert -size "+str(width)+"x"+str(height)+"+"+str(16 + palette_len * 4) +" -depth " + str(depth) + "   -alpha off -compress NONE -scale 800% gray:"+filename+".raw " +filename+"." + imgfmt

	#right size unscaled
	#cmd = "convert -size "+str(width)+"x"+str(height)+"+"+str(16 + palette_len * 4) +" -depth " + str(depth) + "   -alpha off -compress NONE gray:"+filename+".raw " +filename+"." + imgfmt

	if idx in list(strings_cn.keys()):
		string = strings_cn[idx]
		cmd = "convert -depth " + str(depth) + "  -alpha off -compress NONE -background black -fill white -font DejaVu-Sans -gravity center -pointsize 9 -size "+str(width)+"x"+str(height)+"  label:\"" + string + "\" " +filename+"." + imgfmt +" 2>/dev/null"
		os.system(cmd)
	else:
		palfile = open(filename+".pal","w")
		for i in range(palette_len):
		    #print "i: %x" %(16 + i)
		    r=ord(fileContent[start+16+ ( 4*i+0):start+16+ ( 4*i+1)])
		    g=ord(fileContent[start+16+ ( 4*i+1):start+16+ ( 4*i+2)])
		    b=ord(fileContent[start+16+ ( 4*i+2):start+16+ ( 4*i+3)])
		    a=ord(fileContent[start+16+ ( 4*i+3):start+16+ ( 4*i+4)])
		    #print "DEBUG: rgb(%d,%d,%d)" %(r,g,b)
		    if a != 0:
			print "DEBUG: alpha(%d)" %a
		    palfile.write("xc:rgb(%d,%d,%d)\n" % ( r,g,b))
		palfile.close()
		cmd="convert @"+filename+".pal +append "+filename+"clut.png"
		#print "DEBUG: %s" % cmd
		os.system(cmd)
		#print "DEBUG: removing "+filename+".pal"
		os.unlink(filename+".pal")

		cmd = "convert -size "+str(width)+"x"+str(height)+"+"+str(16 + palette_len * 4) +" -depth " + str(depth) + "   -alpha off -compress NONE gray:"+filename+".raw "+filename+"clut.png -clut " +filename+"." + imgfmt
		#print "DEBUG: %s" % cmd
		os.system(cmd)
		#print "DEBUG: removing "+filename+".pal"
		os.unlink(filename+"clut.png")


with open(fileName, mode='rb') as file: # b is important -> binary
    fileContent = file.read()
    #https://docs.python.org/3/library/struct.html#format-strings
    fileHeader, version, dummy1, dummmy2 = struct.unpack('5sbHL', fileContent[0:16]) 

    if fileHeader != "HMRES":
	print "file isn't a resource file. Exiting"
	os.exit(1)
    print "file is a Haumi resource file"
    print "version??? %d" % version

    buf = [ ord(elem) for elem in fileContent[0x10:0x10+4]]
    max_rsrc = (buf[0] <<0) + (buf[1] <<8) + (buf[2] << 16) + (buf[3] <<24)

    print "number of resources: %d" % max_rsrc

    offs = 4 * max_rsrc + 0x14

    #extract all bitmap and translate the one in the list
    extract_list = range(max_rsrc)

    #TODO: add an if to enable translation

    #create only translate bitmap
    #extract_list = strings_cn.keys()

    for index in extract_list:

	addr = get_rsrc_addr(index)
        print "resource %3d | addr: %x | pos on file: %x" % ( index, addr, offs + addr )

	#sys.stdout.write('.')
	#sys.stdout.flush()

	get_bmp(index)



