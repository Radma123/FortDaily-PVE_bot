import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import math
import telebot
#import datetime as dt
import logging
import os

#настройка логгирования
logging.basicConfig(
    level=logging.WARNING,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )
logging.warning('________________________________HELLO__________________________________')


# настройки для телеги
token = os.environ['TOKEN']
channel_id = os.environ['CHANNEL_ID']
#prx =  "http://proxy.server:3128"
bot = telebot.TeleBot(token, parse_mode='HTML')


#фейк замена для браузера
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}


#получение медиагруппы скинов для отправки в телегу
def daily_shop(): 
    response = requests.get('https://fnitemshop.com/',headers=header).text
    soup = BeautifulSoup(response,'lxml')
    block = soup.find('div',class_ ='entry-content single-content')
    magazine = block.find_all('p')[2:]
    print(magazine)
    
    mediaphoto_jpeg_skins = []

    k = 0
    for category in magazine:
        skins = category.find_all('a')
        if math.ceil(len(skins)/3) > 9:
            p1 = []
            p2 = []
            allpr = []
            dl = math.ceil(len(skins)/2) + len(skins)%2
            for i in range(len(skins)):
                if i <= (dl-1):
                    p1.append(skins[i])
                else:
                    p2.append(skins[i])
            allpr.append(p1)
            allpr.append(p2)
            for skins in allpr:
                dlina = 2196                       #background image(black wallpaper)
                visota = math.ceil(len(skins) / 3) * 732
                background_img = Image.new('RGB',(dlina,visota),'black')

                for skin1 in range(len(skins)):
                    k+=1
                    href = skins[skin1].get('href')
                    image_bytes = requests.get(href).content
                    pillow_image = Image.open(io.BytesIO(image_bytes))
                    pillow_image = pillow_image.resize((732, 732))
                    
                    paste_dlina = 0
                    paste_visota = 0

                    if k % 3 == 0:
                        paste_dlina = 1464
                    elif k % 3 == 2:
                        if skin1 == len(skins) - 1:
                            paste_dlina = 1098
                        else:
                            paste_dlina = 732
                    else: # k % 3 == 1
                        if skin1 == len(skins) - 2:
                            paste_dlina = 366
                        elif skin1 == len(skins) - 1:
                            paste_dlina = 732
                        else:
                            paste_dlina = 0
                    
                    paste_visota = math.ceil(k/3) * 732 - 732
                    background_img.paste(pillow_image,(paste_dlina,paste_visota))
                k = 0
                mediaphoto_jpeg_skins.append(background_img)
        else:
            dlina = 2196                       #background image(black wallpaper)
            # visota = (len(skins) // 3) * 731
            # if len(skins) % 3 != 0:
            #     visota += 731
            visota = math.ceil(len(skins) / 3) * 732
            background_img = Image.new('RGB',(dlina,visota),'black')

            for skin1 in range(len(skins)):
                k+=1
                href = skins[skin1].get('href')
                image_bytes = requests.get(href).content
                pillow_image = Image.open(io.BytesIO(image_bytes))
                pillow_image = pillow_image.resize((732, 732))
                
                paste_dlina = 0
                paste_visota = 0

                if k % 3 == 0:
                    paste_dlina = 1464
                elif k % 3 == 2:
                    if skin1 == len(skins) - 1:
                        paste_dlina = 1098
                    else:
                        paste_dlina = 732
                else: # k % 3 == 1
                    if skin1 == len(skins) - 2:
                        paste_dlina = 366
                    elif skin1 == len(skins) - 1:
                        paste_dlina = 732
                    else:
                        paste_dlina = 0
                
                paste_visota = math.ceil(k/3) * 732 - 732
                background_img.paste(pillow_image,(paste_dlina,paste_visota))
            k = 0
            mediaphoto_jpeg_skins.append(background_img)

    return mediaphoto_jpeg_skins




#получение str строки алертов
def check_alerts():
    alerts = ''
    link = 'https://fortnitedb.com/'
    response = requests.get(headers=header, url=link).text
    soup = BeautifulSoup(response, 'lxml')


    vbucksblock = soup.find('div', class_ = 'new_block_content').find_all('tr')

    try:        
        missions = []
        summary = 0
        for mission in vbucksblock:
            power = mission.find('td',class_ = 'right').text.strip()
            reward = mission.find('td',class_ = 'cell col mythic--border-small').text.strip()
            zna4 = int(''.join(reward).split('x')[0])
            summary += zna4
            location = ''
            if int(power) >= 1 and int(power) <= 19:
                if int(power) == 19:
                    location = 'Камнелесье/Планкертон'
                else:
                    location = 'Камнелесье'
            elif int(power) > 19 and int(power) <= 46:
                if int(power) == 46:
                    location = 'Планкертон/Вещая долина'
                else:
                    location = 'Планкертон'
            elif int(power) > 46 and int(power) <= 76:
                if int(power) == 76:
                    location = 'Вещая долина/Линч-Пикс'
                else:
                    location = 'Вещая долина'
            elif int(power) > 76:
                location = 'Линч-Пикс'
            missions.append(f'{location} {power}⚡ -> {zna4} V-Bucks')
        missions.append(f"<u>Всего: {summary} V-Bucks</u>")

        for mis in missions:
            alerts = alerts+'\n'+mis
        #print(alerts)
        return alerts
    except:
        return False
    


def sending():
    try:
        mediaphoto_jpeg_skins = daily_shop()
        if len(mediaphoto_jpeg_skins) < 11:
            mediagroup = [telebot.types.InputMediaPhoto(i) for i in mediaphoto_jpeg_skins]
            bot.send_media_group(chat_id=channel_id, media=mediagroup)
        else:
            for page in mediaphoto_jpeg_skins:
                bot.send_photo(chat_id=channel_id, photo=page)

    except Exception as err:
        print('+++++++++++++++Exception raised, but still running+++++++++++++++',end='\n')
        logging.warning(err)
        print(err)

        mediaphoto_jpeg_skins = daily_shop()[:-1]
        if len(mediaphoto_jpeg_skins) < 11:
            mediagroup = [telebot.types.InputMediaPhoto(i) for i in mediaphoto_jpeg_skins]
            bot.send_media_group(chat_id=channel_id, media=mediagroup)
        else:
            for page in mediaphoto_jpeg_skins:
                bot.send_photo(chat_id=channel_id, photo=page)

    finally:
        alerts = check_alerts()
        if alerts == False:
            bot.send_message(chat_id=channel_id, text='<u>Сегодня нет V-Bucks</u>')
        else:
            bot.send_message(chat_id=channel_id, text=alerts)


# def main():
#     if send_delay == True:
#         timee = dt.datetime.now()
#         timee += dt.timedelta(hours=5) #время в Уфе
#         file = open('status.txt')
#         status = file.read()
#         file.close()
#         if (timee.hour == 5 or timee.hour == 6) and (bool(status) == False):
#             sending()
#             file = open('status.txt','w')
#             file.write('True')
#             file.close
#         elif timee.hour > 6 and timee.hour < 23:
#             file = open('status.txt','w')
#             file.write('False')
#             file.close
#     else:
#         sending()


if __name__ == '__main__':
    try:
        sending()
    except Exception as err:
        logging.exception(err)
        print('??????????????????___Fatal error has occured!___?????????????????',end='\n')
        print(err)
