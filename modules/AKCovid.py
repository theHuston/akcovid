import argparse
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
from modules import Location

scale_size = 1

# Set up the correct display and scaling factors
inky_display = InkyPHAT("red")

inky_display.set_border(inky_display.BLACK)

width = inky_display.WIDTH
height = inky_display.HEIGHT

img = Image.new("P", (width, height))
draw = ImageDraw.Draw(img)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
science_font = ImageFont.truetype('/home/pi/akcovid/resources/fonts/Science_Icons.ttf', 22)
fat_font = ImageFont.truetype('/home/pi/akcovid/resources/fonts/04b_30/04B_30__.TTF', 12)
vcr_font = ImageFont.truetype('/home/pi/akcovid/resources/fonts/vcr_osd_mono/VCR_OSD_MONO_1.001.ttf', 11)
big_vcr_font = ImageFont.truetype('/home/pi/akcovid/resources/fonts/vcr_osd_mono/VCR_OSD_MONO_1.001.ttf', 15)

#minecraft_font = ImageFont.truetype('/home/pi/akcovid/resources/fonts/8bit_wonder/8-BIT WONDER.TTF', 11)
pixelmix_font_tiny = ImageFont.truetype('/home/pi/akcovid/resources/fonts/pixelmix/pixelmix.ttf', 7)
pixelmix_font = ImageFont.truetype('/home/pi/akcovid/resources/fonts/pixelmix/pixelmix.ttf', 8)
pixelmix_font_bold = ImageFont.truetype('/home/pi/akcovid/resources/fonts/pixelmix/pixelmix_bold.ttf', 10)

intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding_x = 10
padding_y = 5
padding_y_small = 4
top = padding_y
bottom = height-padding_y

#Text Heights
small_text_height = 9

#Header vars
header_height = 19

#Table Header vars
table_header_start_y = header_height+padding_y
table_header_height = 12
table_header_padding = 3

table_width = width-padding_x

table_col_1_width = table_width - 100
table_col_2_width = (table_width-table_col_1_width)/2
table_col_3_width = (table_width-table_col_1_width)/2

#print("W:"+str(width)+" TW:"+str(table_width)+" T1:"+str(table_col_1_width)+" T2:"+str(table_col_2_width)+" T3:"+str(table_col_3_width)+" TOT:"+str(table_col_1_width+table_col_2_width+table_col_3_width))

# Move left to right keeping track of the current x position for drawing shapes.
left = padding_x
right = width-padding_x

#Variables for updates
last_update = "0/0/0"

locations=list()

loc_1 = 0
loc_2 = 0
loc_3 = 0

ak_total = 0
ak_total_confirmed = 0
ak_total_pending = 0
ak_total_travel = 0
ak_total_local = 0
us_total = 0

global number_spots

def makeScreen():

    print("Starting new update on "+last_update)

    draw_header()
    draw_table_header()
    draw_table_content()
    #draw_table_arrows()
    draw_footer()

    # Display the logo image
    inky_display.set_image(img)
    inky_display.show()

#Function to make text
def draw_header():

    #Draw Header Background
    draw.rectangle((0, 0, width, header_height), fill=inky_display.RED)
    draw.rectangle((0, header_height, width, header_height), outline=inky_display.BLACK)

    #Draw Header Title Text
    draw.text((left-2, top-8), 'F', font=science_font, fill=inky_display.WHITE)
    draw.text((left+20, top), 'COVID-19', font=fat_font, fill=inky_display.WHITE)

    draw.text((left+135, header_height-padding_y-5), 'AK | '+last_update, font=pixelmix_font_tiny, fill=inky_display.WHITE)

def draw_table_header():

    #first Column
    draw.rectangle((left, table_header_start_y+table_header_height, table_col_1_width, table_header_start_y+table_header_height), outline=inky_display.BLACK)

    #Second Column
    draw.rectangle((table_col_1_width, table_header_start_y, left+table_col_1_width+table_col_2_width, table_header_start_y+table_header_height), outline=inky_display.BLACK, fill=inky_display.BLACK)

    #Third Column
    draw.rectangle((table_col_1_width+table_col_2_width, table_header_start_y, table_col_1_width+table_col_2_width+table_col_3_width, table_header_start_y+table_header_height), outline=inky_display.BLACK, fill=inky_display.RED)

    #Draw Labels
    draw.text((left+1, table_header_start_y+table_header_padding), 'REGION', font=pixelmix_font_tiny, fill=inky_display.BLACK)
    draw.text((table_col_1_width+9, table_header_start_y+table_header_padding), 'PENDING', font=pixelmix_font_tiny, fill=inky_display.WHITE)
    draw.text((table_col_1_width+table_col_2_width+3, table_header_start_y+table_header_padding), 'CONFIRMED', font=pixelmix_font_tiny, fill=inky_display.WHITE)

