# install.packages("ggplot2")
# install.packages("reshape2")
# install.packages("scales")
library(ggplot2)
library(reshape2)
library(scales)

setwd("/home/fronchetti/Documentos/JBCS-2018") # Working directory

##################
# PULL REQUESTS  #
#   PER MONTH    #
##################
# File type: EPS
# Chart type: Time series (Line)
# W: 600 H: 400

# Change the path according to the project
pulls_per_month <- read.csv("Dataset/git-lfs/pull_requests_per_month.csv", colClasses=c("Date",NA, NA, NA))

data <- subset(pulls_per_month, pull_type == "opened")
ggplot(data, aes(x=month, y=pull_amount, colour=user_type, group=user_type)) +
  scale_x_date(breaks = date_breaks("years"), labels = date_format("%Y"), limits = as.Date(c('2011-01-01','2018-02-01'))) + ylim(0, 80) + 
  geom_line(size=1.2, aes(linetype = user_type)) + scale_color_manual(values=c("#00C853", "#1565C0")) + 
  labs(x = "Years", y = "# Occurrences") + theme( legend.title=element_blank(), axis.text=element_text(size=14), legend.position="top", axis.text.x = element_text(size=13, color="#000000"), axis.text.y = element_text(size=13, color="#000000"))
dev.copy2eps(file="Images/git-lfs/git-lfs_opened_pulls_series.eps", width = 6, height = 4)
dev.off()

data <- subset(pulls_per_month, pull_type == "merged")
ggplot(data, aes(x=month, y=pull_amount, colour=user_type, group=user_type)) +
  scale_x_date(breaks = date_breaks("years"), labels = date_format("%Y"), limits = as.Date(c('2011-01-01','2018-02-01'))) + ylim(0, 80) + 
  geom_line(size=1.2, aes(linetype = user_type)) + scale_color_manual(values=c("#00C853", "#1565C0")) + 
  labs(x = "Years", y = "# Occurrences") + theme(legend.title=element_blank(), axis.text=element_text(size=14), legend.position="top", axis.text.x = element_text(size=13, color="#000000"), axis.text.y = element_text(size=13, color="#000000"))
dev.copy2eps(file="Images/git-lfs/git-lfs_merged_pulls_series.eps", width = 6, height = 4)
dev.off()

data <- subset(pulls_per_month, pull_type == "closed")
ggplot(data, aes(x=month, y=pull_amount, colour=user_type, group=user_type)) +
  scale_x_date(breaks = date_breaks("years"), labels = date_format("%Y"), limits = as.Date(c('2011-01-01','2018-02-01'))) + ylim(0, 80) + 
  geom_line(size=1.2, aes(linetype = user_type)) + scale_color_manual(values=c("#00C853", "#1565C0")) + 
  labs(x = "Years", y = "# Occurrences") + theme(legend.title=element_blank(), axis.text=element_text(size=14), legend.position="top", axis.text.x = element_text(size=13, color="#000000"), axis.text.y = element_text(size=13, color="#000000"))
dev.copy2eps(file="Images/git-lfs/git-lfs_closed_pulls_series.eps", width = 6, height = 4)
dev.off()

##################
# PULL REQUESTS  #
#    SUMMARY     #
##################
# File type: EPS
# Chart type: Boxplot
# W: 650 H: 360

pulls_summary <- read.csv("Dataset/git-lfs/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA))

internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")

boxplot(externals$number_of_days, internals$number_of_days, xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=1.5, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#b8d1ed", "#aae0c0")))
legend("topright", legend=c("Internals", "Externals"), fill=c("#aae0c0", "#b8d1ed"), inset= .0, cex=1, ncol=2)
dev.copy2eps(file="Images/git-lfs/git-lfs_days_amount.eps", width = 6.5, height = 3.6)
dev.off()

boxplot(externals$number_of_commits, internals$number_of_commits, xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=1.5, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#b8d1ed", "#aae0c0")))
legend("topright", legend=c("Internals", "Externals"), fill=c("#aae0c0", "#b8d1ed"), inset= .0, cex=1, ncol=2)
dev.copy2eps(file="Images/git-lfs/git-lfs_commits_amount.eps", width = 6.5, height = 3.6) 
dev.off()

boxplot(externals$number_of_comments, internals$number_of_comments, xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=1.5, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#b8d1ed", "#aae0c0")))
legend("topright", legend=c("Internals", "Externals"), fill=c("#aae0c0", "#b8d1ed"), inset= .0, cex=1, ncol=2)
dev.copy2eps(file="Images/git-lfs/git-lfs_comments_amount.eps", width = 6.5, height = 3.6)
dev.off()

mar.default <- c(5,4,4,2) + 0.1
par(mar = mar.default + c(0, 5, 0, 0)) 
boxplot(externals$number_of_additions, internals$number_of_additions, externals$number_of_deletions, internals$number_of_deletions, externals$number_of_files_changed, internals$number_of_files_changed, xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=1.5, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), at = c(1,2,4,5,7,8), col=(c("#b8d1ed", "#aae0c0","#b8d1ed", "#aae0c0","#b8d1ed", "#aae0c0")))
mtext("Files Changed", side=2, at=1.5, las=1, outer=FALSE, adj=1.1, cex=1.5)
mtext("Deletions", side=2, at=4.5, las=1, outer=FALSE, adj=1.2, cex=1.5)
mtext("Additions", side=2, at=7.5, las=1, outer=FALSE, adj=1.2, cex=1.5)
legend("topright", legend=c("Internals", "Externals"), fill=c("#aae0c0", "#b8d1ed"), inset= .0, cex=1, ncol=2)
dev.copy2eps(file="Images/git-lfs/git-lfs_changes_amount.eps", width = 8.5, height = 4.6)
dev.off()

library(plyr)
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")
boxplot(externals_sum$freq, internals_sum$freq, xlab="# Occurrences", las = 1, outline = FALSE, cex.lab=1.5, cex.axis = 1.5, horizontal = TRUE, margin = list(l = 10, r = 10, b = 0, t = 0), col=(c("#b8d1ed", "#aae0c0")))
legend("topright", legend=c("Internals", "Externals"), fill=c("#aae0c0", "#b8d1ed"), inset= .0, cex=1, ncol=2)
dev.copy2eps(file="Images/git-lfs/git-lfs_pulls_amount.eps", width = 6.5, height = 3.6)
dev.off()


