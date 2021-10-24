# Running the Code

To run the code, we need 4 terminals. 

Run `source ./devel/setup.bash` as required for each terminal.

Open the following terminals in sequece and run the commands. Otherwise, the captured output may be incomplete.

Terminal 1 - to run roscore

```bash
$ roscore
```

Terminal 2 - to run the OpenCV code

Change directory to catkin_ws

```bash
$ catkin build && source ./devel/setup.bash && rosrun assignment3 node.py
```

Terminal 3 - to record the output of the program

```bash
$ rosbag record /detected/debug_img/compressed
```

Terminal 4 - to run assignment3.bag

```bash
$ rosbag play assignment3.bag
```

# Viewing the Results

To view the results, run from the appropriate directory

```bash
$ rosbag play <name-of-bag-file>.bag
```

In another terminal, run and select /detected/debug_img/compressed

```bash
$ rqt
```



# Interpreting the Results

A blue contour line of thickness 3 is created around the red region of the roulette.