# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sqlite3


class SQLiteHandler(logging.Handler):
    """
    Logging handler that write logs to SQLite DB
    """

    def __init__(self, filename):
        global db
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        db = sqlite3.connect(filename)  # might need to use self.filename
        db.execute("""
        CREATE TABLE  IF NOT EXISTS 
        debug(date datetime, logger_name text, filename, src_line_no integer, func text, level text, msg text)
        """)
        db.commit()

    def emit(self, record):
        # record.message is the log message
        db.execute(
            'INSERT INTO debug(date, logger_name, filename, src_line_no, func, level, msg) VALUES(?,?,?,?,?,?,?)',
            (
                datetime.datetime.now(),
                record.name,
                os.path.abspath(record.filename),
                record.lineno,
                record.funcName,
                record.levelname,
                record.msg,
            )
        )
        db.commit()


class ProjectLogger(object):
    def __init__(self, name=None):
        dirname = os.path.dirname(__file__)
        now = datetime.datetime.now()
        log_name = now.strftime("%Y-%m-%d") + '_test.log'
        sql_log_name = now.strftime("%Y-%m-%d") + '_test.sqlite'

        log_path = os.path.join(dirname, 'logs', log_name)
        sql_log_path = os.path.join(dirname, 'logs', sql_log_name)

        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(SQLiteHandler(sql_log_path))
        self.logger.addHandler(fh)

    def save_screenshot(self, driver):
        dirname = os.path.dirname(__file__)
        now = datetime.datetime.now()
        img_name = now.strftime("%Y-%m-%d_%H-%m-%S") + '_img.png'
        img_path = os.path.join(dirname, 'screenshots', img_name)
        driver.save_screenshot(img_path)

    def get_logger(self):
        return self.logger

    @property
    def proxy_log_path(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, 'logs')

    @property
    def proxy_log_file(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d") + '_proxy.log'

    @property
    def proxy_har_file(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d") + '_har.log'
