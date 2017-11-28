-------------------------------------------------------------------------------------
|                  Installation instructions using Ubuntu 16.04		  	    |
-------------------------------------------------------------------------------------

Setup virtual environment:
-------------------------------------------------------------------------------------

Create a virtual environment to install the packages above:
	$ virtualenv venv

To activate the environment created use the following:
	$ source venv/bin/activate

To deactivate the environment created use the following:
	$ deactivate


Installing required python packages (2 options to install, use option (2) if option (1) fails):			  
-------------------------------------------------------------------------------------

1) With the environment activated run the following line:
	$ pip install -r requirements.txt

2) With the environment activated install the required python packages:

	$ pip install opencv-python
	$ pip install sklearn
	$ pip install scipy
	$ pip install tensorflow
	$ pip install keras
	$ pip install Pillow


Classify an Image using the trained dataset (predict):				    
-------------------------------------------------------------------------------------

[usage] 
Run the following command to predict the emotion of a face:
	$ python predict.py <path/to/img/img.jpg>

	- Example run command to classify image 'img1_face.jpg':
	    $ python predict.py img1_face.jpg

[optional but strongly encouraged to get correct prediction] 
Before an image is used to predict emotion, we should extract a face from the image, run as follow:
	$ python extract_faces.py <path/to/img/img.jpg> <path/to/output/img/img.jpg>

	An example run, assuming we are reading image from current directory, and writing new image to a directory called 'faces', on an image called 'img1.jpg':
	    $ python extract_faces.py ./img1.jpg faces/img1_face.jpg


-------------------------------------------------------------------------------------

I will be posting the images along with the way to train the model another day, I have to store the images somewhere else since the file will probably be to big for github. 
