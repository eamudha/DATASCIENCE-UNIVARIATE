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