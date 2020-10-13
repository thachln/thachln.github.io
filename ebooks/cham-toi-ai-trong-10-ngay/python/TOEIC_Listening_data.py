# =============================================================================
# Cài đặt thư viện
# pip install mutagen
# =============================================================================
from mutagen.mp3 import MP3
import logging as log
import os
import pandas as pd
from os.path import normpath, basename

# =============================================================================
# Lấy thời gian của file âm thanh mp3.
# @filePath đường dẫn của file mp3
# @return thời lượng của file âm thanh tính bằng giây
# =============================================================================
def getDuration(filePath):
    audio = MP3(filePath)

    audio_info = audio.info    
    length_in_secs = int(audio_info.length)

    log.debug('Duration of audio', length_in_secs)

    return length_in_secs

# =============================================================================
# Duyệt thư mục và tất cả thư mục con (recursively)
# @folderPath thư mục cha cần duyệt
# @return DataFrame gồm 3 cột: part, file, duration
# part: là 1 trong 7 part của đề thi TOEIC (lấy từ tên thư mục chứa file mp3)
# file: là tên file mp3
# duration: thời lượng của file mp3 (tính bằng giây)
# =============================================================================
def scanAudio(folderPath):
    parts = []
    files = []
    durations = []
    for dirpath, dirnames, filenames in os.walk(folderPath):
        for filename in [f for f in filenames if f.endswith('.mp3')]:
            part = basename(normpath(dirpath))
            audioFilePath = os.path.join(dirpath, filename)
            duration = getDuration(audioFilePath)
            parts.append(part)
            files.append(filename)
            durations.append(duration)
            
            log.debug('audioFilePath=', audioFilePath, duration)
            # print('audioFilePath=', audioFilePath)
    # Build dataframe
    
    df = pd.DataFrame(list(zip(parts, files, durations)), columns=['part', 'file', 'duration'])
    df.sort_values(by=['part', 'file'])

    return df

# Đường dẫn của dữ liệu đề thi TOEIC mẫu
PATH = r'D:\Projects\TOEIC\TOEIC_ETS_2016_1'
log.basicConfig(level=log.DEBUG)
df = scanAudio(PATH)

# Lưu data frame ra file CSV.
df.to_csv('D:/Temp/TOEIC.csv')
