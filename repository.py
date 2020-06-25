import sqlite3
import settings


def update_game_current_number(game_key, current_number):
    conn = sqlite3.connect(settings.DATABASE_PATH)
    sql = ''' UPDATE video_numbers
              SET current_number = ?
              WHERE game_key = ?'''
    task = (current_number, game_key)
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()
    conn.close()

def get_game_current_number(game_key):
    conn = sqlite3.connect(settings.DATABASE_PATH)
    sql = ''' SELECT current_number
              FROM video_numbers
              WHERE game_key = ?'''
    task = (game_key,)
    c = conn.cursor()
    c.execute(sql, task)
    row = c.fetchone()
    return row[0]            
