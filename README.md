
# Hostel_mgmt
Package for Hostel Management Project

__Package name__: `hostel_mgmt`<br>
__Package description__: *Python Package for managing records and databases that are required in managing the resources and data of a hostel viz. Student Details, Block details, Mess details etc.*

Be sure to run the create_all.py before running the main program, set the Windows theme to default(if any external theme is installed) and install the external libraries used. Else, the system won't run properly and would throw errors.

Contains a `run_app.py` which imports the main package `hostel_mgmt`. Inside the package `hostel_mgmt`, we have an `__init__.py` file which initializes the whole package by creating the skeleton GUI. Other files included in the package are `admncrd.py`, `auth.py`, `center_frame.py`, `design.py`, `left_frame.py`, `left_frame_func.py`, `right_frame.py` and `right_frame_func.py`.

Outside the package, apart from `run_app.py`, we have one image `Fee Chart.png` and a binary file `pvt.dat`.

__Structure of `hostel_mgmt` package:__

```
rootdir:.
│   create_all.py
│   Fee Chart.png
│   pvt.dat
│   run_app.py
│
└───hostel_mgmt
        admncrd.py
        auth.py
        center_frame.py
        design.py
        gen_details_pdf.py
        gen_pdf.py
        left_frame.py
        left_frame_func.py
        models.py
        right_frame.py
        right_frame_func.py
        support_queries.py
        __init__.py
```
