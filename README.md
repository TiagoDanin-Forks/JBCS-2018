# JBCS-2018
In this repository you will find all the necessary steps to replicate the method available in the paper "Who Drives Company-Owned OSS Projects: Internals or Externals Members?", published at JBCS 2018.

## Reproducing the dataset:
If you want to create your own version of the dataset execute the file "<i>get_data.py</i>" [[1]](https://github.com/fronchetti/JBCS-2018/blob/master/get_data.py) using Python 2.7. After the script execution, all the files will be saved in a folder called "Dataset", and you may need to allow this process in your system. We have already made available a ready copy of this folder in this repository [[2]](https://github.com/fronchetti/JBCS-2018/tree/master/Dataset). Feel free to add new projects to the dataset during the process execution by adding them in line 410 of "<i>get_data.py</i>".

### Dataset Structure:
⋅⋅* Dataset: <br>
⋅⋅*⋅⋅*⋅⋅* Project: <br>
⋅⋅*⋅⋅*⋅⋅*⋅⋅*⋅⋅* casual_contributors.csv (General information about casual contributors in the project)<br>
⋅⋅*⋅⋅*⋅⋅*⋅⋅*⋅⋅* external_contributors.csv (General information about external contributors in the project<br>
⋅⋅*⋅⋅*⋅⋅*⋅⋅*⋅⋅* closed_pull_requests_summary.csv (Summary with general information about closed pull requests)<br>
⋅⋅*⋅⋅*⋅⋅*⋅⋅*⋅⋅* merged_pull_requests_summary.csv (Summary with general information about merged pull requests)<br>
