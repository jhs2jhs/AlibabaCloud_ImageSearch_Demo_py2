
# coding: utf-8

# # this demo is to setup using python2

# In[1]:


#from IPython.display import Image
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from IPython.display import display
from IPython.core.display import HTML 
import json
from pprint import pprint
import os
import time
import hashlib


# In[2]:


def get_md5(txt):
    #return md5.new(txt).digest()
    return str(hashlib.sha224(txt).hexdigest())


# In[3]:


def image_preview(image_path, box, cate):
    #img1 = Image(filename = image_path, width=100, height=100)
    img1 = Image.open(image_path)
    if box is not None and box != '':
        draw = ImageDraw.Draw(img1)
        bb = box.split(",")
        x0 = float(bb[0])
        y0 = float(bb[2])
        x1 = float(bb[1])
        x2 = float(bb[3])
        draw.rectangle([(x0, y0), (x1, x2)], outline='red')
        if cate is not None and cate != "":
            draw.text((x0, y0), cate, fill="red")
    img = img1
    return img


# In[4]:


from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider

import ali_config

product = "ImageSearch"
region = ali_config.region # via: cn-shanghai(sh), ap-southeast-1(sg)
accessKeyId = ali_config.accessKeyId # via: https://ak-console.aliyun.com
accessKeySecret = ali_config.accessKeySecret
domain = "imagesearch."+ region +".aliyuncs.com"

instanceNameCategory = "testforbc";
instanceNameSimilarity = "general1" #"general1";

region_provider.add_endpoint(product, region, domain)
requestClient = client.AcsClient(accessKeyId, accessKeySecret, region)


# In[5]:


from aliyunsdkimagesearch.request.v20180120.SearchItemRequest import SearchItemRequest

def image_search_category(instanceName, image_path):
    request = SearchItemRequest()

    request.set_instance_name(instanceName)
    request.set_num(20)
    request.set_start(0)

    file_object = open(image_path)
    file_content = None
    try:
        file_content = file_object.read()
    finally:
        file_object.close()

    request.set_search_picture(file_content)

    request.build_post_content()

    result = requestClient.do_action(request)
    return result


# In[6]:


def image_search_result_category(instanceName, image_path):
    result = image_search_category(instanceName, image_path)
    r = json.loads(result)
    category_desc = ''
    for c in r['PicInfo']['AllCategory']['Category']:
        if r['PicInfo']['Category'] == c['Id']:
            category_desc = c['Name']
    r['cate_desc'] = category_desc
    r['cate_id'] = r['PicInfo']['Category']
    #pprint(r)
    display(image_preview(image_path, r['PicInfo']['Region'], category_desc))
    print(image_path, 'found category_desc: ', category_desc, r['PicInfo']['Category'], 'found category_id: ', r['PicInfo']['Category'], 'found region: ',  r['PicInfo']['Region'])
    return r



# In[7]:


# test to search a single image

#instanceName = "testforbc"; # e.g. imagesearchtest
image_name = '5.jpg'
image_folder = '../images_bottle'
image_path = os.path.abspath(image_folder+'/'+image_name)
r = image_search_result_category(instanceNameCategory, image_path)
#cate_id = r['PicInfo']['Category']
#pprint(r)


# In[8]:


from aliyunsdkimagesearch.request.v20180120.AddItemRequest import AddItemRequest

def image_upload_similarity(instanceName, image_name, image_path, cate_id, cate_desc):
    # load file
    file_object = open(image_path)
    file_content = None
    try:
        file_content = file_object.read()
    finally:
        file_object.close()
        
    img_id = get_md5(file_content)
    print('img_id: ', img_id)

    request = AddItemRequest()
    request.set_instance_name(instanceName)
    request.set_cate_id(str(cate_id))
    request.set_item_id(img_id)
    image_content = {'name': image_name, 'path': image_path, 'img_id': img_id, 'cate_id': cate_id, 'cate_desc': cate_desc}
    #pprint(image_content)
    request.set_cust_content(json.dumps(image_content))

    print len(file_content)
    request.add_picture(image_name, file_content)
    request.build_post_content()

    result = requestClient.do_action(request)
    return result



# In[9]:


# test to upload a single image

