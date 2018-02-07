require("effsize")

setwd("/home/fronchetti/Documentos/JBCS-2018") # Working directory

pulls_per_month <- read.csv("Dataset/hubot/pull_requests_per_month.csv", colClasses=c("Date",NA, NA, NA))

# Opened Pulls (Per Month)
data <- subset(pulls_per_month, pull_type == "opened")
internals <- subset(data, user_type == "Internals")
externals <- subset(data, user_type == "Externals")
wilcox.test(internals$pull_amount, externals$pull_amount)
cliff.delta(internals$pull_amount, externals$pull_amount)

# Closed Pulls (Per Month)
data <- subset(pulls_per_month, pull_type == "closed")
internals <- subset(data, user_type == "Internals")
externals <- subset(data, user_type == "Externals")
wilcox.test(internals$pull_amount, externals$pull_amount)
cliff.delta(internals$pull_amount, externals$pull_amount)

# Merged Pulls (Per Month)
data <- subset(pulls_per_month, pull_type == "merged")
internals <- subset(data, user_type == "Internals")
externals <- subset(data, user_type == "Externals")
wilcox.test(internals$pull_amount, externals$pull_amount)
cliff.delta(internals$pull_amount, externals$pull_amount)

pulls_summary <- read.csv("Dataset/git-lfs/merged_pull_requests_summary.csv", colClasses=c(NA, NA, NA, NA, NA, NA, "Date", NA, NA, NA, NA, NA))
internals <- subset(pulls_summary, user_type == "Internals")
externals <- subset(pulls_summary, user_type == "Externals")
externals <- externals[which(externals$number_of_additions != 0 | externals$number_of_deletions != 0 | externals$number_of_files_changed != 0),]
internals <- internals[which(internals$number_of_additions != 0 | internals$number_of_deletions != 0 | internals$number_of_files_changed != 0),]

# Number of additions
wilcox.test(internals$number_of_additions, externals$number_of_additions)
cliff.delta(internals$number_of_additions, externals$number_of_additions)

# Number of deletions
wilcox.test(internals$number_of_deletions, externals$number_of_deletions)
cliff.delta(internals$number_of_deletions, externals$number_of_deletions)

# Number of files changed
wilcox.test(internals$number_of_files_changed, externals$number_of_files_changed)
cliff.delta(internals$number_of_files_changed, externals$number_of_files_changed)

# Number of days
wilcox.test(internals$number_of_days, externals$number_of_days)
cliff.delta(internals$number_of_days, externals$number_of_days)

# Number of commits
wilcox.test(internals$number_of_commits, externals$number_of_commits)
cliff.delta(internals$number_of_commits, externals$number_of_commits)

# Number of comments
wilcox.test(internals$number_of_comments, externals$number_of_comments)
cliff.delta(internals$number_of_comments, externals$number_of_comments)

library(plyr)
internals_sum <- count(internals, "user_login")
externals_sum <- count(externals, "user_login")

wilcox.test(internals_sum$freq, externals_sum$freq)
cliff.delta(internals_sum$freq, externals_sum$freq)

