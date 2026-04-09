
###  This file is intended to reduce dimensionality of the data to a few features relating to substance abuse

library(dplyr)
df <- read.csv(file.choose())

type_cols <- c("nicotine_type_cig",
               "nicotine_type_vape",
               "nicotine_type_chew",
               "nicotine_type_zyn",
               "nicotine_type_cess")

# Derive a composite variable for any nicotine use
# This variable indicates if a participant uses any nicotine product.
df$any_nicotine_use <- ifelse(df$nicotine_type_none == 1, 0,
                              ifelse(apply(df[type_cols], 1, function(x) all(is.na(x))), NA,
                                     ifelse(rowSums(df[type_cols], na.rm = TRUE) > 0, 1, 0)))

# Recode frequency variables to a numerical scale for easier scoring
# Higher numbers will indicate higher frequency/risk.

recode_freq <- function(x) {
  recode(x,
         '1' = 7, '2' = 6, '3' = 5, '4' = 4,
         '5' = 3, '6' = 2, '7' = 1,
         .default = NA_real_)
}

df$nicotine_freq_cig_score  <- recode_freq(df$nicotine_freq_cig)
df$nicotine_freq_vape_score <- recode_freq(df$nicotine_freq_vape)
df$nicotine_freq_chew_score <- recode_freq(df$nicotine_freq_chew)
df$nicotine_freq_zyn_score  <- recode_freq(df$nicotine_freq_zyn)
df$nicotine_freq_cess_score <- recode_freq(df$nicotine_freq_cess)


# Create a composite nicotine frequency score
df$nicotine_overall_freq_score <- pmax(df$nicotine_freq_cig_score,
                                       df$nicotine_freq_vape_score,
                                       df$nicotine_freq_chew_score,
                                       df$nicotine_freq_zyn_score,
                                       df$nicotine_freq_cess_score,
                                       na.rm = TRUE)

df$nicotine_overall_freq_score[is.infinite(df$nicotine_overall_freq_score)] <- NA

# If 'nicotine_type_none' was selected, overall frequency should be 0.
df$nicotine_overall_freq_score <- ifelse(df$nicotine_type_none == 1, 0,
                                         ifelse(is.infinite(df$nicotine_overall_freq_score), NA, df$nicotine_overall_freq_score))

# Calculate a total nicotine use score (similar to AUDIT_score)

# Convert while preserving NA
df[type_cols] <- lapply(df[type_cols], function(x) {
  # Keep NA as NA, convert 1 to 1, everything else to 0
  ifelse(is.na(x), NA, ifelse(x == 1, 1, 0))
})

df$nicotine_score <- rowSums(df[type_cols], na.rm = TRUE) + 
  ifelse(is.na(df$nicotine_overall_freq_score), 0, df$nicotine_overall_freq_score)

all_na <- apply(df[type_cols], 1, function(x) all(is.na(x)))
df$nicotine_score[all_na] <- NA

# Define a nicotine risk variable (similar to AUDIT_risk)
# With current scoring: min = 0 (no use), max = 5 (all types used) + 7 (max freq) = 12.

df$nicotine_risk <- ifelse(is.na(df$nicotine_score), NA,
                           ifelse(df$nicotine_score > 5 & df$nicotine_score <= 12, 1, 0))

# Reverse sub_knowwher_rev (6 is most aware of where to find help)
df$sub_knowwhere_rev <- 7 - df$sub_knowwher

# Make sub_effort binary
df$sub_effort_binary <- ifelse(df$sub_effort == 1, 1, 0)

# Combine aca_substance 1-7 into a score
df$aca_substance_impact_count <- rowSums(cbind(df$aca_substance_1,
                                               df$aca_substance_2,
                                               df$aca_substance_3,
                                               df$aca_substance_4,
                                               df$aca_substance_5,
                                               df$aca_substance_6,
                                               df$aca_substance_7), na.rm = TRUE)

# Get an overall grade Score: participants can select up to two grade scores which they most commonly reiceve, if they select 2, take the average
# (F = 0, A = 4)

df <- df %>%
  mutate(
    grade_composite = case_when(
      gr_none == 1 ~ NA_real_,
      gr_dk == 1 ~ NA_real_,
      TRUE ~ {
        vals <- cbind(
          ifelse(gr_A == 1, 4, NA),
          ifelse(gr_B == 1, 3, NA),
          ifelse(gr_C == 1, 2, NA),
          ifelse(gr_D == 1, 1, NA),
          ifelse(gr_F == 1, 0, NA)
        )
        res <- rowMeans(vals, na.rm = TRUE)
        ifelse(is.nan(res), NA, res)
      }
    )
  )


cols_to_keep <- c("nicotine_risk", "nicotine_score", "audit_risk", "audit_score", "drug_mar", "aca_substance_impact_count", "sub_effort_binary", "sub_knowwhere_rev", "grade_composite")

filtered_df <- df[, cols_to_keep]

table(df$any_nicotine_use)
table(df$nicotine_score)
summary(df$nicotine_score)

write.csv(filtered_df, file = file.choose())
