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

[usage] 2 modes (extract faces, and do not extract faces)

[Mode 1: Extract faces]
Run the following command to extract and predict the emotions of faces in company folder:
	$ python predict.py <path/to/stock> extract

	- Example run command to ectract and predict TSLA images:
	    $ python predict.py companies/TSLA extract

[Mode 2: Do not extract faces, assume already extracted (better for performance)]
Run the following command to predict the emotions of faces in company folder:
	$ python predict.py <path/to/stock>

	- Example run command to predict TSLA images:
	    $ python predict.py extracted_data/TSLA
-------------------------------------------------------------------------------------

1) To extract videos:

I downloaded this application to extract videos into frames:
	https://www.dvdvideosoft.com/products/dvd/Free-Video-to-JPG-Converter.htm

Once I have all the frames in a directory (the application above does this), I save the directory of frames inside of companies(rename it using the stock name if you want) and then just run the command above to extract and predict.

Ex. If I just downloaded a Windows video and got the frames using the above software, I would save the folder that software created inside of companies (inside of this project) and rename it MSFT. Then to run predict on that directory we just run the following command:

	$ python predict.py companies/MSFT extract

Once it finished it will show the prediction result and return it (if function call)

To view extracted images go to directory : 
	extracted_data/MSFT

To run predictor on the images once they are extracted to get the result only (much faster, takes less than 3 seconds)
	$ python predict.py extracted_data/MSFT

-------------------------------------------------------------------------------------

To train this classifier

I will be posting the images along with the way to train the model another day, I have to store the images somewhere else since the file will probably be to big for github. 
