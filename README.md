## Project Demo

[](https://youtu.be/xih-XiKhoQ4)

## Problem

With an ever-increasing supply of software solutions being made each day, the energy consumption of the technology industry is sky-rocketing, and thus also its impact towards the environment.

Until now, there has been very little consideration of the sustainability costs in the software engineering workflow. Taking consideration of the environmental impact (such as the carbon emissions and electricity consumption of newly deployed code) is indeed incredibly important. However, oftentimes it is entirely ignored due to the hassles and inefficiencies it adds to the engineering process.

## Solution

By creating a seamless integration to the software engineering Github CI/CD pipeline, we offer automatic server renting costs, electricity consumption and carbon emissions estimation for every commit.

Even more impressively, we perform these estimations using a machine learning model which predicts the runtime of pushed code without running the code itself! This allows for integrating sustainability much earlier on in the engineering cycle, further facilitating taking serious consideration of the environmental impacts while designing software products.

In addition to this, we provide detailed information through a frontend view (accessible from Github itself) which allows software engineers and architects to receive actionable advice to reduce their carbon footprint and costs. Notably, we are able to provide optimal hardware configurations to use thanks to our runtime and memory prediction of the code (drastically saving deployment costs). We are additionally able to recommend deployment server regions across the world which are produced with low-carbon intensity electricity.

### What inspired us

As a team of Computer Scientists from EPFL, we have always sought to find ways to reduce our environmental impact through the use of technology! We noticed very early on that the Computer Science engineering workflow hardly took into consideration the environmental factors and tried to find seamless ways to integrate this into our workflow.

Speaking to the AXA engineers really helped us to see that this is indeed a problem with the software engineering workflow and that there should be much more awareness for the sustainability impact in the engineering workflow, which is what we tackled.

It was also great to think about it from the eyes of an EPFL student, we can certainly see the benefit of gaining this additional awareness about how much energy is consumed by our code and how much carbon is produced. Additionally, we found it very helpful to receive comparisons of our code electricity/carbon values to everyday objects such as the car journeys.

### What we learned
Working on this project allowed us to develop many different skills in a short amount of time and understand much more about the software workflow. We are incredibly happy with what we were able to build in just 24 hours.

We learned many different technologies, some that we were previously familiar with and many which we had to learn on the fly! We worked with machine learning models, transformers, Github CI/CD, Svelte, Ngrok, Python, Javascript. Read below to see how we built our project (and more details about the different technologies we used)

We more importantly had an incredible amount of fun and excitement being able to work on a technology which we believe will have a huge impact on the technology industry, and seeing how to design a product which integrates seamlessly while providing utility!

## How we built our project

To build our project we divided up the tasks between our 4 members:

One member worked on a GPT-3 based code memory and runtime prediction model
One member worked on a SVM model to predict the runtime of code based on similar functions and their runtimes
We had another member work on the Github CI/CD pipeline and set-up, as well as researching how to integrate our process as seamlessly as possible for the end users
We also developed a backend server (which we made publicly accessible through an Ngrok tunnel to avoid hosting costs) where we computed the costs of server renting, electricity and carbon emissions by aggregating data from multiple sources (Google Cloud Provider, Exoscale, Electricity Maps, ...).
We made our calculations accessible through API endpoints, which we then set-up a basic Svelte application to visualize this data
Overall, we created a full-rounded application using many different technologies and integrations, in such a short time. At each step of the process, we always focused on our user (software engineers/architects) and finding the optimal solution to their needs (seamless integration of sustainability data).

## Challenges we faced


Our app estimates the runtime of an algorithm without having the run it, in itself this challenge if solved fully would solve the halting problem. Nevertheless, we realised that with feature expression analysis the problem of estimating an algorithms runtime could be solved with this Natural Language Procession Machine Learning approach.

We decided to divide the tasks between each other so as to optimise the speed to which we would code the algorithm and its deployment as a GitHub action feature. The challenges faced by those creating the algorithm was the creation of a machine learning algorithm to properly identify the flow control of a given input code to properly estimate the asymptotic bounds of the code. Once we found a sufficiently big dataset to use as a validation and testing sets we were faced with the challenge of creating a robust AI capable of estimating the runtime of the algorithm in a precise way.

## Papers used

Learning based Methods for Code Runtime Complexity Prediction by Adobe and IIT Delhi, 4 Nov 2019 (https://arxiv.org/abs/1911.01155)

