# Import pandas
import pandas as pd
import pandas_profiling


def makeDateNumeric(text):
    numMonths = int(text[:2])
    numYears = int(text[3:7])
    result = (numYears - 2000) * 12 + numMonths
    return result


def makeDayNumeric(text):
    numMonths = int(text[3:5])
    numYears = int(text[6:10])
    result = (numYears - 2000) * 12 + numMonths
    return result


def build_features(df):
    # Define the DEFAULT FLAG
    # df.rename(index=str, columns={'ForeclosureDate': 'Default'}, inplace= True)
    # df['Default'].fillna(0, inplace=True)
    # df.loc[df['Default'] != 0, 'Default'] = 1
    # print(df['Default'].head())
    # df['Default'] = df['Default'].astype('category')

    # pd.to_numeric(df['Default'], errors='coerce')

    # REMOVE CONSTANT FEATURES (see profile-report)
    df = df.drop(['ProductType', 'ServicingIndicator'], axis=1)

    # REMOVE FEATURES WITH MORE THAN 90% MISSING VALUES

    # GET DATA WITH ONLY NUMERICAL FEATURES
    num_feat = df.select_dtypes(include=['int32', 'int64', 'float64']).columns

    # CATEGORICAL FEATURES
    obj_feat = df.select_dtypes(include='object').columns

    cat_feat = ['Channel', 'SellerName', 'FTHomeBuyer', 'LoanPurpose', 'PropertyType', 'OccStatus', 'PropertyState',
                'ProductType', 'RelMortInd', 'ModFlag']

    # TRANSFORM DATES TO NUMBER OF MONTHS (STARTING FROM 01/2000)
    df['MonthRep'] = df['MonthRep'].apply(makeDayNumeric)
    df['OrDate'] = df['OrDate'].apply(makeDateNumeric)
    df['FirstPayment'] = df['FirstPayment'].apply(makeDateNumeric)
    df['MaturityDate'] = df['MaturityDate'].apply(makeDateNumeric)

    pd.to_numeric(df['MonthRep'], errors='coerce')
    pd.to_numeric(df['OrDate'], errors='coerce')
    pd.to_numeric(df['FirstPayment'], errors='coerce')
    pd.to_numeric(df['MaturityDate'], errors='coerce')

    print(df.head())

    # SPLIT INPUT AND TARGET VARIABLES
    # y = df[['Default']]
    # X = df.drop(['Default'], axis=1)

    # return X


if __name__ == '__main__':

    #  The features of Table Acquisition
    col_acq = ['LoanID','Channel','SellerName','OrInterestRate','OrUnpaidPrinc','OrLoanTerm',
                'OrDate','FirstPayment','OrLTV','OrCLTV','NumBorrow','DTIRat','CreditScore',
                'FTHomeBuyer','LoanPurpose','PropertyType','NumUnits','OccStatus','PropertyState',
                'Zip','MortInsPerc','ProductType','CoCreditScore','MortInsType','RelMortInd']

    #  The features of Table Performance
    col_per = ['LoanID','MonthRep','Servicer','CurrInterestRate','CAUPB','LoanAge','MonthsToMaturity',
                  'AdMonthsToMaturity','MaturityDate','MSA','CLDS','ModFlag','ZeroBalCode','ZeroBalDate',
                  'LastInstallDate','ForeclosureDate','DispositionDate','PPRC','AssetRecCost','MHRC',
                  'ATFHP','NetSaleProceeds','CreditEnhProceeds','RPMWP','OFP','NIBUPB','PFUPB','RMWPF',
                  'FPWA','ServicingIndicator']

    linesToRead = 1000000

    aquisition_frame = pd.read_csv('C:/Users/bebxadvberb/Documents/AI/Trusted AI/Acquisition_2007Q4.txt', sep='|', names=col_acq, nrows= linesToRead)
    performance_frame = pd.read_csv('C:/Users/bebxadvberb/Documents/AI/Trusted AI/Performance_2007Q4.txt', sep='|', names=col_per, index_col=False, nrows = linesToRead)

    # performance_frame.drop_duplicates(subset='LoanID', keep='last', inplace=True)

    # Merge the two DF's together using inner join
    df = pd.merge(aquisition_frame, performance_frame, on = 'LoanID', how='inner')

    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile="report.html")
    print("1")


    build_features(df)
    print("2")

    print(df.dtypes)

    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile="report2.html")
    print("3")