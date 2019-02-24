# kerry-logistics-drone-ai-hackathon Group 5

It turns out that we are going to do the flight manually and do the preprocessing afterward. 

## Our original design of automatic flight

We use the compass sensor (Hall effect sensor) in the drone to calibrate the unstable movement in the flight, so that it can fly in a straight line and the path is exactly parallel with the aisle. 

## However it doesn't work, it drifts a lot.

We spent whole night debugging, but it still drifts a lot.
We thought it was the problem due to resolution, update rate or hardware unstable, we tried lots of way to reduce the problem.
But it still drafts.

## Reason of drafting

We turn out found that there is a strong magnetic field under our aisle. We confirm it by a magnetic sensor, the magnetic field is two times the normal reading than in other location in the room. And this doesn't happen in another aisle we tested.

## Since no time, So we switch to manual flying

Since there is already no time for our time for us to fine tune our algorithm even the organiser may allow us to switch the aisle in the morning, we decide to use manual mode.

# Anyway, we have a Robust, Fault-Tolerance post-processing algorithm to match all the QR codes after manual flying

## Reason of not using any neural network algorithm
It is an overkill to use a such complex model for such a constrainted problem which can be solved with simple model.

Neural network introduces a lot of uncertainty since we dont have a really large dataset. What is suggested is just a transfer learning of an existing image recognition model by changing the last layer. That model is not designed specially for our use case. It sometimes works not well. So we don't use them.

I do think that unless we are doing visual navigation, which may require a reinforcement learning (using neural nnetwork), we dont have to use any neural network in solving the problem defined.

## A simple model with feature engineering

We do some feature engineering, analyze the data, and do some calculations with geometry. We can create a simple model with very best preformance. We dont have to train them

## In most of our test case, we get 100% accuracy!

That's why we dont need to use any neural network model.


# Use a simpler model if we can. Data science 101!
