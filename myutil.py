#from IPython.display 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from IPython.display import display
from IPython.core.display import HTML 
import json
from pprint import pprint
import os
import time
#import md5
import hashlib
import os

from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.client import AcsClient
import base64
import aliyunsdkimagesearch.request.v20190325.AddImageRequest as AddImageRequest
import aliyunsdkimagesearch.request.v20190325.DeleteImageRequest as DeleteImageRequest
import aliyunsdkimagesearch.request.v20190325.SearchImageRequest as SearchImageRequest

import os
import time
from pprint import pprint

def list_images(image_folder):
    images = {}
    for file in os.listdir(image_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_path = os.path.join(image_folder, file)
            # print(os.path.abspath(image_path))
            images[image_path] = file
    return images

def get_Piccontent_from_file(image_path):
    file_object = open(image_path)
    file_content = None
    try:
        file_content1 = file_object.read()
        import base64
        file_content = base64.b64encode(file_content1) # ('data to be encoded') 
        # data = base64.b64decode(encoded)
    finally:
        file_object.close()
    return file_content


def my_image_preview(image_path, box, cate, color="red"):
    #img1 = Image(filename = image_path, width=100, height=100)
    img1 = Image.open(image_path)
    if box is not None and box != '':
        draw = ImageDraw.Draw(img1)
        bb = box.split(",")
        x0 = float(bb[0])
        y0 = float(bb[2])
        x1 = float(bb[1])
        x2 = float(bb[3])
        draw.rectangle([(x0, y0), (x1, x2)], outline=color)
        if cate is not None and cate != "":
            draw.text((x0, y0), cate, fill=color)
    img = img1
    return img

###########################################################
###########################################################
def match_cate_desc(cate_id):
    AllCategories = [{'Id': 0, 'Name': 'Tops'}, {'Id': 1, 'Name': 'Dress'},{'Id': 2, 'Name': 'Bottoms'},{'Id': 3, 'Name': 'Bag'}, {'Id': 4, 'Name': 'Shoes'},{'Id': 5, 'Name': 'Accessories'},{'Id': 6, 'Name': 'Snack'},{'Id': 7, 'Name': 'Makeup'},{'Id': 8, 'Name': 'Bottle'},{'Id': 9, 'Name': 'Furniture'},{'Id': 20, 'Name': 'Toy'},{'Id': 21, 'Name': 'Underwear'},{'Id': 22, 'Name': 'Digital device'},{'Id': 88888888, 'Name': 'Other'}]
    for c in AllCategories:
        if cate_id == c['Id']:
            return c['Name']
    return 'Other'

def my_image_upload_base(requestClient, endpoint, instanceName, ProductId, image_name, image_path, cate_id, cate_desc, obj_region):
    # load file 
    request = AddImageRequest.AddImageRequest()
    request.set_endpoint(endpoint)
    request.set_InstanceName(instanceName)
    image_content = {'name': image_name, 'path': image_path, 'cate_id':cate_id, 'cate_desc':cate_desc, 'obj_region':obj_region}
    request.set_CustomContent(json.dumps(image_content))
    request.set_ProductId(ProductId)
    request.set_PicName(image_name)
    #if cate_id is not None:
    request.set_CategoryId(cate_id)
    print("=======", cate_id, image_name)
    with open(image_path, 'rb') as imgfile:
        encoded_pic_content = base64.b64encode(imgfile.read())
        request.set_PicContent(encoded_pic_content)
    response = requestClient.do_action_with_exception(request)
    r = json.loads(response)
    # print(response)
    return r

#def my_image_upload_for_category():

def my_image_upload_for_similarity_search(requestClient, endpoint, instanceName, ProductId, image_name, image_path, cate_id, cate_desc, obj_region):
    r = my_image_upload_base(requestClient, endpoint, instanceName, ProductId, image_name, image_path, cate_id, cate_desc, obj_region)
    #print("== image upload return result ==")
    #pprint(r)
    cate_desc = match_cate_desc(r['PicInfo']['CategoryId'])
    r['cate_desc'] = cate_desc
    r['cate_id'] = r['PicInfo']['CategoryId']
    r['obj_region'] = r['PicInfo']['Region']
    #pprint(r)
    #display(my_image_preview(image_path, r['obj_region'], r['cate_desc']))
    #print(image_path, ' | found category_desc: ', r['cate_desc'], r['cate_id'], ' | found category_id: ', r['cate_id'], ' | found region: ',  r['obj_region'])
    return r

###########################################################
###########################################################
def my_image_search_base(requestClient, instanceName, image_path):
    request = SearchImageRequest.SearchImageRequest()
    request.set_InstanceName(instanceName)
    with open(image_path, 'rb') as imgfile:
        encoded_pic_content = base64.b64encode(imgfile.read())
        request.set_PicContent(encoded_pic_content)
    response = requestClient.do_action_with_exception(request)
    r = json.loads(response)
    #pprint(r)
    return r

def my_image_search_for_category_detection(requestClient, instanceName, image_path):
    r = my_image_search_base(requestClient, instanceName, image_path)
    #r = json.loads(r)
    #pprint(r)
    category_desc = ''
    for c in r['PicInfo']['AllCategories']:
        if r['PicInfo']['CategoryId'] == c['Id']:
            category_desc = c['Name']
    r['cate_desc'] = category_desc
    r['cate_id'] = r['PicInfo']['CategoryId']
    r['obj_region'] = r['PicInfo']['Region']
    return r

def my_image_search_for_category_detection_display(requestClient, instanceName, image_path):
    r = my_image_search_for_category_detection(requestClient, instanceName, image_path)
    display(my_image_preview(image_path, r['obj_region'], r['cate_desc']))
    #print(image_path, ' | found category_desc: ', r['cate_desc'], r['cate_id'], ' | found category_id: ', r['cate_id'], ' | found region: ',  r['obj_region'])
    return r

###########################################################
###########################################################
def my_image_search_for_similarity(requestClient, instanceName, image_path):
    r = my_image_search_base(requestClient, instanceName, image_path)
    #r = json.loads(r)
    #pprint(r)
    category_desc = ''
    for c in r['PicInfo']['AllCategories']:
        if r['PicInfo']['CategoryId'] == c['Id']:
            category_desc = c['Name']
    #pprint(r)
    
    #print(image_path, 'found category_desc: ', category_desc, r['PicInfo']['Category'], 'found category_id: ', r['PicInfo']['Category'], 'found region: ',  r['PicInfo']['Region'])
    
    #image_similar_name = r['Auctions'][1]['PicName']
    #image_similar_path = r['Auctions'][1]['CustomContent']
    image_similar_name = json.loads(r['Auctions'][1]['CustomContent'])['name']
    image_similar_path = json.loads(r['Auctions'][1]['CustomContent'])['path']
    image_similar_score = r['Auctions'][1]['SortExprValues']
    category_desc = json.loads(r['Auctions'][1]['CustomContent'])['cate_desc']
    obj_region = json.loads(r['Auctions'][1]['CustomContent'])['obj_region']
    print(image_path)
    print("similar score: ", image_similar_score, "similar image: ", image_similar_path)
    
    #print(r['Auctions']['Auction'][1])
    
    img1 = my_image_preview(image_path, obj_region, category_desc)
    img2 = my_image_preview(image_similar_path, '0,0,0,0', 'most_similart_to', 'green')
    
    img_height = img1.size[1]
    if img1.size[1] < img2.size[1]:
        img_height = img2.size[1]
    img = Image.new('RGB', (img1.size[0]+img2.size[0]+40, img_height), "white")
    img.paste(img1, (0, 0))
    img.paste(img2, (img1.size[0]+40, 0))
    #print(img)
    
    draw = ImageDraw.Draw(img)
    draw.text((img1.size[0]+20, img_height/2), '=>', fill="green")
    draw.text((img1.size[0]+20, img_height/2+10), 'most', fill="red")
    draw.text((img1.size[0]+20, img_height/2+20), 'similar', fill="red")
    draw.text((img1.size[0]+20, img_height/2+30), 'to', fill="red")
    draw.text((img1.size[0]+20, img_height/2+40), '=>', fill="green")
    sim_score = "{0:.0%}".format(float(image_similar_score.split(';')[0]))
    draw.text((img1.size[0]+20, img_height/2+50), image_similar_score, fill="red")
    
    #display(img1)
    #display(img2)
    display(img)
    
    return r