#instanceName = "testforbcgeneral"; # e.g. imagesearchtest
image_name = '5.jpg'
image_folder = '../images_bottle'
image_path = os.path.abspath(image_folder+'/'+image_name)
r = image_search_result_category(instanceNameCategory, image_path)
#pprint(r)
print(r['cate_id'], r['cate_desc'])
result = image_upload_similarity(instanceNameSimilarity, image_name, image_path, r['cate_id'], r['cate_desc'])
print(image_path, result)


# In[10]:


import os
import time
from pprint import pprint

image_folder = os.path.abspath('../images_bottle')
images = {}
for file in os.listdir(image_folder):
    if file.endswith(".jpg"):
        image_path = os.path.join(image_folder, file)
        #print(os.path.abspath(image_path))
        images[image_path] = file

pprint(images)

for image_path in images:
    image_name = images[image_path]
    r = image_search_result_category(instanceNameCategory, image_path)
    result = image_upload_similarity(instanceNameSimilarity, image_name, image_path, r['cate_id'], r['cate_desc'])
    print(instanceNameSimilarity, image_name, image_path, result)
    time.sleep(1)


# In[11]:


from aliyunsdkimagesearch.request.v20180120.SearchItemRequest import SearchItemRequest

def image_search_similarity(instanceName, image_path):
    request = SearchItemRequest()

    request.set_instance_name(instanceName)
    request.set_num(20)
    request.set_start(0)

    file_object = open(image_path)
    file_content = None
    try:
        file_content = file_object.read()
    finally:
        file_object.close()

    request.set_search_picture(file_content)

    request.build_post_content()

    result = requestClient.do_action(request)
    return result


# In[12]:


def image_search_result_similarity(instanceName, image_path):
    result = image_search_similarity(instanceName, image_path)
    r = json.loads(result)
    #pprint(r)
    category_desc = ''
    for c in r['PicInfo']['AllCategory']['Category']:
        if r['PicInfo']['Category'] == c['Id']:
            category_desc = c['Name']
    #pprint(r)
    
    print(image_path, 'found category_desc: ', category_desc, r['PicInfo']['Category'], 'found category_id: ', r['PicInfo']['Category'], 'found region: ',  r['PicInfo']['Region'])
    
    image_similar_name = json.loads(r['Auctions']['Auction'][1]['CustContent'])['name']
    image_similar_path = json.loads(r['Auctions']['Auction'][1]['CustContent'])['path']
    image_similar_score = r['Auctions']['Auction'][0]['SortExprValues']
    print("similar score: ", image_similar_score, "similar image: ", image_similar_path)
    
    #print(r['Auctions']['Auction'][1])
    
    img1 = image_preview(image_path, r['PicInfo']['Region'], category_desc)
    img2 = image_preview(image_similar_path, '', '')
    
    img_height = img1.size[1]
    if img1.size[1] < img2.size[1]:
        img_height = img2.size[1]
    img = Image.new('RGB', (img1.size[0]+img2.size[0]+40, img_height), "white")
    img.paste(img1, (0, 0))
    img.paste(img2, (img1.size[0]+40, 0))
    
    draw = ImageDraw.Draw(img)
    draw.text((img1.size[0]+20, img_height/2), '=>', fill="red")
    #sim_score = "{0:.0%}".format(float(image_similar_score.split(';')[0]))
    #draw.text((img1.size[0]+20, img_height/2+10), sim_score, fill="red")
    
    #display(img1)
    #display(img2)
    display(img)
    
    return r



# In[13]:


# test to search a single image

#instanceName = "testforbcgeneral"; # e.g. imagesearchtest
image_name = '5.jpg'
image_folder = '../images_bottle'
image_path = os.path.abspath(image_folder+'/'+image_name)
r = image_search_result_similarity(instanceNameSimilarity, image_path)
#pprint(r)


# In[14]:


image_folder = os.path.abspath('../images_bottle')
images = {}
for file in os.listdir(image_folder):
    if file.endswith(".jpg"):
        image_path = os.path.join(image_folder, file)
        #print(os.path.abspath(image_path))
        images[image_path] = file

pprint(images)

for image_path in images:
    image_name = images[image_path]
    r = image_search_result_similarity(instanceNameSimilarity, image_path)
    print("\n=======\n")

