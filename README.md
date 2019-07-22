# Demo with ImageSearch API version 20190325 and be ready for kubernetes
imagesearch for predownload images: [demo_imagesearch_product_static.ipynb](https://github.com/jianhuashao/AlibabaCloud_ImageSearch_Demo_py2/blob/master/demo_imagesearch_product_static.ipynb)

imagesearch for images downloaded from aliexpress in realtime: [demo_imagesearch_product-dynamic.ipynb](https://github.com/jianhuashao/AlibabaCloud_ImageSearch_Demo_py2/blob/master/demo_imagesearch_product-dynamic.ipynb)

Pls set environment for key and ID by: `source set_secret.sh`

```sh
# set secret for imagesearch
cp set_secret.sh.temp set_secret.sh
vi edit set_secret.sh
source set_secret.sh
jupyter notebook
# check: demo_imagesearch_product_static.ipynb
# check: demo_imagesearch_product-dynamic.ipynb # images are download from aliexpress in realtime
```
