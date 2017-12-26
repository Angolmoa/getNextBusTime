# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime, date, timezone, timedelta
import nextBus as bus

# �G���g���[�|�C���g
def lambda_handler(event, context):
    return get_next_bus_response()

# ���̃o�X���ԃ��X�|���X�𐶐�
def get_next_bus_response():
    session_attributes = {}
    time = datetime.now(timezone(timedelta(hours=+9))).time()
    
    if bus.isHolyday() :
        wkd = "�y�x��"
    else:
        wkd = "����"
    card_title = "{0}{1}:{2:02d}���ȍ~�̃o�X����".format(wkd,time.hour,time.minute)
    nearest,all,busStop,destination = bus.getNextXBusTime(3)
    if len(nearest) > 0:
        speech_output=nearest + "�Ƀo�X�����܂�\n"
    else:
        speech_output = "�����͂����o�X������܂���\n"
    card_text = speech_output + busStop + ' ' + destination + '\n' + all
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_text, should_end_session))

# �߂�l��JSON�𐶐�
def build_speechlet_response(title, output, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': card_text
        },
        'shouldEndSession': should_end_session
    }

# �߂�l�̑S��
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }