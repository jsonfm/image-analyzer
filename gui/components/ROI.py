import numpy as np
import cv2
import time 
import sys
sys.path.append('../..')
from loaders.images import ImageLoader
from viewer import normalizeArray


class Polygon:
	def __init__(self, points=[], maxPoints=1000, segmentLength=10):
		self.maxPoints = maxPoints
		self.segmentLengt = segmentLength
		self.points = list(points)
		self.pointsBackup = list(points)
		self.undoIndex = 0
	
	def setPoints(self, points:list):
		"""Set a list o points."""
		self.points = points

	def getPoints(self, asArray=True, dtype='int'):
		"""It returns the list of points"""
		if asArray:
			return np.array(self.points, dtype=dtype)
		else:
			return self.points

	def distance(self, point1, point2):
		"""It calculates the distance between two points."""
		x1, y1 = point1
		x2, y2 = point2
		dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return dist

	def addPoint(self, *args):
		"""It adds a new point to the list of points.
		Example:
			# way 1
			polygon.addPoint(1, 2)
			# way 2
			polygon.addPoint([1, 2])
		"""
		if len(args) < 2:
			newPoint = args[0]
		else:
			newPoint = [args[0], args[1]]
		if self.maxPoints <= len(self.points):
			lasPoint = self.points[-1]
			if self.distance(lasPoint, newPoint) >= self.segmentLengt:
				self.points.append(newPoint)
	
	def undo(self):
		"""It deletes the last point added."""
		self.points.pop()

	def redo(self):
		self.undoIndex += 1
		if self.undoIndex > len(self.points):
			self.undoIndex = 0
	
	def clear(self, backup=True):
		"""It clears the list of points."""
		if backup:
			self.pointsBackup = list(self.points)
		self.points = []
	
	def clearAll(self):
		"""It clears list of points and its backup."""
		self.points = []
		self.pointsBackup = []
	
	def restoreBackup(self):
		"""it """
		self.points = list(self.pointsBackup)

	def checkDtype(self, image, dtype='uint8'):
		"""It checks dtype of and image array."""
		if image.dtype != dtype:
			image = image.astype(dtype)
		return image
	
	def addColorChannels(self, image, to='rgb', dtype='uint8'):
		"""It transform a gray scale image to rgb or bgr."""
		if len(image.shape) < 3:
			if to == 'rgb':
				image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
			elif to == 'bgr':
				image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
			else:
				raise("to param must be: 'rgb' or 'bgr' ")
		image = self.checkDtype(image, dtype=dtype)
		return image

	def getBinaryMask(self, shape, label=1, dtype='uint8'):
		"""It returns a labeled mask (binary mask) of the roi inside of the polygon.
			Args:
				shape (tuple or lits): shape of the mask
				label (int or float) : max value inside of the mask
				dtype (str): data type of the image
		"""
		mask = np.zeros(shape, dtype=dtype)
		points = self.getPoints()
		mask = cv2.fillPoly(mask, [points], label)
		mask = self.checkDtype(mask, dtype=dtype)
		return mask

	def drawLines(self, mask, isClosed=True, color=(0, 0, 255), thickness=2, dtype='uint8'):
		"""It draws lines over a zeros mask.
		Args:
			mask (numpy array): zeros array
			isClosed (bool): flag to obtain closed polygon lines.
			color (tuple or list): RGB format
			thickness (int or float): thickness of the line
			dtype (str): data type of image
		"""
		points = self.getPoints()
		mask = self.checkDtype(mask, dtype)
		mask = self.addColorChannels(mask, to='rgb', dtype=dtype)
		lines = cv2.polylines(mask, [points], isClosed=isClosed, color=color, thickness=thickness)
		lines = self.checkDtype(lines, dtype=dtype)
		return lines

	def fillArea(self, mask, color=(0, 0, 255), dtype='uint8'):
		"""It paints and area over a zeros mask array.
		Args:
			mask (numpy array): zeros arrays
			color (list or tuple): RGB format
			dtype (str): data type of the image returned
		"""
		points = self.getPoints()
		mask = self.checkDtype(mask, dtype=dtype)
		mask = self.addColorChannels(mask, to='rgb', dtype=dtype)
		area = cv2.fillPoly(mask, [points], color=color)
		return area

	def fillAreaOver(self, image, color=(0, 0, 255), alpha=0.5, beta=0.5, dtype='uint8'):
		"""It paints area contained by the polygon over an image.
		Args:
			image (numpy array): image array
			color (list or tuple): RGB format
			alpha (int or float): opacity of the image
			beta (int or float): opacity of the mask
			dtype (str): data type of the image array
		"""
		mask = np.zeros(image.shape, dtype=dtype)
		area = self.fillArea(mask, color=color, dtype=dtype)
		image = self.addColorChannels(image, dtype=dtype)
		painted = cv2.addWeighted(image, alpha, area, beta, 0.0)
		painted = self.checkDtype(painted, dtype=dtype)
		return painted
	
	def drawLinesOver(self, image, color=(0,0, 255), alpha=0.5, beta=0.5, dtype='uint8'):
		"""It draws lines over an image.
		Args:
			image (numpy array): image array
			color (list or tuple): RGB format
			alpha (int or float): opacity of the image
			beta (int or float): opacity of the mask
			dtype (str): data type of the image array
		"""
		mask = np.zeros(image.shape, dtype=dtype)
		lines = self.drawLines(mask, color=color, dtype=dtype)
		image = self.addColorChannels(image, dtype=dtype)
		painted = cv2.addWeighted(image, alpha, lines, beta, 0.0)
		painted = self.checkDtype(painted, dtype=dtype)
		return painted


class Brush:
	def __init__(self, radius=10):
		self.radius = radius


	def erase(self, image):
		pass


src_c = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et2w_tse_clear_coronal.nii.gz"
src_s = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_sagital.nii.gz"
src_a = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_axial.nii.gz"

print_info =  lambda name, image: print(f"{name} , shape: {image.shape}")
# imageAxial = ImageLoader(src_a).load_array()
# imageCoronal = ImageLoader(src_c).load_array()
# imageSagital = ImageLoader(src_s).load_array()


def printMetadata(image, name="METADATA"):
	print(f"========================   {name}   =============================")
	for k in image.GetMetaDataKeys():
		v = image.GetMetaData(k)
		print(k, ": ", v)


imageAxial = ImageLoader(src_a).load_sitk()
imageCoronal = ImageLoader(src_c).load_sitk()
imageSagital = ImageLoader(src_s).load_sitk()
printMetadata(imageAxial, 'AXIAL')
print()
printMetadata(imageCoronal, 'CORONAL')
print()
print(imageSagital, 'SAGITAL')


print("Dir: ", imageAxial.GetDirection())
print("Dir 2: ", imageAxial.GetDirection)
# print_info("Axial: ", imageAxial)
# print_info("Coronal: ", imageCoronal)
# print_info("Sagital: ", imageSagital)
# for i in range(min(imageAxial.shape)):
# 	img = imageAxial[i, : , :]
# 	img = cv2.cvtColor(imageAxial, cv2.COLOR_GRAY2RGB)
# 	imageAxialRGB.append(img)
# imageAxialRGB = np.array(imageAxialRGB)
#imageAxialRGB = cv2.cvtColor(imageCoronal[1, : ,:], cv2.COLOR_GRAY2RGB)
# img = imageAxial[1, : , :]
# img = np.float32(img)
# rgb = cv2.cvtColor(imageCoronal[1, : ,:], cv2.COLOR_GRAY2RGB)
# print(img.shape)
# print(imageCoronal[:,1, :].shape)

# image = imageAxial[1, :, :]
# mask = np.zeros(image.shape)
# vertices = [[10, 30], [40, 50], [60, 100], [50, 250]]
# roi = ROI(vertices)
# t0 = time.time()
# filled = roi.fillArea(mask)
# t1 = time.time()
# lines = roi.drawLines(mask)
# t2 = time.time()
# new = roi.fillAreaOver(image, alpha=1, beta=0.25, label=1)
# # time.time()
# dt1 = t1 - t0
# dt2 = t2 - t1 

# print(f"filled: {dt1}")
# print(f"lines: {dt2}")
# new = polygon.paint(mask, label=2)
# print(new.max())

# cv2.imshow("filled", filled)
# cv2.imshow("lines", lines)
# cv2.imshow("added", new)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#print(indx[0])

# polygon = Polygon(vertices)
# polygon.fillZeroArray(mask)