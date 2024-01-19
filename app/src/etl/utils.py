import pandas as pd


def transform_data_to_scd(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the dataset into a format suitable for Slowly Changing Dimension (SCD) Type 2.

    Args:
        df (pd.DataFrame): The raw dataset containing work orders, status, and modification dates.

    Returns:
        pd.DataFrame: A transformed DataFrame with separate columns for start and finish dates.
    """
    # Create two separate dataframes for start and finish dates
    start_date_df = df[df["status"] == "WIP"].rename(columns={"modification_date": "start_date"})
    finish_data_df = df[df["status"] == "Terminado"].rename(
        columns={"modification_date": "finish_date"}
    )

    start_df = start_date_df.drop(columns=["status"])
    finish_df = finish_data_df[["work_order", "finish_date"]]

    # Merge the two dataframes on 'work_order' to rearrange the columns
    transformed_df = pd.merge(start_df, finish_df, on="work_order", how="outer")

    transformed_df = transformed_df.where(pd.notna(transformed_df), None)

    transformed_df = transformed_df.drop_duplicates(subset=["work_order"])

    return transformed_df


def determine_status(row):
    if row["finish_date"] is None:
        return "WIP"
    else:
        return "Finished"


def add_tracking_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds tracking data to a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to which tracking data is to be added.

    Returns:
        pd.DataFrame: The DataFrame with tracking data added.
    """
    # Flag if the work order is finished or is work in process
    df["status"] = df.apply(determine_status, axis=1)

    # Add the number week when the work order was assigned
    # Notice, date columns are converted to datetime to apply the dt.week method
    # Before the data is loaded, the date columns are converted to datetime
    date_cols = ["start_date", "finish_date"]
    week_cols = ["start_week", "finish_week"]

    for date, week in zip(date_cols, week_cols):
        df[date] = pd.to_datetime(df[date])
        df[week] = df[date].dt.isocalendar().week

    # df["start_date"] = pd.to_datetime(df["start_date"])
    # df["finish_date"] = pd.to_datetime(df["finish_date"])
    # df["start_week"] = df["start_date"].dt.isocalendar().week
    # df["finish_week"] = df["finish_date"].dt.isocalendar().week

    return df
