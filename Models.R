file = "Workspace/cmu Project/OLI_PHYC_Project/code/oli_phy_fa/data/merged_step_read_file_readkc-283.csv"

memory.limit(10000)
library("boot", lib.loc="/usr/local/lib/R/3.5/site-library")
ds = read.csv(file, header = TRUE, quote="\"", dec=".", fill = TRUE, comment.char="",sep=",")

attach(ds) # Allows reference to the variables in ds without using ds: e.g., ds$Anon.Student.Id

summary(ds) # Inspect the contents of the file
L = length(correct) # Number of "rows" (values) in (this "column" variable from) ds
abc = vector(mode="numeric", length=L) # Create a new variable (default values are 0)
abc = ifelse(correct == 'correct',1,0)  # Change rows where First.Attempt is "correct" to 1.

ds["Success"] = abc
xyz = vector(mode="numeric", Length = L)
xyz = kc_step_opportunity + kc_read_opportunity
ds['kc_total_opportunity'] = xyz
m00 = glm(Success~student_id + kc + kc :kc_total_opportunity  , family=binomial(), data=ds)
m0 = glm(Success~student_id + kc + kc :kc_step_opportunity    , family=binomial(), data=ds)
m01 = glm(Success~student_id + kc + kc :kc_step_opportunity + kc:kc_read_opportunity   , family=binomial(), data=ds)
m02 = glm(Success~student_id + kc + kc :kc_step_opportunity + kc:reading_speed   , family=binomial(), data=ds)
m1 = glm(Success~student_id + kc + kc :kc_prev_incorrect_step + kc:kc_prev_correct_step   , family=binomial(), data=ds)
m2 = glm(Success~student_id + kc + kc :kc_prev_incorrect_step + kc:kc_prev_correct_step +kc:kc_read_opportunity, family=binomial(), data=ds)
m3 = glm(Success~student_id + kc + kc :kc_prev_incorrect_step + kc:kc_prev_correct_step + kc:reading_speed, family=binomial(), data=ds)

summary(m00)$aic+length(coef(m00))*(log(L)-2)
summary(m0)$aic+length(coef(m0))*(log(L)-2)
summary(m01)$aic+length(coef(m01))*(log(L)-2)
summary(m02)$aic+length(coef(m02))*(log(L)-2)
summary(m1)$aic+length(coef(m1))*(log(L)-2)
summary(m2)$aic+length(coef(m2))*(log(L)-2)
summary(m3)$aic+length(coef(m3))*(log(L)-2)



model.names <- c("1 Gender00","1 Gender1","1 Gender2","1 Gender3","1 Gender", "2 Dept", "3 Gender + Dept")
summ.table <- do.call(rbind, lapply(list(m00,m0,m01,m02,m1, m2, m3), broom::glance))
table.cols <- c("df.residual", "deviance", "AIC")
reported.table <- summ.table[table.cols]
names(reported.table) <- c("Resid. Df", "Resid. Dev", "AIC")

reported.table[['dAIC']] <-  with(reported.table, AIC - min(AIC))
reported.table[['weight']] <- with(reported.table, exp(- 0.5 * dAIC) / sum(exp(- 0.5 * dAIC)))
reported.table$AIC <- NULL
reported.table$weight <- round(reported.table$weight, 2)
reported.table$dAIC <- round(reported.table$dAIC, 1)
row.names(reported.table) <- model.names
reported.table
reported.table2 <- bbmle::AICtab(m00,m0,m01,m02,m1, m2, m3, weights = TRUE, sort = FALSE, mnames = model.names)
reported.table2[["Resid. Dev"]]  <- summ.table[["deviance"]] # get the deviance from broom'd table
reported.table2


model.names <- c("1 Gender", "2 Dept", "3 Gender + Dept")
summ.table <- do.call(rbind, lapply(list(m1, m2, m3), broom::glance))
table.cols <- c("df.residual", "deviance", "AIC")
reported.table <- summ.table[table.cols]
names(reported.table) <- c("Resid. Df", "Resid. Dev", "AIC")

reported.table[['dAIC']] <-  with(reported.table, AIC - min(AIC))
reported.table[['weight']] <- with(reported.table, exp(- 0.5 * dAIC) / sum(exp(- 0.5 * dAIC)))
reported.table$AIC <- NULL
reported.table$weight <- round(reported.table$weight, 2)
reported.table$dAIC <- round(reported.table$dAIC, 1)
row.names(reported.table) <- model.names
reported.table
reported.table2 <- bbmle::AICtab(m1, m2, m3, weights = TRUE, sort = FALSE, mnames = model.names)
reported.table2[["Resid. Dev"]]  <- summ.table[["deviance"]] # get the deviance from broom'd table
reported.table2


model.names <- c("1 Gender100","1 Gender","1 Gender2","1 Gender3")
summ.table <- do.call(rbind, lapply(list(m00,m0,m01,m02), broom::glance))
table.cols <- c("df.residual", "deviance", "AIC")
reported.table <- summ.table[table.cols]
names(reported.table) <- c("Resid. Df", "Resid. Dev", "AIC")

reported.table[['dAIC']] <-  with(reported.table, AIC - min(AIC))
reported.table[['weight']] <- with(reported.table, exp(- 0.5 * dAIC) / sum(exp(- 0.5 * dAIC)))
reported.table$AIC <- NULL
reported.table$weight <- round(reported.table$weight, 2)
reported.table$dAIC <- round(reported.table$dAIC, 1)
row.names(reported.table) <- model.names
reported.table
reported.table2 <- bbmle::AICtab(m00,m0,m01,m02, weights = TRUE, sort = FALSE, mnames = model.names)
reported.table2[["Resid. Dev"]]  <- summ.table[["deviance"]] # get the deviance from broom'd table
reported.table2

cost <- function(r, pi = 0) mean(abs(r-pi) > 0.5)
(cv.11.err.m00 <- cv.glm(ds, m00, cost, K = 10))

(cv.11.err.m0 <- cv.glm(ds, m0, cost, K = 10))
(cv.11.err.m01 <- cv.glm(ds, m01, cost, K = 10))
(cv.11.err.m02 <- cv.glm(ds, m02, cost, K = 10))

(cv.11.err.m1 <- cv.glm(ds, m1, cost, K = 10))
(cv.11.err.m2 <- cv.glm(ds, m2, cost, K = 10))
(cv.11.err.m3 <- cv.glm(ds, m3, cost, K = 10))
cv.11.err.m0$delta
cv.11.err.m01$delta
cv.11.err.m02$delta
cv.11.err.m1$delta
cv.11.err.m2$delta
cv.11.err.m3$delta



