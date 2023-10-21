import pandas as pd

class CleanCurryCompData():

    TO_INT = ["Delivery_person_Age", "multiple_deliveries", "Time_taken(min)"]
    TO_FLOAT = ["Delivery_person_Ratings"]


    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        df = CleanCurryCompData.remove_nan(df)
        df = CleanCurryCompData.remove_extra_spaces(df)
        df = CleanCurryCompData.format_time(df)
        df = CleanCurryCompData.obj_to_num(df, CleanCurryCompData.TO_INT)
        df = CleanCurryCompData.obj_to_num(df, CleanCurryCompData.TO_FLOAT, float)
        df = CleanCurryCompData.obj_to_date(df)
        df = CleanCurryCompData.add_week_of_year(df)
        return df
    

    @staticmethod
    def remove_nan(df: pd.DataFrame) -> pd.DataFrame:
        # Removing NaNs
        cols = ["Delivery_person_Age", "Weatherconditions", "Road_traffic_density",
                "multiple_deliveries", "Festival", "City"]
        for col in cols:
            df = df.loc[~df[col].str.contains("NaN"), :]
        return df
        

    @staticmethod
    def remove_extra_spaces(df: pd.DataFrame) -> pd.DataFrame:
        # Removing extra spaces
        cols = ["Road_traffic_density", "Type_of_order", "Type_of_vehicle", "Festival",
                "City"]
        for col in cols:
            df[col] = df[col].str.strip()
        return df
    

    @staticmethod
    def format_time(df: pd.DataFrame) -> pd.DataFrame:
        # Removing (min) string from Time_taken(min) column
        df["Time_taken(min)"] = df["Time_taken(min)"].apply(lambda x: x.split(' ')[1])
        return df
    

    @staticmethod
    def obj_to_num(df: pd.DataFrame, cols, type=int) -> pd.DataFrame:
        # Converting numerical data as object to numerical types
        for col in cols:
            df[col] = df[col].astype(type)
        return df
    

    @staticmethod
    def obj_to_date(df: pd.DataFrame) -> pd.DataFrame:
        # Converting date string to datetime
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y")
        return df
    

    @staticmethod
    def add_week_of_year(df: pd.DataFrame) -> pd.DataFrame:
        # Adding week_of_year column
        df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )
        return df


    # @staticmethod
    # def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #     df = remove_nan(df)
    #     df = remove_extra_spaces(df)
    #     df = format_time(df)
    #     df = obj_to_num(df, TO_INT)
    #     df = obj_to_num(df, TO_FLOAT, float)
    #     df = obj_to_date(df)
    #     df = add_week_of_year(df)
    #     return df
