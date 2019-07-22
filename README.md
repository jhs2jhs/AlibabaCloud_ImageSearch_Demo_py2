# Demo with ImageSearch API version 20190325 and be ready for kubernetes
[demo_imagesearch_product.ipynb](https://github.com/jianhuashao/AlibabaCloud_ImageSearch_Demo_py2/blob/master/demo_imagesearch_product.ipynb)
Pls set environment for key and ID by:
```sh
# set secret for imagesearch
cp set_secret.sh.temp set_secret.sh
vi edit set_secret.sh
source set_secret.sh
jupyter notebook
# check: demo_imagesearch_product_static.ipynb
# check: demo_imagesearch_product-dynamic.ipynb # images are download from aliexpress in realtime
```


----

also moved all historical file into "code_backup_for_historical" folder


# Demo with api version 20190325

[app_image_search_general_v20190510_1.ipynb](https://github.com/jianhuashao/AlibabaCloud_ImageSearch_Demo_py2/blob/master/app_image_search_general_v20190510_1.ipynb)

Pls set environment for key and ID by:
```sh
export accessKeyId="xx"
export accessKeySecret="yy"
```

# This works only with previous version of API and is now deprecated.

[py2 notebook demo](https://github.com/jianhuashao/AlibabaCloud_ImageSearch_Demo_py2/blob/master/app_image_search_py2.ipynb)
