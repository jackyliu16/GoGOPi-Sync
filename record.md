

## reference
how to understand the cv2.VideoCapture: https://blog.csdn.net/Zhou_yongzhe/article/details/80310537

能否尝试不使用现有解决方案，直接通过计算整个轮廓中距离最远的两对点的位置，然后将这两条直线之间的夹角进行计算

- 当夹角小于某个角度的时候，则可以认为两条直线处于重合状态，此时应当选择最长的那条线，但是可能由于线段当前的根位置对于实验产生影响
当夹角接近 90+-10度的时候，可以认定面前存在终点线，此时跟着相对来说更加垂直的那条直线继续行驶

```plain
在OpenCV中，您可以使用cv2.findContours()函数来查找轮廓。该函数返回一个包含所有轮廓的列表，每个轮廓都是一个包含(x,y)坐标的numpy数组。一旦您找到了轮廓，您可以使用cv2.arcLength()函数来计算轮廓的周长，然后使用cv2.approxPolyDP()函数来近似轮廓并减少其顶点数。最后，您可以使用cv2.drawContours()函数来绘制轮廓。

要计算轮廓中相距最远的两个点，您可以使用scipy.spatial.distance.cdist()函数来计算所有点之间的距离，并使用numpy.unravel_index()函数找到距离最远的两个点的索引。然后，您可以使用这些索引从原始轮廓中提取这些点。

以下是一个示例代码：

import cv2
import numpy as np
from scipy.spatial.distance import cdist

# Load image and convert to grayscale
image = cv2.imread('image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find contours
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find contour with largest area
contour = max(contours, key=cv2.contourArea)

# Approximate contour and reduce number of vertices
epsilon = 0.01 * cv2.arcLength(contour, True)
approx = cv2.approxPolyDP(contour, epsilon, True)

# Compute pairwise distances between all points in contour
distances = cdist(approx.reshape(-1, 2), approx.reshape(-1, 2))

# Find indices of points with maximum distance
i, j = np.unravel_index(np.argmax(distances), distances.shape)

# Extract points with maximum distance from contour
point1 = tuple(approx[i][0])
point2 = tuple(approx[j][0])

# Draw line connecting two points
cv2.line(image, point1, point2, (0, 0, 255), 3)

# Display result
cv2.imshow('Result', image)
cv2.waitKey(0)
```

- 当前使用的算法，在对于