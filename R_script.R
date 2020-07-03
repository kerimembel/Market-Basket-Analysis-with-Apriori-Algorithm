library(arules)
library(arulesViz)
library(tidyverse)
library(readxl)
library(knitr)
library(lubridate)
library(plyr)
library(dplyr)

tr <- read.transactions('data\\groceries.csv', format = 'basket', sep=',',skip = 1)
inspect(tr)

if (!require("RColorBrewer")) 
  {
  # install color package of R
  install.packages("RColorBrewer")
  #include library RColorBrewer
  library(RColorBrewer)
}

itemFrequencyPlot(tr,topN=10,type="absolute",col=brewer.pal(8,'Pastel2'), main="Absolute Item Frequency Plot")
itemFrequencyPlot(tr,topN=10,type="relative",col=brewer.pal(8,'Pastel2'),main="Relative Item Frequency Plot")

association.rules <- apriori(tr, parameter = list(supp=0.01, conf=0.6))
write(association.rules, file = "results\\rResultssupp001conf06.csv", sep=",")
inspect(association.rules[1:5])

rules <- apriori(tr, parameter = list(supp = 0.001, conf = 0.8))
write(association.rules, file= "results\\rResultssupp0001conf08.csv", sep=",")

rulesForPlot <- apriori(tr, parameter = list(supp = 0.01, conf = 0.2))
inspect(rulesForPlot,rules[1:10])

plot(rulesForPlot,method="graph",interactive=TRUE,shading=NA)