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

Now we have some options how the images will be translated:


![image](https://github.com/jedota/texture-ps-hda/assets/171809025/1dace6ca-cf4c-4d6d-a1cd-0b2b06f1ebd4)



For the standard way, you just have to specfiy the input/output folders like this:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/4cb70018-e815-4d5c-8646-ae13d4b8e116)

Now the translated images are in the specified output folders, the names of the folders will be the same as you used in the cfg.json:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/63462389-e2c6-4e22-afab-c5a925ea886c)






@MAX, explain all the protocols similar to PPT. All the files used must be included here (no database). please indicate how to use the Python function, and include examples of images, too.
Goal: One person must be able to replicate all the processes only following this GitHub.



# Citation
# Disclaimer
