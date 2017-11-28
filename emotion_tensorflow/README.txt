Create a virtual environment to install the packages above, and activate it:
	$ virtualenv venv
	$ source venv/bin/activate

To deactivate the environment use:
	$ deactivate

-------------------------------------------------------------------------------------

With the environment activated install the following python packages:

	$ pip install opencv-python
	$ pip install sklearn
	$ pip install scipy
	$ pip install tensorflow
	$ pip install keras
	$ pip install Pillow


Before an image is used to predict emotion, we should extract a face from the image, run as follow:
	$ python extract_faces.py <path/to/img/img.jpg> <path/to/output/img/img.jpg>

An example run, assuming we are reading, and writing from current directory, on an image called 'img1.jpg':
	$ python extract_faces.py img1.jpg img1_face.jpg

Once a face has been extracted from an image, we can run the following to predict the emotion of the face of image 'img1_face.jpg':
	$ python predict.py img1_face.jpg

-------------------------------------------------------------------------------------

I will be posting the images along with the way to train the model another day, I have to store the images somewhere else since the file will probably be to big for github. 
