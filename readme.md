# Simple visualizer for Statsbomb open data

Installation instructions
-------------------------
Create virtualenv and install requirements:
```bash 
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
        
# Configuration

If you are using PyCharm, the IDE should automatically detect the requirements.txt file and install the requirements.

This repository doesn't include the actual data. You must download the Statsbomb open data package from https://github.com/statsbomb/open-data
and set the correct path to config.py - just change the value to the directory you have extracted the data package into. By default the 
path is set to `open-data-master`, which assumes that the data has been copied into the base directory of the Python project.
    
# Running the application

In order to run the streamlit package, you should follow the documentation in https://streamlit.io/ . Hint: streamlit run main.py 

In PyCharm, you can define a new Python run target, by following the instructions in https://discuss.streamlit.io/t/run-streamlit-from-pycharm/21624/15 (please see dvrkdvys' comments from May 23, 2022)