def draw_table_arrows():
    draw.polygon([(number_spots[0].travel_x, number_spots[0].travel_x), (number_spots[0].travel_x, number_spots[0].travel_x+5), (number_spots[0].travel_x+5, number_spots[0].travel_x+5)], fill=inky_display.BLACK)

def draw_table_content():

    number_spots=list()

    #insert table content
    #Anchorage
    draw.text((left+2, table_header_start_y+table_header_height+padding_y), locations[loc_1].name, font=pixelmix_font, fill=inky_display.BLACK)
    draw.text((table_col_1_width+(table_col_2_width/2), table_header_start_y+table_header_height+padding_y), str(locations[loc_1].pending), font=pixelmix_font, fill=inky_display.BLACK)
    draw.text((table_col_1_width+table_col_2_width+(table_col_3_width/2), table_header_start_y+table_header_height+padding_y), str(locations[loc_1].confirmed), font=pixelmix_font, fill=inky_display.BLACK)

    loc_1_number_loc = Number_Locations(
    table_col_1_width+(table_col_2_width/2),
    table_header_start_y+table_header_height+padding_y,
    table_col_1_width+table_col_2_width+(table_col_3_width/2),
    table_header_start_y+table_header_height+padding_y)

    number_spots.append(loc_1_number_loc)

    #print("x:"+str(number_spots[0].travel_x)+" | y:"+str(number_spots[0].travel_y))

    #first Line
    draw.rectangle((left, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1), table_width, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1)), outline=inky_display.BLACK)

    #Gulf Area
    draw.text((left+2, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1)+padding_y_small), locations[loc_2].name, font=pixelmix_font, fill=inky_display.BLACK)
    draw.text((table_col_1_width+(table_col_2_width/2), table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1)+padding_y_small), str(locations[loc_2].pending), font=pixelmix_font, fill=inky_display.BLACK)
    draw.text((table_col_1_width+table_col_2_width+(table_col_3_width/2), table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1)+padding_y_small), str(locations[loc_2].confirmed), font=pixelmix_font, fill=inky_display.BLACK)

    loc_2_number_loc = Number_Locations(table_col_1_width+(table_col_2_width/2),
    table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1)+padding_y_small,
    table_col_1_width+table_col_2_width+(table_col_3_width/2),
    table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*1)+padding_y_small
    )

    number_spots.append(loc_2_number_loc)


    #Second Line
    draw.rectangle((left, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*2)+padding_y_small, table_width, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*2)+padding_y_small), outline=inky_display.BLACK)

    #Matsu Area
    draw.text((left+2, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*2)+(padding_y_small*2)), locations[loc_3].name, font=pixelmix_font, fill=inky_display.BLACK)
    draw.text((table_col_1_width+(table_col_2_width/2), table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*2)+(padding_y_small*2)), str(locations[loc_3].pending), font=pixelmix_font, fill=inky_display.BLACK)
    draw.text((table_col_1_width+table_col_2_width+(table_col_3_width/2), table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*2)+(padding_y_small*2)), str(locations[loc_3].confirmed), font=pixelmix_font, fill=inky_display.BLACK)

def draw_footer():

    #Second Line
    draw.rectangle((0, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*3)+padding_y_small+padding_y, width, height), fill=inky_display.RED)
    draw.rectangle((0, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*3)+padding_y_small+padding_y, width, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*3)+padding_y_small+padding_y), outline=inky_display.BLACK)

    #draw.text((right-51, height-11), "IN AK | "+str(ak_total),  font=pixelmix_font, fill=inky_display.WHITE)
    draw.text((left, height-11), "PEND "+str(ak_total_pending)+" | CONFIRM "+str(ak_total_confirmed)+" | TOTAL "+str(ak_total),  font=pixelmix_font, fill=inky_display.WHITE)

# Define location class
class Number_Locations:
    def __init__(self, travel_x, travel_y, local_x, local_y):
        self.travel_x = travel_x
        self.travel_y = travel_y
        self.local_x = local_x
        self.local_y = local_y
