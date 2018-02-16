# install.packages("reshape2")
# install.packages("scales")
library(reshape2)
library(scales)
library(plyr)

setwd("/home/fronchetti/Documentos/JBCS-2018") # Working directory
op <- par(oma=c(0,0,5,0), mfrow=c(3,2))

pulls_summary <- read.csv("Dataset/atom/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals_sum$freq, internals_sum$freq, ylim=c(0, 103), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Atom")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/electron/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals_sum$freq, internals_sum$freq, ylim=c(0, 103), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Electron")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/git-lfs/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals_sum$freq, internals_sum$freq, ylim=c(0, 103), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Git-lfs")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/hubot/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals_sum$freq, internals_sum$freq, ylim=c(0, 103), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Hubot")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/linguist/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals_sum$freq, internals_sum$freq, ylim=c(0, 103), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Linguist")), side=3, las=1, adj=0.5, cex=1.3, line = 1)


par(op) # Leave the last plot
op <- par(usr=c(0,1,0,1), # Reset the coordinates
          xpd=NA)         # Allow plotting outside the plot region
legend(0,1.19, # Find suitable coordinates by trial and error
       c("Internals", "Externals"), pch=15, col=c("#727272", "#E6E6E6"), ncol=2, cex=1.5, bty = "n", pt.bg = "black")
# 1000, 750
dev.copy2eps(file="Images/number_of_pull_requests.eps", width = 10, height = 7.5)
dev.off()

