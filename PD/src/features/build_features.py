
if __name__ == '__main__':

    # Define the DEFAULT FLAG
    df.rename(index=str, columns={'ForeclosureDate': 'Default'}, inplace=True)
    df['Default'].fillna(0, inplace=True)
    df.loc[df['Default'] != 0, 'Default'] = 1  
    df['Default'] = df['Default'].astype(int)

    # REMOVE CONSTANT FEATURES (see profile-report)
    df.drop(['ProductType', 'ServicingIndicator'])

    # REMOVE FEATURES WITH MORE THAN 90% MISSING VALUES




    # SPLIT INPUT AND TARGET VARIABLES
    y = df[['Default']]
    X = df.drop(['Default'], axis=1)

    dates = df.select_dtypes(include='date').columns
