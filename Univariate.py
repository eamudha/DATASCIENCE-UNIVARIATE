class UNIVARIATE():
    def QuanQual(dataset):
        Qual=[]
        Quan=[]
        for ColumnName in dataset.columns:
            #print (ColumnName)
            if (dataset[ColumnName].dtypes=="O"):
                #print ("Qual")
                Qual.append(ColumnName)
            else:
                #print ("Quan")
                Quan.append(ColumnName)
        return Quan,Qual

    def U_Variate(dataset, Quan):
        Descriptive=pd.DataFrame(index=["Mean","Median","Mode","Min","Max","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR","1.5IQR","Lesser","Greater", "Kurtosis", 
                                "Skewness","Variance","Standard_Deviation"],columns=Quan)
        for ColumnName in Quan:
            Descriptive[ColumnName]["Mean"]=dataset[ColumnName].mean()
            Descriptive[ColumnName]["Median"]=dataset[ColumnName].median()
            Descriptive[ColumnName]["Mode"]=dataset[ColumnName].mode()[0]
            Descriptive[ColumnName]["Min"]=dataset[ColumnName].min()
            Descriptive[ColumnName]["Max"]=dataset[ColumnName].max()
            Descriptive[ColumnName]["Q1:25%"]=dataset.describe()[ColumnName]["25%"]
            Descriptive[ColumnName]["Q2:50%"]=dataset.describe()[ColumnName]["50%"]
            Descriptive[ColumnName]["Q3:75%"]=dataset.describe()[ColumnName]["75%"]
            Descriptive[ColumnName]["Q4:100%"]=dataset.describe()[ColumnName]["max"]
            Descriptive[ColumnName]["IQR"]=Descriptive[ColumnName]["Q3:75%"]-Descriptive[ColumnName]["Q1:25%"]
            Descriptive[ColumnName]["1.5IQR"]=1.5*Descriptive[ColumnName]["IQR"]
            Descriptive[ColumnName]["Lesser"]=Descriptive[ColumnName]["Q1:25%"]-Descriptive[ColumnName]["1.5IQR"]
            Descriptive[ColumnName]["Greater"]=Descriptive[ColumnName]["Q3:75%"]+Descriptive[ColumnName]["1.5IQR"]
            Descriptive[ColumnName]["Kurtosis"]=dataset[ColumnName].kurtosis()
            Descriptive[ColumnName]["Skewness"]=dataset[ColumnName].skew()
            Descriptive[ColumnName]["Variance"]=dataset[ColumnName].var()
            Descriptive[ColumnName]["Standard_Deviation"]=dataset[ColumnName].std()
        return Descriptive
        
    def Finding_outliers(Descriptive, Quan):
        Lesser = []
        Greater = []
        for ColumnName in Quan:
            if Descriptive[ColumnName]["Min"] < Descriptive[ColumnName]["Lesser"]:
                Lesser.append(ColumnName)
            if Descriptive[ColumnName]["Max"] > Descriptive[ColumnName]["Greater"]:
                Greater.append(ColumnName)
        return Lesser, Greater
        
    def Handle_outliers(dataset, Descriptive, Quan):
        Lesser, Greater = Finding_outliers(Descriptive, Quan)
        for ColumnName in Lesser:
            dataset.loc[dataset[ColumnName] < Descriptive[ColumnName]["Lesser"], ColumnName] = Descriptive[ColumnName]["Lesser"]
        for ColumnName in Greater:
            dataset.loc[dataset[ColumnName] > Descriptive[ColumnName]["Greater"], ColumnName] = Descriptive[ColumnName]["Greater"]
        return dataset
        
    def Frequency_Table(ColumnName, dataset):
        Frequency_Table=pd.DataFrame(columns=["Unique_Values", "Frequency", "Relative_Frequency", "Cum_Sum"])
        Frequency_Table["Unique_Values"]=dataset[ColumnName].value_counts().index
        Frequency_Table["Frequency"]=dataset[ColumnName].value_counts().values
        total_count = len(dataset[ColumnName])
        Frequency_Table["Relative_Frequency"]=Frequency_Table["Frequency"]/total_count
        Frequency_Table["Cum_Sum"]=Frequency_Table["Relative_Frequency"].cumsum()
        return Frequency_Table
    
    def get_pdf_probability(dataset,startrange,endrange):
        from matplotlib import pyplot
        from scipy.stats import norm
        import seaborn as sns
        ax = sns.distplot(dataset,kde=True,kde_kws={'color':'blue'},color='Green')
        pyplot.axvline(startrange,color='Red')
        pyplot.axvline(endrange,color='Red')
        # generate a sample
        sample = dataset
        # calculate parameters
        sample_mean =sample.mean()
        sample_std = sample.std()
        print('Mean=%.3f, Standard Deviation=%.3f' % (sample_mean, sample_std))
        # define the distribution
        dist = norm(sample_mean, sample_std)
        
        # sample probabilities for a range of outcomes
        values = [value for value in range(startrange, endrange)]
        probabilities = [dist.pdf(value) for value in values]    
        prob=sum(probabilities)
        print("The area between range({},{}):{}".format(startrange,endrange,sum(probabilities)))
        return prob

    def stdNBgraph(dataset):
            # Coverted to standard Normal Distribution
        import seaborn as sns
        mean=dataset.mean()
        std=dataset.std()
    
        values=[i for i in dataset]
    
        z_score=[((j-mean)/std) for j in values]
    
        sns.distplot(z_score,kde=True)
    
        sum(z_score)/len(z_score)
        #z_score.std()