library(dplyr)
library(sf)
library(stringr)

tiles_relevant = c("32UQB", "33UUS", "32UPB")

a = st_read("/home/robin/Desktop/S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml")
head(a$Name)
class(a$Name)

tiles = a %>% select(Name) %>% filter(stringr::str_detect(Name, pattern = "32|33"))
tiles = tiles[tiles$Name %in% tiles_relevant, ]



