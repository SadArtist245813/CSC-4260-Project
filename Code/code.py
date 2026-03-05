import os
import rpy2.robjects as robjects

# Open R
os.environ['RPY2_CFFI_MODE'] = 'ABI'
os.environ['R_HOME'] = r'C:\Program Files\R\R-4.5.1'   # ← update to your R version
os.environ['PATH'] = r'C:\Program Files\R\R-4.5.1\bin\x64;' + os.environ.get('PATH', '')

# Run Script
r_script_path = "feature_filtering.R"
r_source = robjects.r['source']
r_source(r_script_path)
print("✅ R script sourced via rpy2!")