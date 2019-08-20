# Yet another ML Pipelining method

Machine Learning pipelines have been done over and over again. Everyone has 
their own favourite way of doing ML pipelines. Often, library maintainers such
as Tensorflow make it easy to implement a lot of complex pipelines which is
great.

This is no different really. This example actually encompasses two levels
higher than the pipeline itself. 

First is the orchestration of pipelines, and the other is the project.

## The project level 
So why do we need to go two levels higher? Well let's start with the project.
This is pretty simple; a project is a semantic boundary which we draw around
bundles of work or entities. This boundary is helpful to manage billing, 
responsibility of maintenance, and support. The project also provides a single
entrypoint to all the work it can do. For example, we can containerise the 
project tag it and maintain all the moving parts in a clear and concise way.

## The orchestration level
This is one level down from the project; the orchestration. The reason we need
orchestration is because, often ML models are'nt trained and inferenced in
isolation. They often have big pipelines that actually work together in some
way to make a final prediction.

For example; 

* Some of your models need to be fully trained before the next model can start
training.
* You want to group pipelines together in some semantic pattern and but 
orchestrate them together.
* You want to schedule your pipelines based on some other external dependencies
or triggers.


All above the above, require some orchestration code to coordinate the running
of the pipelines. 

## Core Architecture

In order to do this, we use a detached architecture between pipeline, model
and orchestrator. Let's have a look at the below.

### Orchestrator
The orchestrator references the projects entrypoint with arguments on how the
pipeline needs to be instantiated. For example, is it going to be in scoring
or training mode, which image version of the pipeline to use, which pipeline
to run, where the source data is, where to write out the outputs, etc.

### Pipelines
Pipelines define a flow of data through the model. For example, there might
be a pipeline which runs a linear regression model, with some certain features.

Another could be a XGB model which sources expects predictions from the linear
regression model once it's trained. 

Together with using orchestration code, we can stitch together the two 
pipelines to form a disjointed pipeline. 

### Models
Models can be different mathematical objects with their own properties. Ideally
they should provide controls to save their state and reload their state from
persistent storage devices. 

## The project artifact
Make no mistake, the project artifact is a single wrapped object which gives
access to the code which runs the pipelines. Generally this is done by 
constructing a container. 

The container will have arguments to configure the pipelines inside. Many
semantic pipelines can be built this way and bundled together.

Since we don't explicitly keep the model binaries inside the container we can
further decouple the pipelines. 

## Beam programming model

The pipelines here use the Apache Beam programming model, which means that we 
can decouple our running of the pipeline from the pipeline itself. Also
each step in the pipeline can be distributed across various backends and 
physical or virtual machines. 

## Airflow Kubernetes orchestration

Since we are using containers it makes logical sense to use Airflow's
Kubernetes pod operator to orchestrate them. 

Therefore, we have a number of structural elements which are;
* Models which contain the model themselves and how to save state on persistent
storage.
* Pipelines the way to interact with models in a unified model for both Batch
and Streaming.
* The project which encapsulates the logic
* Orchestration which allows to use the project in whatever way you see fit. 
