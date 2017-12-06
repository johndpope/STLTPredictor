import tensorflow as tf
import numpy as np
import os,glob,cv2
import sys,argparse, glob
from extract_faces import extract

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#cmpny_name='TSLA'

classes = ['anger','disgust', 'happy', 'neutral', 'surprise']
class_weight = [-1.0, -0.5, 1.0, 0.0, 0.5]

def predict(cmpny_name, mode):
	# First, pass the path of the image
	dir_path = os.path.dirname(os.path.realpath(__file__))
	#filename = dir_path + '/' + cmpny_path + '/' + image_path
	#filepath = dir_path + '/companies/' + cmpny_name
	filepath = dir_path + '/' + cmpny_name
	image_size=150
	num_channels=3
	predict_files = glob.glob(filepath + "/*")

	## Let us restore the saved model 
	sess = tf.Session()
	# Step-1: Recreate the network graph. At this step only graph is created.
	saver = tf.train.import_meta_graph('emotion-model.meta')
	# Step-2: Now let's load the weights saved using the restore method.
	saver.restore(sess, tf.train.latest_checkpoint(dir_path))

	# Accessing the default graph which we have restored
	graph = tf.get_default_graph()

	# Now, let's get hold of the op that we can be processed to get the output.
	# In the original network y_pred is the tensor that is the prediction of the network
	y_pred = graph.get_tensor_by_name("y_pred:0")

	## Let's feed the images to the input placeholders
	x= graph.get_tensor_by_name("x:0") 
	y_true = graph.get_tensor_by_name("y_true:0") 
	y_test_images = np.zeros((1, 5)) 

	predictions = {'anger':0, 'disgust':0, 'happy':0, 'neutral':0, 'surprise':0}
	
	#print "filepath: ", filepath
	img_location = ""
	for predict_img in predict_files:
		
		images = [] # Reading the image using OpenCV
		
		#img_location = extract(predict_img, predict_img.split("/")[-1])

		if mode is 1:
			img_location = extract(predict_img, "extracted_data/" + cmpny_name.split("/")[-1] + "/" + predict_img.split("/")[-1])
		else:		
			img_location = predict_img

		if img_location == '':
			img_location = predict_img
			img_location_remove = False
		else:
			img_location_remove = True
		
			
		#print "img_location:", img_location
		image = cv2.imread(img_location)
		#image = extract(filename, "/extracted_data/" + cmpny_path + "pic1.jpg")
		
		#if img_location_remove:
			#os.remove(img_location)

		# Resizing the image to our desired size and preprocessing will be done exactly as done during training
		image = cv2.resize(image, (image_size, image_size),0,0, cv2.INTER_LINEAR)
		images.append(image)
		images = np.array(images, dtype=np.uint8)
		images = images.astype('float32')
		images = np.multiply(images, 1.0/255.0) 
		#The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
		x_batch = images.reshape(1, image_size,image_size,num_channels)

		## Let us restore the saved model 
		# deleted lines go here

		### Creating the feed_dict that is required to be fed to calculate y_pred 
		feed_dict_testing = {x: x_batch, y_true: y_test_images}
		result=sess.run(y_pred, feed_dict=feed_dict_testing)
		result_array = [result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]]

		#for emotion in classes:
		#print(result)

		# uncomment for loop to print which emotion it classified, with what probability
		#for i in range(len(classes)):
			#print("%s: %s" % (classes[i] ,'{:.10%}'.format(result_array[i])))

		#print("disgust: %s" % '{:.10%}'.format(result_array[1]))
		#print("happy: %s" % '{:.10%}'.format(result_array[2]))
		#print("neutral: %s" % '{:.10%}'.format(result_array[3]))
		#print("surprise: %s" % '{:.10%}'.format(result_array[4]))
		
		max_val = max(result_array)
		#print "max:", max_val
		predictions[classes[result_array.index(max_val)]] += 1

	prediction_val = max(predictions, key=predictions.get)
	#print "max prediction:", prediction_val

	total_predict = 0
	for emotion in classes:
		total_predict += predictions[emotion]

	#print "total_predict:", total_predict

	decision = 0.0
	index = 0;	
	for emotion in classes:
		#print emotion, ":", float(predictions[emotion])
		#print "predictions[emotion]/total_predict: ", float(predictions[emotion])/float(total_predict)
		decision += float(predictions[emotion])/float(total_predict)*class_weight[index]
		#print "decision: ", '{:.10%}'.format(decision)
		index += 1

	print "decision:", decision

	'''
	decision = 0
	if prediction_val == "neutral" or len(predict_files) == 0:
		print "NOT SURE IF BUY!"
		decision = 0
	elif prediction_val == "happy" or prediction_val == "surprised":
		print "YOU SHOULD BUY!"
		decision = 1
	else:
		print "DO NOT BUY!"
		decision = -1
	'''

	return decision
	#return something here, max prediction for now
		

if __name__ == "__main__":

	mode = -1
	if len(sys.argv) == 3:
		mode = 1
	else:
		mode = 0;

	img_path = sys.argv[1]
	
	#predict("companies/TEST_DIR")	
	predict(img_path, mode)	
