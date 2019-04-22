# Hebrew letters dataset:
Building a handwritten Hebrew letters dataset is one of the stages in the project planning.
At this stage we would like to recognize the letters that we detected, and to do so, we will need a set of letters written in Hebrew.
First, we conducted a thorough search for Hebrew alphabet on the network, and also we looked for this kind of database in national libraries. Unfortunately, we were unable to locate this type of letter dataset. So we decided to build such a dataset ourselves.


## The dataset building blocks:
* Create a page containing 270 slots - used as a designated place to fill 10 samples of each letter - (total of 27 letters in Hebrew) - you can view the format [here](https://github.com/moranzargari/Handwriting-detection-recognition/blob/master/Letters%20Dataset%20Collection/page.jpg?raw=true)
* Distribute the page to people to get as many different types of handwriting as possible from the language.
* Scan all full pages - Link to scanned pages
* Writing a program in Python that knows how to extract the letters written to a desired format from the page - a link to the code we wrote in Python
* We received a letter dataset when each letter is a letter of size X pixels and from each letter we have Y performances - a link to the letters folders
