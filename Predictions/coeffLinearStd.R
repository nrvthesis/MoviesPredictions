# Script which takes 1 arguments, the path of the
# data set. The script print the coefficients
# of the linear regression

args <- commandArgs(trailingOnly = TRUE)
mydata <- read.table(args[1])
data <- mydata[,0:(length(mydata[])-1)]
y <- mydata[,(length(mydata[]))]
model <- lm(y~., data)
coefficients(model)