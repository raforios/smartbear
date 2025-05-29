'''
    Configuring Logger
'''
import logging

def setup_logger(name, log_file = './logs/app.log', level = logging.INFO):
    ''' 
        Logger Config
    '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

custom_logger = setup_logger('smartbear')
