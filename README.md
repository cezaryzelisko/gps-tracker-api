# GPS Tracker API

author: Cezary Zelisko

email: cezary.zelisko@gmail.com

## Description
Part of the GPS Tracker project. For more information visit this
[link](https://github.com/cezaryzelisko/gps_tracker).

## Install
In order to install `gps_tracker_api` package you should install all Python requirements.
They are collected in the `requirements.txt` file so to install them at once:

1. navigate to the directory where `gps_tracker` package is stored:

    ```cd /path/to/the/directory/of/gps_tracker_api```

2. issue the following command in a terminal:

    ```sudo pip3 install -r requirements.txt```

3. make sure that `gps_tracker_api` package can be imported (i.e. it's parent directory is
on the `PYTHONPATH`),

## Test
In order to run all tests issue this command from the project directory:

```python3 manage.py test```

## Run
GPS Tracker API server can be run with the following command (remember to navigate to the
package directory first):

```python3 manage.py runserver XXX.XXX.XXX.XXX:PPPP```

where `XXX.XXX.XXX.XXX` is an IP address that this server will be running on and `PPPP`
is a port number.
