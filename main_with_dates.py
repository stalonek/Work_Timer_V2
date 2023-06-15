import time
import sqlite3
import logging
import sys
from datetime import datetime


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class DBManager:
    """ Class responsible for data base management DB name: LoggingDB.db """
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        """DB connection set up"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            return self.connection
        except sqlite3.Error as e:
            print(f"DB connection has failed due to: {e.args[0]}")
            return None

    def disconnect(self):
        """DB disconnection"""
        self.connection.close()

    def write_to_db(self, time, date_of_study,  study_topic):
        """DB update with values"""

        cursor = self.connection.cursor()
        try:
            cursor.execute(f"INSERT INTO Logs (Time,'Study topic','Date of study') VALUES (?,?,?)", (time, study_topic, date_of_study,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Something went wrong with DB update due to: {e.args[0]}")

    def fetch_all(self):
        """ DB select * from"""

        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM Logs")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"DB operation has failed due to: {e.args[0]}")
            return None


class Timer:
    """ Class for time counting management"""

    def __init__(self):
        self.start_time = None
        self.pause_start_time = None
        self.paused_time = 0
        self.is_paused = False
        self.current_time = None



    def get_formatted_time(self, elapsed_time):
        """Formatting time """

        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}"


    def get_date(self):
        """ Return current date value"""
        self.current_date = datetime.now()
        formatted_date = self.current_date.strftime("%d-%m-%Y")
        return formatted_date

    logging.info('Date has been retrieved')

    def start(self):
        """Start counter"""

        self.start_time = time.time()
        self.is_paused = False
        logging.info('Timer started')

    def print_current_time(self):
        """Print current time in each of the needed functiion"""

        self.current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Time of current action: {self.current_time}")


    def stop(self):
        """Stop counter"""

        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.start_time = None
            logging.info("Timer stopped")
            print(f'Timer stopped: elapsed time is {self.get_formatted_time(elapsed_time)}')
            return self.get_formatted_time(elapsed_time)

    def pause(self):
        """Pause counter"""
        if self.start_time is not None and not self.is_paused:
            self.pause_start_time = time.time()
            self.is_paused = True
            elapsed_time = self.pause_start_time - self.start_time - self.paused_time
            print('Time paused')
            return self.get_formatted_time(elapsed_time)

    def resume(self):
        """Resume pause"""
        if self.is_paused:
            self.paused_time += time.time() - self.pause_start_time
            self.is_paused = False
            pause_duration = time.time() - self.pause_start_time
            print('Timer resumed')
            return self.get_formatted_time(pause_duration)



    def get_time(self):
        """ Returns current timer value"""

        if self.start_time is not None:
            if self.is_paused:
                return self.get_formatted_time(self.paused_time)
            else:
                return self.get_formatted_time(time.time()-self.start_time)
        else:
            logging.error('Timer was not started')






class Program:
    """ Managing class"""

    def __init__(self, db_manager, timer):
        self.db_manager = db_manager
        self.timer = timer

    def run(self):
        print('1 - START PROGRAM \n'
              '2 - SHOW SUMMARY \n'
              'q - QUIT PROGRAM ')
        while True:
            self.timer.print_current_time()
            command = input()
            if command == "1":
                self.timer.start()

                while True:


                    command = input()  # Ask for the user's command
                    if command.lower() == 'exit':
                        formated_time = self.timer.stop()
                        study_topic = input("Enter the topic of the study: ")
                        date_of_study = self.timer.get_date()
                        self.db_manager.connect()
                        self.db_manager.write_to_db(formated_time, study_topic, date_of_study)
                        self.db_manager.disconnect()
                        print(f'Timer stopped, elapsed time: {formated_time}, study topic: {study_topic}')
                        break

                    elif command.lower() == 'p':
                        if self.timer.is_paused:
                            pause_duration = self.timer.resume()
                            print(
                                f"Timer resumed after a pause of {pause_duration}. Type 'exit' to stop the timer or 'p' to pause it again.")
                        else:
                            elapsed_time = self.timer.pause()
                            print(f'Timer paused after {elapsed_time}. Type "p" again to resume')

                    elif command.lower() == 'q':
                        sys.exit()

            elif command == '2':
                self.db_manager.connect()
                rows = self.db_manager.fetch_all()
                for row in rows:
                    print(row)
                self.db_manager.disconnect()

            elif command.lower() == 'q':
                print('Program has been finished, thanks!')
                sys.exit()

            else:
                logging.error("Invalid command")


if __name__ == "__main__":
    db_manager = DBManager('LoggingDB.db')
    timer = Timer()
    program = Program(db_manager, timer)
    program.run()

#TODO kurwa nie dzialaja printy trzeba poprawic






