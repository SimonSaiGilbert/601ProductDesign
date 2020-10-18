I found two segmentation neural networks and decided to implement both. I did this because the implementations are relatively easy and because I wasn't sure which type of segmentation would be most useful for the term project.

## Implementing DeepLab Demo

The iPython Notebook DeepLab_Demo.ipynb runs an implementation of DeepLab to perform image segmentation on data from the PASCAL VOC dataset. The notebook runs in Google Colab and should run without any problems.

## Object Detection Demo

This .ipynb also runs easily in Google Colab and implements either FasterRCNN+InceptionResNet V2 or ssd+mobilenet V2 for object detection.

Both of these notebooks are very "plug-and-play". Enjoy!!

## Implementation for lung segmentation
Both neural networks proved to be less-than-ideal for the task of lung segmentation. The Object Detection demo segments images via rectangular bounding boxes which is not useful for lungs which have oblong shapes that need to be segmented exactly. This is a fundamental flow which precludes the use of this network. The DeepLab demo is optimized for training on RGB color images and is designed for segmenting into a set of class labels comprised of common objects, people, and animals which are relevant for the COCO dataset. This might not necessarily be a problem except that the architecture of this DeepLab is more 'hidden' than I initially thought when I implemented it. Changing the parameters/hyperparameters of the network would involve an entirely new full installation followed by a potentially extensive reworking of the system which doesn't seem like the best course of action at this stage in the project.
