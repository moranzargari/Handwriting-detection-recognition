# Lines Detection

We first examined in literature what algorithms are used today to separate the lines in an image containing handwritten text. During the search, we found many solutions to the problem and finally, we decided to focus on the three most common algorithms we've seen. (the code files is in "lines detection" folder).

* FindConturs
* MSER
* Reduce

Also, we wrote our own algorithm called "sumPixels".
In order to find out who is the best algorithm, we have defined a statistical measure that examines the four algorithms (we use the images collection folder).
After the comparison, we found out that our algorithm is the best, so we decided to use it to detect the lines in our project.
(the code file and the CSV files is in "lines detection/statistic" folder)
