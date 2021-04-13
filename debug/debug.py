import os
import psutil

process = psutil.Process(os.getpid())
print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB')
