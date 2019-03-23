setwd('/Volumes/Transcend/Sentinel')

library(readr)
library(lubridate)
library(tidyr)
library(xgboost)
library(dplyr)
library(magrittr)

sent <- data.frame(read_csv('SentComp.csv'))
madridata <- data.frame(read_csv('MadComp.csv'))

sent$DIA <- day(sent$Fecha)
sent$MES <- month(sent$Fecha)
sent$ANO <- year(sent$Fecha)
sent$HORAS <- hour(sent$Fecha)
colnames(sent)[colnames(sent)=='Estacion'] <- 'ESTACION'

dataset <- merge(sent,madridata,how="inner",by=c("ANO","MES","DIA","HORAS","ESTACION"))

dataset <- dataset[grepl("V",dataset$MEDIDA)==TRUE,]

dataset$MEDIDA<-as.numeric(sapply(dataset$MEDIDA,function(x) strsplit(x,"V")[[1]],USE.NAMES=FALSE))

#7,12,8

datacom <- dataset[dataset$MAGNITUD==12,c(8:18,20)]
datacom <- datacom[datacom$MEDIDA<300,]

datacom[1:12] <- sapply(datacom[1:12],as.numeric)

model <- xgboost(as.matrix(datacom[,1:11]),as.matrix(datacom[,12]),nrounds=5)

set.seed(1234)

datacom <- datacom[sample(nrow(datacom)),]

itext <- 1:204
itrain <- 205:258

testset <- datacom[itext,]
trainset <- datacom[itrain,]

errors <- c()

vartot <- names(datacom)
vartot <- vartot[1:11]

vars <- c("B09","B01","B02","B08")
for (k in itrain){
  
  index <- 1:nrow(trainset)
  index <- index[-k]
  dtrain <- xgb.DMatrix(as.matrix(trainset[index,vars]), label = as.matrix(trainset[index,12]))
  
  set.seed(1234)
  model <- xgboost(dtrain,nrounds=5,verbose=0,max_depth=2)
  
  prediction <- predict(model,as.matrix(trainset[k,vars]))
  
  error <- abs(prediction-as.matrix(trainset[k,"MEDIDA"]))
  
  errors <- c(errors,error)
}

predictions <- predict(model,as.matrix(testset[,vars]))
errors <- abs(predictions-testset$MEDIDA)
errors <- mean(errors)/(max(testset$MEDIDA)-min(testset$MEDIDA))




sevilla<-data.frame()

