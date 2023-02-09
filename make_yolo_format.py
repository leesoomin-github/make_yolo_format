import json
import os
import shutil


json_path = "C:/Users/lee soo min/Documents/신호등-도로표지판 인지 영상(수도권)/validation/labels/c_validation_1280_720_daylight_1/"
data = []
outputs_path_image = "C:/Users/lee soo min/Documents/신호등-도로표지판 인지 영상(수도권)/validation/image"
#labels_path = "C:/Users/lee soo min/Documents/신호등-도로표지판 인지 영상(수도권)/validation/label"
images_path = "C:/Users/lee soo min/Documents/신호등-도로표지판 인지 영상(수도권)/validation/images/"
label_path = "C:/Users/lee soo min/Documents/신호등-도로표지판 인지 영상(수도권)/validation/label"
def read_json():

    json_list = os.listdir(json_path)
    json_list = [file for file in json_list if file.endswith(".json")]

    for i in json_list:
        with open(json_path + i , "r") as f:
            data.append(json.load(f))

    return data

def get_img_ann():
    img_ann = []
    annotation = read_json()

    for ann_list in annotation:
        for ann in ann_list['annotation']:
            if ann['class'] == 'traffic_light' and ann['type'] == 'car':
                ann['image_name'] = ann_list['image']['filename']
                ann['image_size'] = ann_list['image']['imsize']
                if ann['light_count'] == '3' or ann['light_count'] == '4':
                    if ann['attribute'][0]['green'] == 'on' and ann['attribute'][0]['left_arrow'] == 'off':
                        ann['id'] = '0'
                        img_ann.append(ann)
                    if ann['attribute'][0]['red'] == 'on' and ann['attribute'][0]['left_arrow'] == 'off':
                        ann['id'] = '1'
                        img_ann.append(ann)
                    if ann['attribute'][0]['yellow'] == 'on' and ann['attribute'][0]['left_arrow'] == 'off':
                        ann['id'] = '2'
                        img_ann.append(ann)
                    if ann['attribute'][0]['red'] == 'on' and ann['attribute'][0]['left_arrow'] == 'on':
                        ann['id'] = '3'
                        img_ann.append(ann)
                    if ann['attribute'][0]['green'] == 'on' and ann['attribute'][0]['left_arrow'] == 'on':
                        ann['id'] = '4'
                        img_ann.append(ann)


    return img_ann




def make_yolo_format():
    # Extracting image


    # Get Annotations for this image
    img_ann = get_img_ann()
    for img in img_ann:
        img_w = img['image_size'][0]
        img_h = img['image_size'][1]
        image_name = img['image_name'].split('.')

        # Opening file for current image
        file_object = open(f"{label_path}/{image_name[0]}.txt", "a")

        # for ann in img_ann:
        current_category = img['id']  # As yolo format labels start from 0
        current_bbox = img['box']
        x = current_bbox[0]
        y = current_bbox[1]
        w = current_bbox[2]
        h = current_bbox[3]

        # Finding midpoints
        x_centre = (x + (x + w)) / 2
        y_centre = (y + (y + h)) / 2

        # Normalization
        x_centre = x_centre / img_w
        y_centre = y_centre / img_h
        w = w / img_w
        h = h / img_h

        # Limiting upto fix number of decimal places
        x_centre = format(x_centre, '.6f')
        y_centre = format(y_centre, '.6f')
        w = format(w, '.6f')
        h = format(h, '.6f')

        # Writing current object
        file_object.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")

        file_object.close()

def check_img():
    label_list= os.listdir(label_path)
    label_list = [file for file in label_list if file.endswith(".txt")]

    for l in label_list:
        l=l.split(".")[0]
        source = images_path + l + ".jpg"
        destination = f"{outputs_path_image}/{l}.jpg"
        shutil.copy(source, destination)


if __name__ == "__main__":
    make_yolo_format()
    check_img()





