# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns
from scipy.stats import chi2_contingency
def main():

    # loading thr dataset and printing the intial 5 values
    health=pd.read_excel(r"D:\Swayam\technical_skills\internship projects\Heart disease\Heart Disease data\Heart Disease data.xlsx")
    print(health.head())
    sns.set_style('whitegrid')
    



    # Performing the exploratory data analysis(EDA)


    def exploratory_analysis():
        def age_group_bins():
            bins=[30,35,40,45,50,55,60,65,70,75,80]
            labels=('30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79')
            health['age_group'] = pd.cut(health['age'], bins=bins, labels=labels, right=False)
        age_group_bins()

        # Q.0 evaluating avg and maximum tresbps
        maximum_trestbps=health.groupby('age_group')['trestbps'].max()
        health['max_trestbps'] = health['age_group'].map(maximum_trestbps)

        pl.subplot(1,2,1)
        sns.barplot(x='age_group',y='trestbps',data=health,hue='sex',errorbar=None)   #gender wise resting blood pressure for each age-group
        pl.subplot(1,2,2)
        sns.barplot(x='age_group',y='max_trestbps',data=health,hue='sex',errorbar=None)
        pl.show()
        # Q.0.1 Evulating relationship between heart disease and trestbps
        pl.subplot(1,2,1)
        sns.barplot(x='age_group',y='trestbps',data=health,hue='target',errorbar=None)   #gender wise resting blood pressure for each age-group
        pl.subplot(1,2,2)
        sns.barplot(x='age_group',y='max_trestbps',data=health,hue='target',errorbar=None)
        pl.show()
        '''insight not any clear relationship between trestbps and heart diseases'''

        
        # Q.1 finding which chest pain type is most commmon via countplot
        label=["no Heart Disease",'Heart Disease']
        pl.subplot(1,2,1)
        ax=sns.countplot(x='cp',data=health,hue='age_group')
        for p in ax.patches:

            ax.annotate(format(p.get_height(), '.0f'), 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, 10), 
            textcoords = 'offset points')
        pl.xlabel('Chest Pain Type')
        pl.ylabel("Number of people")
        pl.subplot(1,2,2)
        ax=sns.countplot(x='cp',data=health,hue='target')
        for p in ax.patches:

            ax.annotate(format(p.get_height(), '.0f'), 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, 10), 
            textcoords = 'offset points')
        pl.xlabel('Chest Pain Type')
        pl.ylabel("Number of people")
        pl.show()

        # Q.2 find the correlation between cp and serum cholestrol
        sns.boxplot(x='cp', y='chol', data=health,hue='sex')    
        pl.title('Relationship between Chest Pain Type and Serum Cholesterol (Box Plot)')
        pl.xlabel('Chest Pain Type')
        pl.ylabel('Serum Cholesterol')
        pl.show()   
        

        '''As there is sufficiently large overlapping between he distributions solely cholestrol level cannot determine chest pain type'''

        # Q.3 Now studying the effect of cholestrol on heart rate while exercising and how many of them experienced irritation/chest_pain 
        pl.subplot(1,2,1)
        sns.scatterplot(y='chol',x='thalach',data=health,hue='exang')
        
        pl.subplot(1,2,2)
        sns.lineplot(y='chol',x='thalach',data=health,hue='exang')
        pl.show()

        '''They are both independent quantities'''

        # Q.4 Checking proportion of people with or without heart disease
        disease_proportion=health.groupby('target')['target'].value_counts()
        disease_labels=['Absence','Presence']
        ex=[0,0.05]
        pl.pie(disease_proportion,labels=disease_labels,explode=ex,autopct="%0.2f%%",shadow=True,radius=1,labeldistance=1.15,rotatelabels=True,startangle=90)    #Almost 50% of people having disease(HUGE NUMBER)

        pl.title('Prevalence Of Heart Disease')
        pl.legend()
        pl.show()

        # Q.4 checking distribution of thalach and serum colestrol
        pl.subplot(1,2,1)
        sns.kdeplot(x='chol',data=health,shade=True)
        pl.subplot(1,2,2)
        sns.kdeplot(x='thalach',data=health,shade=True)
        pl.show()

        # Q.5 People distrubution among age having or not having heart disease
        labels=['No heart disease','Heart Disease']
        ax = sns.countplot(x='age_group', data=health, hue='target')

        # Add labels to the axes
        pl.xlabel('Age')
        pl.ylabel('Number of people')

        # Add legend with custom labels
        pl.legend(labels=labels)

        # Add value labels to each bar
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, 10), 
            textcoords = 'offset points')

        pl.show()

        #Q.6 

        
    exploratory_analysis()
        

    def target_relation():
        # Q.1- solely having high cholestrol lead to a heart disease?
        sns.barplot(x='age_group',y='chol',hue='target',data=health,errorbar=None)  #cholestrol solely can't be only reason for target=1
        pl.show()
       
       # Q.2- Generally which type of chest pain is experienced by people having heart disease
        sns.countplot(x='cp',data=health,hue='target')
        pl.show()
        
        '''Insight- Type 1 and type 2 chest pain is most likely to be a symptom for heart disease'''

        # Q.3 studying the causal relationship between exercise induced agina, max heart rate and target value
        sns.boxplot(x='exang',y='thalach',data=health)   
        pl.show()
        #for exang=0 there are numerours outliers. Thus, analyze the factor more deeply. 
        sns.barplot(x='exang',y='thalach',data=health,hue='target')
        pl.show()
        '''Insight- The avg maximum heart rate is more for people having heart disease despite inducing pain or not '''
        # Q.4- Study whether fasting blood sugar and high cholestrol leads to heart disease
        danger_chol_fbs=health[(health.chol>=240) & (health.fbs==1)]  #dataframe of those having dangerous cholestrol level and positive fbs
        at_risk_chol_fbs= health[(health.chol<=239) & (health.chol>200) & (health.fbs==1)]   # dataframe of those having dangerous cholestrol level and positive fbs
        negative_fbs_dangerous_chol=health[(health.chol>=240) & (health.fbs==0)]
        negative_fbs_at_risk_chol=health[(health.chol<=239) & (health.chol>200) & (health.fbs==0)]
        dangerous_chol_level=health[health.chol>=240]
        at_risk_chol_level=health[(health.chol<240) & (health.chol>200)]

       
       # visulaing relationship between trestbps and heart disease for people having high cholestrol
        pl.subplot(1,2,1)
        sns.barplot(x='age_group',y='trestbps',data=dangerous_chol_level,hue='target',errorbar=None)   #gender wise resting blood pressure for each age-group
        pl.subplot(1,2,2)
        sns.barplot(x='age_group',y='max_trestbps',data=dangerous_chol_level,hue='target',errorbar=None)
        pl.show()

       # visualising for people having cholestrol level>240 (above danger level)
       
        pl.figure(figsize=(12, 8))

        pl.subplot(2, 2, 1)
        sns.countplot(x='target', data=danger_chol_fbs)
        pl.title('Dangerous Cholesterol Level with Positive Fasting Blood Sugar')

        pl.subplot(2, 2, 2)
        sns.countplot(x='target', data=negative_fbs_dangerous_chol)
        pl.title('Dangerous Cholesterol Level with Negative Fasting Blood Sugar')

        pl.subplot(2, 2, 3)
        sns.countplot(x='target', data=at_risk_chol_fbs)
        pl.title('Borderline Risk Cholesterol Level with Positive Fasting Blood Sugar')

        pl.subplot(2, 2, 4)
        sns.countplot(x='target', data=negative_fbs_at_risk_chol)
        pl.title('Borderline Risk Cholesterol Level with Negative Fasting Blood Sugar')

        #pl.tight_layout()
        pl.show()

      


        

        # statistical analysis

        #For people having cholestrol level above 240

        dangerous_chol_level=health[health.chol>=240]
        at_risk_chol_level=health[(health.chol<240) & (health.chol>200)]
        contingency_table = pd.crosstab(dangerous_chol_level['fbs'], dangerous_chol_level['target'])
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        # Display chi-squared test results
        print("Chi-squared statistic:", round(chi2,2))
        print("p-value:", round(p,2))
        print("Degrees of freedom:", dof)
        print('-------------------------------------------\n')

        #for people having cholestrol level at borderline risk
        contingency_table2=pd.crosstab(at_risk_chol_level['fbs'],at_risk_chol_level['target'])
        chi2,p,dof,expected=chi2_contingency(contingency_table2)
        print("Chi-squared statistic:", round(chi2,2))
        print("p-value:", round(p,2))
        print("Degrees of freedom:", dof)


       
     

        '''conclusion- as p value>0.05 and chi sqaured is less than crtitical value , it's cleat that the null hypothesis is fail to be rejected for both cholestrol levels'''
        # determining relationship between heart disease and trestbps for people having cholestrol above dangerous level and compoaring into two groups pf fbs +ve and -ve
        #relating the same two for people having dangerous level chol(subplot1) and people having fbs=1 too(subplot2)
        pl.subplot(2,2,1)
        sns.barplot(x='age_group',y='trestbps',data=dangerous_chol_level,hue='target')
        pl.title("People with dangerous chol")
        pl.subplot(2,2,2)
        sns.countplot(x='age_group',data=dangerous_chol_level,hue='target')
        pl.subplot(2,2,3)
        sns.barplot(x='age_group',y='trestbps',data=danger_chol_fbs,hue='target')
        pl.title('people with dangerous chol and +ve fbs')
        pl.subplot(2,2,4)
        sns.countplot(x='age_group',data=danger_chol_fbs,hue='target')
        pl.show()
         

        
        # Q.5 - Understanding impact of ECG on heart disease
        sns.countplot(x='restecg',data=health,hue='target') 
        pl.show()
        '''Insight- Type 1 restecg is more common in people having heart disease'''

        # Q.6 slope of ST depression and heart diseaase
        sns.countplot(x='slope',data=health,hue='target')
        pl.show()

        # fluroscopy
        sns.countplot(x='ca',data=health,hue='target')
        pl.show()
        # Q.7- which age group experience most of the heart disease with gender comparison. 
        positive_target=health[health.target==1]
        sns.countplot(x='age_group',data=positive_target,hue='sex')
        pl.show()

        # Q.8 analysing old peak with heart disease
        positive_oldpeak=health[health.oldpeak>0]
        zero_oldpeak=health[health.oldpeak==0]
        pl.subplot(2,2,1)
        sns.countplot(x='target',data=positive_oldpeak)
        pl.subplot(2,2,2)
        sns.countplot(x='target',data=zero_oldpeak)
        pl.subplot(2,2,3)
        sns.boxplot(x='target',y='oldpeak',data=health)
        pl.show()


        # Q.9 correlation between old peak, slope of ST segment & oldpeak,ca and target 
        pl.subplot(2,2,1)
        sns.boxplot(x='slope',y='oldpeak',data=health,hue='target')
        pl.subplot(2,2,2)
        sns.countplot(x='slope',data=health,hue='target')
        
        pl.subplot(2,2,3)
        sns.boxplot(x='ca',y='oldpeak',data=health,hue='target')
        pl.subplot(2,2,4)
        sns.countplot(x='ca',data=health,hue='target')
        pl.show()

        #correlation  bewteen CAD and slope
        sns.countplot(x='ca',data=health,hue='slope')
        pl.show()

        contingency_table3 = pd.crosstab(health['ca'], health['slope'])

        # Perform chi-square test for independence
        chi2, p, dof, expected = chi2_contingency(contingency_table3)

        print('------------------------------')
        print(contingency_table3)

        print("Chi-square statistic:", chi2)
        print("p-value:", p)
        print("Degrees of freedom:", dof)
        print('expected freq:',expected)

        '''Thus Null hypothesis is rejected and thus, there is a relationship between CAD and slope type'''

        #Q.10 relation between target thar
        sns.boxplot(x='thal',y='thalach',data=health)
        pl.show()

        #correlation between thal and exang
        contingency_table4=pd.crosstab(health['thal'],health['exang'])
        chi2,p,dof,expectd=chi2_contingency(contingency_table4)
        print('----------------------------')
        print(contingency_table4)
        print("chisquared: ",chi2)
        print('p value: ',p)
        print("dof: ",dof)
        print('expected freq.: ',expectd)

        # Q.11 correlationship type between thal,exang & ca & exang
        pl.subplot(1,2,1)
        sns.countplot(x='thal',data=health,hue='exang')
        pl.subplot(1,2,2)
        sns.countplot(x='ca',data=health,hue='exang')
        pl.show()

        '''Insight- no appranet relationship between exang and ca type(potentially to heart disease)'''
        # analysing exang and heart disease
        sns.countplot(x='exang',data=health,hue='target')
        pl.show()
    
        # Determining the relationship between exang and heart disease
        label=['no Heart Disease','Heart Disease']
        ax=sns.countplot(x='exang',data=health,hue='target')
        for p in ax.patches: 
            ax.annotate(format(p.get_height(), '.0f'), 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, 10), 
            textcoords = 'offset points',
            fontsize=8)
        pl.xlabel('Excercise Induced Angina')
        pl.ylabel('Number of people')
        pl.legend(labels=label)
        pl.show()




    target_relation()
    
        
   
main()