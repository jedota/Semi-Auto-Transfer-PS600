# texture-ps-hda
This repository describes the process of simulating print/scan texture used to create print/scan version images from bona fide examples.

# The following steps must be followed:

Step 1: Translating the base images with the desired textures
To transform your images use the "translate_all_textures_NC.py" from this repository.

It is very important to specify the paths to the textures you want to use. 
In the TranslateTexture class you will find the "self.texture_dir", in which you have to insert the paths to your textures.


![image](https://github.com/jedota/texture-ps-hda/assets/171809025/98434cc4-75ea-45a8-b952-c1dc808adc96)

The JSON file contains one array "texture_sources", in which you will have to insert the name of your texture as well as the path where it is saved. 


This is an example cfg.json:
 
![image](https://github.com/jedota/texture-ps-hda/assets/171809025/35560a6f-4906-4b18-9bfd-220024d034d5)





@MAX, explain all the protocols similar to PPT. All the files used must be included here (no database). please indicate how to use the Python function, and include examples of images, too.
Goal: One person must be able to replicate all the processes only following this GitHub.



# Citation
# Disclaimer
