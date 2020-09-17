
# REPEATED SONGS $10K EMAIL '2019'
#------------------------------------
# Not long ago, GOLD FM, a radio in Melbourne had a contest
# if they repeated a song between 6am and 6pm and you call them
# you would win $10.000
# Here's a little script that gets the current song they are playing
# via their webpage, and compares it to all the ones that have been
# played. If a song has been played twice, you will get an email
# telling you to call them and get those $10K!

# This project requires a webdriver, I use firefox to do it as I use
# chrome for my daily browsing (and this way they don't interfere)
# The webdriver allows to get information even if the fields are populated via javascript

# Disclaimer: I did not win! 
# The few seconds between the start of the song and receiving the email were enough for other people to have called. 


# -- Imports ----------------------------------------------------------

from selenium import webdriver
import time
import datetime
import smtplib, ssl
from email.mime.text import MIMEText


# -- Obtain current song ----------------------------------------------
# this is set to work with the above mentioned example but can be easily modified

def get_song(driver):
    
    # get the full HTML (including java populated fields) for the webpage where the current song is displayed
    webpage = driver.execute_script("return document.body.innerHTML")

    # Manually find where that song is in the HTML
    pos = webpage.find('po-audio-player__component-on-air__name')

    # String containing the name of the song (and artist)
    song_string = webpage[pos:pos+100]

    song = song_string.split("title=")[1].split(">")[0].replace('"','')

    return song


# -- Send email via python --------------------------------------------
# this is configured for a gmail account

def send_email(song_txt, past_song):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "sender@gmail.com"  # Enter your address
    receiver_email = "receiver@gmail.com"  # Enter receiver address
    password = "password_here"

    msg = MIMEText(song_txt + ' \n ' + past_song)
    msg['Subject'] = '$10K ' + song_txt
    msg['From'] = sender_email
    msg['To'] = receiver_email
    

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# ---------------------------------------------------------------------
# -- MAIN TEXT --------------------------------------------------------
# ---------------------------------------------------------------------


if False:
    # webpage where the song is displayed
    url = 'https://www.gold1043.com.au/'
    
    driver = webdriver.Firefox()
    driver.get(url)

    time.sleep(10)


#----------------------------------------------------------------------
# -------- main function goes here ------------------------------------
#----------------------------------------------------------------------


if False:

    played_songs = []
    last_song = 'very_first_song'

    

    while True:

        # if we're between 6am and 6pm
        if datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 18:

        	# only very beggining of the song
            if last_song == 'very_first_song':
                print("STARTING_NOW -- " + str(datetime.datetime.now().hour)+
                	':' + str(datetime.datetime.now().minute))

            song = get_song(driver)

            if (song != 'iHeartRadio') and (song != last_song):
                
                # -- format text to save -----------------------------

                hh = str(datetime.datetime.now().hour)
                mm = str(datetime.datetime.now().minute)
                if len(mm) < 2: mm = '0' + mm
                song_txt = song + ' -- ' + hh + ':' + mm


                # -- ARE WE RICH ? ------------------------------------

                gold = [i for i in played_songs if song in i]

                # -- send email here ----------------------------------
                if len(gold) > 0:
                    print('$$$$$$$$$ $10K EMAIL $$$$$$$$$')
                    send_email(song_txt, str(gold))

                
                # -- if we are not rich, let's save the song ---------
                # -- Save Results ------------------------------------

                # append song to played_songs
                played_songs.append(song_txt)

                # append song to txt_file
                with open('songs.txt', 'a+', 1) as f:
                    f.write(song_txt + '\n')

                # print in screen
                print(song_txt)


                # -- move to next iteration ---------------------------
                last_song = song
                time.sleep(10)

            else: # same song or ads scenario 
                time.sleep(10)


        else: # not during the proper time
            time.sleep(60)




































