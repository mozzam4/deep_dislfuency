import redis
import time
import traceback
import json

def redischeck():
    try:
        r = redis.StrictRedis(host='127.0.0.1')                          # Connect to local Redis instance
        utterance = ''
        with open('/home/bbb/dev/mozzam/interm_files/raw_asr_text.txt', "w") as text_file:
            text_file.write(utterance)
        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        #p.subscribe('asr_text_*')
        p.psubscribe('asr_text_*')# Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:                                                                # Will stay in loop until START message received
         #   print("Waiting For redisStarter...")
            message = p.get_message()                                               # Checks for message
            if message:
                if type(message['data']) is bytes:
                    dic = json.loads(message['data'])
                    if type(dic) is dict:
                        for key, value in dic.items():
                            if key == "handle" and value == "completeUtterance": # or value == "partialUtterance"):
                                utterance = dic['utterance'] + ' ' 
                                print(dic['utterance'])
                                with open('/home/bbb/dev/mozzam/interm_files/raw_asr_text.txt', "a") as text_file:
                                    text_file.write(utterance)                

                command = message['data']                                           # Get data from message

                if command == b'START':                                             # Checks for START message
                    PAUSE = False                                                   # Breaks loop

            time.sleep(0.1)


      #  print("Permission to start...")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

redischeck()

