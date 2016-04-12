import pygame
import time
pygame.mixer.init()
pygame.mixer.music.load("config/test.wav")
print("Wait")
time.sleep(1)
print("Now!")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
print("Done!")
