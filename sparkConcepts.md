# Installation and Running it
## Getting everything ready
1. Java Installed:

    sudo apt-get java-jre
    sudo apt-get java-jdk
2. Python Installed (Ubuntu ships with Python 2)
3. Install PySpark

    pip install pyspark

## Running Spark Command Line Interface
1. Download from the [official site](http://spark.apache.org/downloads.html)
2. cd into folder
3. run the following commands for the Python API
    ./bin/pyspark
    spark

# Concepts
* Dataframe: Similar concept to Pandas Dataframe but processing can span multiple machines.
* Partition: Dataframes are broken up to allow parallel processing. Each partition is a chunk of data.
* Transformations: Instructions used to tell Spark to modify the data. Core data structures in Spark are inmutable, so to "change" a Dataframe we need need to isntruct Spark via a transformation.
    
    * Narrow Dependency:each input partition will contribute to only one output partition
    * Wide Dependency: input partitions contributing to many output partitions.
* Spark uses Lazy Evaluation
* Actions: Triggers the actual computation.
