# Script which takes 3 arguments, the path of the
# training set, the number of clusters and the test set.

library(clue)
args <- commandArgs(trailingOnly = TRUE)

# transform the training set
# keep the last column which is the rating
mydata <- read.table(args[1])
mydata <- mydata[,0:(length(mydata[])-1)]

# compute k-means clustering
k <- kmeans(scale(mydata), as.integer(args[2]))

# compute classification to predict where each
# row has to go (in which cluster)
test <- read.table(args[3])
test <- test[,0:(length(test[])-1)]
pre <- cl_predict(k, scale(test))

#output the results
k$cluster
pre