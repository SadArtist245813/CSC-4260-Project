import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Load Data
print("Loading HMS 2024-2025 dataset...")
try:
    df = pd.read_csv(r"HMS_2024-2025_PUBLIC_instchars.csv")
except FileNotFoundError:
    print("Error: HMS_2024-2025_PUBLIC_instchars.csv not found.")
    sys.exit(1)

# Feature Engineering
diener_cols = [col for col in df.columns if col.startswith('diener')]
if diener_cols:
    df['flourish'] = df[diener_cols].sum(axis=1)
else:
    df['flourish'] = 0

phq_cols = [col for col in df.columns if col.startswith('phq9_')]
if phq_cols:
    df['phq9_total'] = df[phq_cols].sum(axis=1)
else:
    df['phq9_total'] = 0

gad_cols = [col for col in df.columns if col.startswith('gad7_')]
if gad_cols:
    df['gad7_total'] = df[gad_cols].sum(axis=1)
else:
    df['gad7_total'] = 0

if 'sleep_wknight' in df.columns and 'sleep_wkend' in df.columns:
    df['avg_sleep'] = (df['sleep_wknight'].fillna(0) + df['sleep_wkend'].fillna(0)) / 2
else:
    df['avg_sleep'] = 0

print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")

# Plot Functions
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def plot_age():
    sns.histplot(df['age'].dropna(), kde=True, bins=30, color='skyblue')
    plt.title('1. Age Distribution of Respondents')
    plt.xlabel('Age'); plt.ylabel('Count')
    plt.savefig('plot_01_age.png', bbox_inches='tight'); plt.close()

def plot_gender():
    gender_cols = [col for col in ['gender_male','gender_female','gender_queer','gender_nonbin','gender_trans'] if col in df.columns]
    if not gender_cols:
        print("Gender columns not found in dataset")
        return
    gender_counts = df[gender_cols].sum()
    sns.barplot(x=gender_counts.index, y=gender_counts.values, palette='Blues')
    plt.title('2. Gender Identity (multiple selections allowed)')
    plt.xticks(rotation=45); plt.ylabel('Count')
    plt.savefig('plot_02_gender.png', bbox_inches='tight'); plt.close()

def plot_race_white():
    if 'race_white' not in df.columns:
        print("race_white column not found in dataset")
        return
    df['is_white'] = df['race_white'].fillna(0)
    sns.countplot(x='is_white', data=df, palette='Set2')
    plt.title('3. Proportion Identifying as White')
    plt.xticks([0,1], ['Non-White', 'White'])
    plt.savefig('plot_03_race_white.png', bbox_inches='tight'); plt.close()

def plot_year_school():
    if 'yr_sch' not in df.columns:
        print("yr_sch column not found in dataset")
        return
    sns.countplot(x='yr_sch', data=df, palette='viridis')
    plt.title('4. Year in School')
    plt.xlabel('Year')
    plt.savefig('plot_04_year_school.png', bbox_inches='tight'); plt.close()

def plot_top_fields():
    field_cols = [col for col in df.columns if col.startswith('field_')]
    field_sums = df[field_cols].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=field_sums.values, y=field_sums.index, palette='mako')
    plt.title('5. Top 10 Fields of Study')
    plt.savefig('plot_05_fields.png', bbox_inches='tight'); plt.close()

def plot_aca_impa():
    if 'aca_impa' not in df.columns:
        print("aca_impa column not found in dataset")
        return
    sns.histplot(df['aca_impa'].dropna(), bins=10, kde=True)
    plt.title('7. Academic Impairment Score')
    plt.savefig('plot_07_aca_impa.png', bbox_inches='tight'); plt.close()

def plot_flourish():
    sns.histplot(df['flourish'].dropna(), kde=True, bins=20, color='teal')
    plt.title('8. Flourishing / Positive Mental Health Score')
    plt.savefig('plot_08_flourish.png', bbox_inches='tight'); plt.close()

def plot_phq9():
    sns.histplot(df['phq9_total'].dropna(), kde=True, bins=15)
    plt.title('9. PHQ-9 Total Depression Score')
    plt.savefig('plot_09_phq9.png', bbox_inches='tight'); plt.close()

def plot_gad7():
    sns.histplot(df['gad7_total'].dropna(), kde=True, bins=15)
    plt.title('10. GAD-7 Total Anxiety Score')
    plt.savefig('plot_10_gad7.png', bbox_inches='tight'); plt.close()

def plot_self_harm():
    if 'sib_any' not in df.columns:
        print("sib_any column not found in dataset")
        return
    sns.countplot(x='sib_any', data=df, palette='Reds')
    plt.title('11. Any Self-Harm Behavior')
    plt.savefig('plot_11_self_harm.png', bbox_inches='tight'); plt.close()

