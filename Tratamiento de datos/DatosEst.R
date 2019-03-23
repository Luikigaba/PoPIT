setwd("/home/lgbaquero/Descargas/Madrid")

library(dplyr)
library(readr)
library(stringi)
library(reshape2)
library(tidyr)

files = list.files(full.names = TRUE)
files = files[stri_detect_fixed(files, "csv")]

df <- files %>% 
  lapply(read_delim,delim=";",col_types = "iiiiccccdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdc") %>% 
  bind_rows 

df <- data.frame(df)

df[,9:24]<-df[35:56]<-NULL

df$H10 <- paste(df$H10,df$V10,sep="")
df$H11 <- paste(df$H11,df$V11,sep="")
df$H12 <- paste(df$H12,df$V12,sep="")
df$H09 <- paste(df$H09,df$V09,sep="")
df$H13 <- paste(df$H13,df$V13,sep="")

df$V10<-df$V11<-df$V12<-df$V09<-df$V13<-df$PROVINCIA<-df$MUNICIPIO<-df$PUNTO_MUESTREO<-NULL

melteddf <- melt(df,id.vars = 1:5,measure.vars = 6:10)
names(melteddf) <- c("ESTACION","MAGNITUD","ANO","MES","DIA","HORA","MEDIDA")

df <- melteddf
df$HORAS[as.character(df$HORA)=="H10"] <- "10"
df$HORAS[as.character(df$HORA)=="H11"] <- "11"
df$HORAS[as.character(df$HORA)=="H09"] <- "09"
df$HORAS[as.character(df$HORA)=="H12"] <- "12"
df$HORAS[as.character(df$HORA)=="H13"] <- "13"

df$HORA <- NULL

write_csv(df,'MadComp.csv')
