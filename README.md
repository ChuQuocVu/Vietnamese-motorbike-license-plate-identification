# Vietnamese-motorbike-license-plate-identification

* Detect plates using OpenCV 
* Recognize characters using VGG16
* Download weight, then put in Model folder: https://drive.google.com/file/d/1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-/view?usp=sharing

1. Run project:
  * Install packages in requirements.txt
  * Run file run.py

2. Advantages:
  * Simpler than using YoLo4 and darknest.
  * Detect plates using opencv only.
  
3. Defect:
  * Sometime confused between "T" and "1", "4" and "Z".
  * Model won't work well when the photoes are too dark.
  
