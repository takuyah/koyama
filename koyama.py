# -*- coding: utf-8 -*-

import os
import json
import mechanize
import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet


def push_to_pushbullet(client, body):
    channel = client.get_channel('koyama')
    return channel.push_link('Koyama Alert', 'http://221.186.136.107/scripts/mtr1010.asp', body)


def lambda_handler(*args):
    timetable = {
        '1': '08:40',
        '2': '09:40',
        '3': '10:40',
        '4': '11:40',
        '5': '12:40',
        '6': '13:30',
        '7': '14:30',
        '8': '15:30',
        '9': '16:30',
        '10': '17:40',
        '11': '18:40',
        '12': '19:40',
        '13': '20:40'
    }

    school_ip = {
        'futakotamagawa': '125.206.202.147',
        'seijo': '153.150.125.233',
        'shakujii': '221.186.136.107',
        'akitsu': '125.206.199.163',
        'tsunashima': '125.206.214.67'
    }

    IP = school_ip[os.environ['KOYAMA_LOC']]
    LOGIN_URL = 'http://{}/scripts/mtr0010.asp'.format(IP)
    CALENDAR_URL = 'http://{}/scripts/mtr1010.asp'.format(IP)

    browser = mechanize.Browser()
    browser.open(LOGIN_URL)
    browser.form = list(browser.forms())[0]

    un_control = browser.form.find_control('mt0010uid')
    un_control.value = os.environ['KOYAMA_ID']
    password_control = browser.form.find_control('mt0010pwd')
    password_control.value = os.environ['KOYAMA_PW']

    browser.submit()
    browser.open(CALENDAR_URL)

    all_available = {}
    all_reserved = {}
    for i in xrange(0, int(os.environ['MAX_WEEKS'])):
        soup = BeautifulSoup(browser.response().read(), 'html.parser', from_encoding='shift-jis')    # doesn't work with lxml/xml
        available = soup.find_all('input', src='/images/ko2_kusya.gif')
        print('week {}: {} available'.format(str(i), str(len(available))))
        for date in available:
            period = date.attrs['name'][1:]
            date_string = date.parent.parent.contents[1].text
            try:
                all_available[date_string].append(timetable[period])
            except KeyError:
                all_available[date_string] = [timetable[period]]
        try:
            browser.form = browser.forms()[0]
            browser.submit('next')
        except:
            break

    print(sorted(all_available))
    message_text = u'\n'.join([u'{}: {}'.format(date, ', '.join(times)) for (date, times) in sorted(all_available.iteritems())])

    if os.environ['KOYAMA_PUSH_MODE'] in ('line', 'both'):
        if all_available:
            message_text += u'\n\n' + CALENDAR_URL
            url = 'https://api.line.me/v2/bot/message/push'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {{{}}}'.format(os.environ['LINE_CHANNEL_TOKEN'])   # {{ → '{'
            }
            payload = {
                'to': os.environ['LINE_MY_ID'],
                'messages':[
                    {
                        'type': 'text',
                        'text': message_text
                    }
                ]
            }
            r = requests.post(url, headers=headers, data=json.dumps(payload))
            print(r)
        else:
            print('None available.')

    if os.environ['KOYAMA_PUSH_MODE'] in ('pushbullet', 'both'):
        pb = Pushbullet(os.environ['PUSHBULLET_TOKEN'])
        if all_available:
            pushes = pb.get_pushes()
            try:
                most_recent = [push for push in pushes if push['sender_name'] == 'Koyama Alert'][0]
                if most_recent['body'] != message_text:
                    pb.dismiss_push(most_recent['iden'])
                    push = push_to_pushbullet(pb, message_text)
            except IndexError:
                push = push_to_pushbullet(pb, message_text)
            print(push)
        else:
            undismissed = [push['iden'] for push in pb.get_pushes() if push['sender_name'] == 'Koyama Alert' and not push['dismissed']]
            for iden in undismissed:
                pb.dismiss_push(iden)
            print('None available. Dismissed pushes.')

    return None


if __name__ == '__main__':
    lambda_handler()