def plot_alc_any():
    if 'alc_any' not in df.columns:
        print("alc_any column not found in dataset")
        return
    sns.countplot(x='alc_any', data=df, palette='Purples')
    plt.title('12. Any Alcohol Use in Past Year')
    plt.xticks([0,1], ['No', 'Yes'])
    plt.savefig('plot_12_alc_any.png', bbox_inches='tight'); plt.close()

def plot_binge():
    if 'binge_fr' not in df.columns:
        print("binge_fr column not found in dataset")
        return
    sns.histplot(df['binge_fr'].dropna(), kde=True)
    plt.title('13. Binge Drinking Frequency')
    plt.savefig('plot_13_binge.png', bbox_inches='tight'); plt.close()

def plot_sleep():
    sns.histplot(df['avg_sleep'].dropna(), kde=True)
    plt.title('14. Average Hours of Sleep')
    plt.savefig('plot_14_sleep.png', bbox_inches='tight'); plt.close()

def plot_exercise():
    if 'exerc' not in df.columns:
        print("exerc column not found in dataset")
        return
    sns.histplot(df['exerc'].dropna(), kde=True)
    plt.title('15. Exercise Frequency / Intensity')
    plt.savefig('plot_15_exercise.png', bbox_inches='tight'); plt.close()

def plot_worry():
    worry_cols = [col for col in ['food_worry', 'housing_worry'] if col in df.columns]
    if not worry_cols:
        print("Worry columns not found in dataset")
        return
    worry_means = df[worry_cols].mean()
    sns.barplot(x=worry_means.index, y=worry_means.values)
    plt.title('16. Mean Worry about Food & Housing')
    plt.savefig('plot_16_worry.png', bbox_inches='tight'); plt.close()

def plot_therapy():
    therapy_cols = [col for col in ['ther_any', 'meds_any'] if col in df.columns]
    if not therapy_cols:
        print("Therapy columns not found in dataset")
        return
    therapy = df[therapy_cols].mean()
    sns.barplot(x=therapy.index, y=therapy.values, palette='cool')
    plt.title('17. Lifetime Therapy or Medication Use')
    plt.savefig('plot_17_therapy.png', bbox_inches='tight'); plt.close()

def plot_abuse_and_grades():
    # Combined visualization: responses to `abuse_life` and grades `gr_A`-`gr_F`
    grade_cols = [c for c in ['gr_A', 'gr_B', 'gr_C', 'gr_D', 'gr_F'] if c in df.columns]

    if 'abuse_life' not in df.columns:
        print("abuse_life column not found in dataset")
        return
    if not grade_cols:
        print("Grade columns not found in dataset")
        return

    grade_map = {
        'gr_A': 'A',
        'gr_B': 'B',
        'gr_C': 'C',
        'gr_D': 'D',
        'gr_F': 'F'
    }
    grades = df[grade_cols].fillna(0).astype(float)

    # Determine the grade selected per person, if any.
    def pick_grade(row):
        positives = [grade_map[col] for col in grade_cols if row[col] == 1]
        if len(positives) == 1:
            return positives[0]
        if len(positives) > 1:
            return '+'.join(positives)
        return 'Unknown'

    person_grade = grades.apply(pick_grade, axis=1)
    data = df[['abuse_life']].copy()
    data['grade_selected'] = person_grade
    data = data[data['grade_selected'] != 'Unknown']
 
    sns.countplot(
        x='grade_selected',
        hue=data['abuse_life'].astype(str),
        data=data,
        palette='Oranges'
    )
    plt.title('Grade choice by abuse_life response')
    plt.xlabel('Grade selected')
    plt.ylabel('Count of respondents')
    plt.legend(title='abuse_life')
    plt.savefig('plot_18_abuse_grades.png', bbox_inches='tight')
    plt.close()
    
    
def plot_dx_any_and_grades():
    # Combined visualization: responses to `dx_any` and grades `gr_A`-`gr_F`
    grade_cols = [c for c in ['gr_A', 'gr_B', 'gr_C', 'gr_D', 'gr_F'] if c in df.columns]

    if 'dx_any' not in df.columns:
        print("dx_any column not found in dataset")
        return
    if not grade_cols:
        print("Grade columns not found in dataset")
        return

    grade_map = {
        'gr_A': 'A',
        'gr_B': 'B',
        'gr_C': 'C',
        'gr_D': 'D',
        'gr_F': 'F'
    }
    grades = df[grade_cols].fillna(0).astype(float)

    # Determine the grade selected per person, if any.
    def pick_grade(row):
        positives = [grade_map[col] for col in grade_cols if row[col] == 1]
        if len(positives) == 1:
            return positives[0]
        if len(positives) > 1:
            return '+'.join(positives)
        return 'Unknown'

    person_grade = grades.apply(pick_grade, axis=1)
    data = df[['dx_any']].copy()
    data['grade_selected'] = person_grade
    data = data[data['grade_selected'] != 'Unknown']
 
    sns.countplot(
        x='grade_selected',
        hue=data['dx_any'].astype(str),
        data=data,
        palette='Oranges'
    )
    plt.title('Grade choice by dx_any response')
    plt.xlabel('Grade selected')
    plt.ylabel('Count of respondents')
    plt.legend(title='dx_any')
    plt.savefig('plot_18_dx_any_grades.png', bbox_inches='tight')
    plt.close()

