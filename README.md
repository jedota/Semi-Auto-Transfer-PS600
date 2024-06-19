# texture-ps-hda
This repository describes the process of simulating the handcrafted print/scan texture used to create print/scan version images automatically from bona fide examples.
This scenario allows us to train in single and differential morphing Attacks.

# The following steps must be followed:

Step 1) Select 50 colour images and create a pdf.
Step 2) Print and Scan this pdf in a glossy paper with 600 or 300 dpi. This new image includes the artefact from print and scan.
Step 3) Segment each colour image from the scanned file.
Step 4) In order to isolate the texture
Step 5) Translating the base images with the desired textures
To transform your images use the "translate_all_textures_NC.py" from this repository.

It is very important to specify the paths to the textures you want to use, for that we are going to use a cfg.json in which we will specify our textures and their path. 
The JSON file contains one array, "texture_sources," in which you must insert the name of your texture and the path where it is saved. 


This is an example cfg.json:
 
![image](https://github.com/jedota/texture-ps-hda/assets/171809025/35560a6f-4906-4b18-9bfd-220024d034d5)

In the TranslateTexture class, you will find the "self.texture_dir", in which you have to insert the path to your cfg.json.


![image](https://github.com/jedota/texture-ps-hda/assets/171809025/98434cc4-75ea-45a8-b952-c1dc808adc96)



Now we have some options how the images will be translated:


![image](https://github.com/jedota/texture-ps-hda/assets/171809025/1dace6ca-cf4c-4d6d-a1cd-0b2b06f1ebd4)



For the standard way, you just have to specfiy the input/output folders like this:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/4cb70018-e815-4d5c-8646-ae13d4b8e116)

Now the translated images are in the specified output folders, the names of the folders will be the same as you used in the cfg.json:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/63462389-e2c6-4e22-afab-c5a925ea886c)


Example for the translated images:
Original: 


![image](https://github.com/jedota/texture-ps-hda/assets/171809025/7f6ea931-0965-4ed4-92db-0075afa845d8)


B300:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/cb66a698-40fd-46e8-8a95-80ccea0f9e37)


B600:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/ff3d157b-c073-4ae4-a33d-04b0841569de)



G300:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/9918ad86-e8fb-433b-afa4-011cd5cd38ac)


G600:

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/7b28489a-d138-4371-92b4-5b15d4f200fd)


Step 2: Calculating the FID-Scores and storing them for later use

For this step we need to use "calculatedFid,py". 
Here you have to specify the folder containing the orignal images as well as the base folder of your translated images. If your images don't have the correct properties, they will also be transformed
so that the FID-Score can be calculated without errors. By default it will be 480x360, if your images are already correctly translated you can change these values to match your own. Finally, you have to specify your JSON file path, so that the results can be saved.

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/485c8245-2052-4ef1-b3bd-25370d2df15a)

or with height/width specified

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/b24f36b9-2be1-4046-9e3d-baefae773b53)



Now, the orgiinal images folder will be used to compare each FID.Score. Then your translated images base folder will be used to traverse all subfolders of this "base folder" and compare the current subfolder to the original images folder. After the calculations are done, the results will be saved in the specified JSON file.

![image](https://github.com/jedota/texture-ps-hda/assets/171809025/79d67cb6-03a8-4df8-b229-6537f8af3d54)







# Citation
https://github.com/mseitzer/pytorch-fid
# Disclaimer
