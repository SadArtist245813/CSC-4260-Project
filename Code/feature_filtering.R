df <- read.csv(file.choose())

# All Categories
all <- c("aca_anx", "gad", "anx", "dx_anx", "aca_dep", "phq9", "dep_", "phq2", "dx_dep", "aca_eat", "thin_good", "sde", "ed_", "wcs", "body", "weight_", "weigh_", "pfdrug", "scoff", "binge", "purge", "diet", "eat", "dx_ea", "aca_add", "dx_neurodev", "disab", "ADHD", "aca_substance", "sub", "alc", "drug", "audit", "thc", "nicotine", "pfdrug", "naloxene", "overdose", "risk_alc", "risk_cig", "risk_mar", "risk_presc", "risk_vape", "care_peer_alc", "est_peer_alc", "est_peer_cig", "est_peer_mar", "est_peer_vape", "est_peer_rxdrug", "opioid", "aca_phys_health", "health", "dx_chronic", "exerc", "TBI", "eatprac", "diet_veg", "sex_partner", "birthcontrol", "nobc", "STI", "preg", "aca_phys_assault", "abuse", "stalk", "IPV", "HITS", "aca_sex_assault", "sa_", "revoke")

# Anxiety
anxiety <- c("aca_anx", "gad", "anx", "dx_anx")

# Depression
depression <- c("aca_dep", "phq9", "dep_", "phq2", "dx_dep")

# Eating
eating <- c("aca_eat", "thin_good", "sde", "ed_", "wcs", "body", "weight_", "weigh_", "pfdrug", "scoff", "binge", "purge", "diet", "eat", "dx_ea")

# Disorders
disorders <- c("aca_add", "dx_neurodev", "disab", "ADHD")

# Substance Abuse
substance <- c("aca_substance", "sub", "alc", "drug", "audit", "thc", "nicotine", "pfdrug", "naloxene", "overdose", "risk_alc", "risk_cig", "risk_mar", "risk_presc", "risk_vape", "care_peer_alc", "est_peer_alc", "est_peer_cig", "est_peer_mar", "est_peer_vape", "est_peer_rxdrug", "opioid")

# Physical Health
physical <- c("aca_phys_health", "health", "dx_chronic", "exerc", "TBI", "eatprac", "diet_veg", "sex_partner", "birthcontrol", "nobc", "STI", "preg")

# Physical Assault
p_assault <- c("aca_phys_assault", "abuse", "stalk", "IPV", "HITS")

# Sexual Assault
s_assault <- c("aca_sex_assault", "sa_", "revoke")

df_filtered_anxiety <- df[, Reduce(`|`, lapply(anxiety, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_depression <- df[, Reduce(`|`, lapply(depression, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_eating <- df[, Reduce(`|`, lapply(eating, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_disorders <- df[, Reduce(`|`, lapply(disorders, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_substance <- df[, Reduce(`|`, lapply(substance, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_physical <- df[, Reduce(`|`, lapply(physical, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_p_assault <- df[, Reduce(`|`, lapply(p_assault, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_s_assault <- df[, Reduce(`|`, lapply(s_assault, function(p) {
  startsWith(names(df), p)
}))]

df_filtered_all <- df[, Reduce(`|`, lapply(all, function(p) {
  startsWith(names(df), p)
}))]


print(colnames(df_filtered_anxiety))

print(colnames(df_filtered_depression))

print(colnames(df_filtered_eating))

print(colnames(df_filtered_disorders))

print(colnames(df_filtered_substance))

print(colnames(df_filtered_physical))

print(colnames(df_filtered_p_assault))

print(colnames(df_filtered_s_assault))

write.csv(df_filtered_all, file = "output.csv")