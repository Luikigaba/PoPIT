setwd("/home/lgbaquero/Descargas/H4G")

library(dplyr)
library(readr)
df <- list.files(full.names = TRUE) %>% 
  lapply(read_csv) %>% 
  bind_rows 

df <- data.frame(df)

namescust <- c("Fecha","Torre","Nubes","B02","B03","B04","B08","B05","B06","B07","B11","B12",
               "B01","B09")
names(df) <- namescust
names(df)

estacion <- c(4,8,11,16,17,18,24,27,35,36,38,39,40,47,48,49,50,54,55,56,57,58,59,60)
estequiv <- data.frame(Torre = 0:23, Estacion=estacion)

df <- merge(df,estequiv,by='Torre')
df$Torre <- NULL

write_csv(df,'SentComp.csv')
