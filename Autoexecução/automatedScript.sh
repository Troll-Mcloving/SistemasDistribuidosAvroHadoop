#/bin/bash
HADOOP_INPUT="/grupo05sd/input"
HADOOP_OUTPUT="/grupo05sd/output"
PYTHON="python3.5"

eval "export HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar"
eval "hadoop com.sun.tools.javac.Main ParallelDijkstra.java"
eval "jar cf dijkstra.jar ParallelDijkstra*.class"

eval "hadoop fs -mkdir $HADOOP_INPUT"
eval "mkdir ./Data"
eval "mkdir ./output"
eval "mkdir ./logs"
eval "tar -xzvf ICMC.tar.gz"
eval "$PYTHON gravacao.py"

for a in `seq 2760`
do
	STRING="LattesGraph"
	TYPE=".txt"
	NAME=$STRING$a$TYPE
	eval "hadoop fs -put ./Data/$NAME $HADOOP_INPUT"
	eval "hadoop fs -mkdir $HADOOP_OUTPUT"
	eval "time hadoop jar dijkstra.jar ParallelDijkstra $HADOOP_INPUT $HADOOP_OUTPUT > ./logs/Log-Hadoop-$a.txt"
	eval "hadoop fs -get $HADOOP_OUTPUT/part-r-00000 ./output/part-r-$a"
	eval "hadoop fs -rm -r $HADOOP_OUTPUT"
	eval "hadoop fs -rm $HADOOP_INPUT/$NAME"
done

eval "$PYTHON postProcess.py"