# Interactive Menu
print("🎯 HMS Interactive Plot Generator")
print("=" * 60)
print("Available sections:")
print("   1. Demographics")
print("   2. Academic Performance")
print("   3. Mental Health")
print("   4. Lifestyle & Health Factors")
print("   all = generate everything")
print("   quit = exit")
print("=" * 60)

while True:
    section_input = input("\nEnter section name or number (or 'all' or 'quit'): ").strip().lower()
    
    if section_input == 'quit':
        print("Exiting. All saved plots are in the current folder.")
        break
    
    if section_input == 'all':
        print("Generating ALL 18 plots...")
        plot_age(); plot_gender(); plot_race_white(); plot_year_school(); plot_top_fields()
        plot_aca_impa()
        plot_flourish(); plot_phq9(); plot_gad7(); plot_self_harm()
        plot_alc_any(); plot_binge(); plot_sleep(); plot_exercise(); plot_worry(); plot_therapy(); plot_abuse_and_grades(); plot_dx_any_and_grades()
        print("All 18 plots saved!")
        continue
    
    # Map user input to section
    section_map = {
        '1': 'demographics', 'demographics': 'demographics',
        '2': 'academic', 'academic performance': 'academic', 'academic': 'academic',
        '3': 'mental', 'mental health': 'mental', 'mental': 'mental',
        '4': 'lifestyle', 'lifestyle & health factors': 'lifestyle', 'lifestyle': 'lifestyle'
    }
    
    section = section_map.get(section_input)
    if not section:
        print("❌ Invalid section. Please try again.")
        continue
    
    # Show available plots for chosen section
    if section == 'demographics':
        print("\nDemographics plots available:")
        print("   1. Age Distribution")
        print("   2. Gender Identity")
        print("   3. Race – White")
        print("   4. Year in School")
        print("   5. Top 10 Fields of Study")
    elif section == 'academic':
        print("\nAcademic Performance plots available:")
        print("   6. Academic Impairment Score")
    elif section == 'mental':
        print("\nMental Health plots available:")
        print("   7. Flourishing Score")
        print("   8. PHQ-9 Depression")
        print("   9. GAD-7 Anxiety")
        print("  10. Any Self-Harm")
        print("  11. Grade choice by abuse_life")
        print("  12. Grade choice by dx_any")
    elif section == 'lifestyle':
        print("\nLifestyle & Health plots available:")
        print("  12. Any Alcohol Use")
        print("  13. Binge Drinking")
        print("  14. Average Sleep")
        print("  15. Exercise")
        print("  16. Food & Housing Worry")
        print("  17. Therapy/Medication Use")
    
    # Get user choice of plots
    choice = input("\nEnter plot numbers (comma separated) or 'all' for this section: ").strip().lower()
    
    if choice == 'all':
        if section == 'demographics':
            plot_age(); plot_gender(); plot_race_white(); plot_year_school(); plot_top_fields()
        elif section == 'academic':
            plot_aca_impa()
        elif section == 'mental':
            plot_flourish(); plot_phq9(); plot_gad7(); plot_self_harm(); plot_abuse_and_grades(); plot_dx_any_and_grades()
        elif section == 'lifestyle':
            plot_alc_any(); plot_binge(); plot_sleep(); plot_exercise(); plot_worry(); plot_therapy()
        print(f"All plots for {section} saved!")
        continue
    
    # Parse numbers
    try:
        numbers = [int(x.strip()) for x in choice.split(',')]
        for n in numbers:
            if n == 1: plot_age()
            elif n == 2: plot_gender()
            elif n == 3: plot_race_white()
            elif n == 4: plot_year_school()
            elif n == 5: plot_top_fields()
            elif n == 6: plot_aca_impa()
            elif n == 7: plot_flourish()
            elif n == 8: plot_phq9()
            elif n == 9: plot_gad7()
            elif n == 10: plot_self_harm()
            elif n == 11: plot_alc_any()
            elif n == 12: plot_binge()
            elif n == 13: plot_sleep()
            elif n == 14: plot_exercise()
            elif n == 15: plot_worry()
            elif n == 16: plot_therapy()
            elif n == 17: plot_abuse_and_grades()
            elif n == 18: plot_dx_any_and_grades()
            else: print(f"Plot {n} not found")
        print(f"Selected plots for {section} have been saved as PNG files!")
    except Exception as e:
        print(f"Invalid input. Use numbers separated by commas. {e}")

    