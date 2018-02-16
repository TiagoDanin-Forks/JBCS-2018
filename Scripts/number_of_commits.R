# install.packages("reshape2")
# install.packages("scales")
library(reshape2)
library(scales)

setwd("/home/fronchetti/Documentos/JBCS-2018") # Working directory
par(mfrow=c(3,2))

pulls_summary <- read.csv("Dataset/atom/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals$number_of_commits, internals$number_of_commits, ylim=c(0,17), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Atom")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/electron/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals$number_of_commits, internals$number_of_commits, ylim=c(0,17), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Electron")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/git-lfs/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals$number_of_commits, internals$number_of_commits, ylim=c(0,17), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Git-lfs")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/hubot/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals$number_of_commits, internals$number_of_commits, ylim=c(0,17), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Hubot")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

pulls_summary <- read.csv("Dataset/linguist/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
mar.default <- c(4,1,4,1) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals$number_of_commits, internals$number_of_commits, ylim=c(0,17), xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=2, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#E6E6E6", "#727272")))
mtext(expression(bold("Linguist")), side=3, las=1, adj=0.5, cex=1.3, line = 1)

# 1000, 750
dev.copy2eps(file="Images/number_of_commits.eps", width = 10, height = 7.5)
dev.off()

