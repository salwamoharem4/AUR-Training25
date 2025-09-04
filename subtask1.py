import numpy as np
import matplotlib.pyplot as plt
import cv2
def convolution(image,kernel):
    rows,col=kernel.shape #make tuple for rows and columns
    if rows %2 ==0 or col %2 ==0:
        raise ValueError(f"Kernel dimensions must be odd")
    kernel=np.flipud(np.fliplr(kernel)) 
    pad_rows=rows//2
    pad_col=col//2
    pad_img=np.pad(image,((pad_rows,pad_rows),(pad_col,pad_col)),mode='constant') #padimage with black pixels
    op=np.zeros_like(image ,dtype=float) #create image of same size
    for i in range(image.shape[0]):
        for j in range(image.shape[1]): #loop over each pixel
            region=pad_img[i:i+rows,j:j+col] 
            op[i,j]=np.sum(region*kernel) #makes the new pixel of i,j
    op=np.clip(op,0,255) 
    return op.astype(np.uint8) 

img = cv2.imread(r"C:\Users\hp\OneDrive\Desktop\Documents\phase2\session3\image.jpg", cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Image not found. Check the file path and name.")
fig, axes = plt.subplots(2, 2, figsize=(8, 8))

# Original
axes[0, 0].imshow(img, cmap='gray')
axes[0, 0].set_title('Original Image')
axes[0, 0].axis('off')

# Box filter (smoothing)
box_kernel = np.ones((5, 5)) / 25
axes[0, 1].imshow(convolution(img, box_kernel), cmap='gray')
axes[0, 1].set_title('Box Filter')
axes[0, 1].axis('off')

# Horizontal Sobel
h_sobel = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])
axes[1, 0].imshow(convolution(img, h_sobel), cmap='gray')
axes[1, 0].set_title('Horizontal Sobel Filter')
axes[1, 0].axis('off')

# Vertical Sobel
v_sobel = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])
axes[1, 1].imshow(convolution(img, v_sobel), cmap='gray')
axes[1, 1].set_title('Vertical Sobel Filter')
axes[1, 1].axis('off')

plt.show()