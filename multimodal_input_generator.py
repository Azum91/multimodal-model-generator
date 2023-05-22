'''
This is the helper code:
if anyone is looking for the example on how to create a genetor
for multimodal input this code can be helpfull.

1. images_list is created using glob
2. dataframe is read as is from the pandas
3. feature_cols is the list of features columns that need to be considered as input
        Note that all preprocessing may be applied before passing to this function the dataframe
4. Labels can be taken from CSV or from the images folder name as class with little modification.
'''

def custom_generator(images_list, dataframe, batch_size, num_classes):
    i = 0
    while True:

        images = []
        features_csv = []
        labels = []
        for b in range(batch_size):
            # Read image from list and convert to array
            if i >= len(images_list):
                i = 0
            image_path = images_list[i]
            # print(len(images_list))
            image_name = os.path.basename(image_path).replace('.JPG', '')
            image = krs_image.load_img(image_path, target_size=(224, 224))
            image = krs_image.img_to_array(image)
            image = datagen.apply_transform(image, data_gen_args)

            # Read data from csv using the name of current image

            csv_row = dataframe.loc[dataframe['image_id'] == image_name]
            features = csv_row[feature_cols].values

            label = csv_row['labels']

            images.append(image)
            features_csv.append(features)
            labels.append(label)
            # print(i)
            i += 1

        images = np.array(images)
        features_csv = np.array(features_csv)
        # Convert labels to categorical values

        labels = np.eye(num_classes)[labels]
        labels = np.reshape(labels, (batch_size, 10))

        yield [images, features_csv], labels

# Example Script for executing the function
training_generator = custom_generator(image_file_list, csv_data, batch_size, NUM_CLASSES)