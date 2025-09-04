import numpy as np
import matplotlib.pyplot as plt
import cv2
img = cv2.imread(r"C:\Users\hp\OneDrive\Desktop\Documents\phase2\session3\shapes.jpg")
out=img.copy() #don't modify the original
#create masks for each color
blue_mask = (img[:,:,0] > 150) & (img[:,:,1] < 100) & (img[:,:,2] < 100)
red_mask = (img[:,:,2] > 150) & (img[:,:,1] < 100) & (img[:,:,0] < 100)
black_mask = (img[:,:,0] < 50) & (img[:,:,1] < 50) & (img[:,:,2] < 50)
#swap colors
out[blue_mask] = [0, 0, 0]      # Blue turned Black
out[red_mask] = [255, 0, 0]     # Red turned Blue
out[black_mask] = [0, 0, 255]   # Black turned Red 
img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #converts bgr to rgb 
out_rgb=cv2.cvtColor(out,cv2.COLOR_BGR2RGB) 
#SHOW IMAGE
fig, axes = plt.subplots(1, 2)
axes[0].imshow(img_rgb)
axes[0].set_title('Original Image')
axes[0].axis('off')

axes[1].imshow(out_rgb)
axes[1].set_title('Processed Image')
axes[1].axis('off')

plt.show()