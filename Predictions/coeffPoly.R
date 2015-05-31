# Script which takes 1 arguments, the path of the
# data set. The script print the coeeficients
# of the polynomial regression (scale the data)


args <- commandArgs(trailingOnly = TRUE)
mydata <- read.table(args[1])
data <- mydata[,0:(length(mydata[])-1)]
y <- mydata[,(length(mydata[]))]

# the star is used as a marker to generate all
# the variable with a python script
model <- lm(scale(y)~ *)
coefficients(model)