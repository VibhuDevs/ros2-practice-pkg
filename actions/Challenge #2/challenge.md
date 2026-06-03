This was a practice challenge in which I was supposed to simulate a hand movement for an imaginary robot that takes joint values bw -180 to 180. Here, I took three joint values and tried to get them to a target value using basic if and else loops. The user can cancel the movement in between and the movement will stop in between giving the current values for it's joints.

Future applications can be used in cobots. In case of any mishappening, the user may cancel the movement whenever they want. Although it's very unrefined tbh.

I used the following:
I used arrays to take target_angles and set the initial_angles
Looked into each element of the array and made them equal to each of the elements inside final output
I made a cancel and a response callback


