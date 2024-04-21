import pandas as pd
from pipeline import ProcessorBase


class TradeDayProcessor(ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(TradeDayProcessor, self).__init__(*args, **kwargs)

    def process(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        return self.process_trade_day_data(input_data)

    def process_trade_day_data(self, trade_day_data: pd.DataFrame) -> pd.DataFrame:
        in_table = trade_day_data.copy()

        out_table_column_name_list = ["date", "is_trade_day"]

        in_table_date_column_name = "calendar_date"
        in_table_is_trade_day_column_name = "is_trading_day"

        in_table_date_column = in_table[in_table_date_column_name]
        in_table_is_trade_day_column = in_table[in_table_is_trade_day_column_name]

        try:
            in_table_date_column = pd.to_datetime(in_table_date_column)
            in_table_is_trade_day_column = in_table_is_trade_day_column.astype("uint8")
        except Exception as e:
            print(f"Error: {e}")

        out_table = pd.DataFrame({out_table_column_name_list[0]: in_table_date_column,
                                  out_table_column_name_list[1]: in_table_is_trade_day_column})

        return out_table


if __name__ == '__main__':
    from producer import TradeDayProducer
    trade_day_data = TradeDayProducer().produce()
    # print(trade_day_data)
    processor = TradeDayProcessor()
    processed_trade_day_data = processor.process_trade_day_data(trade_day_data)

    print(processed_trade_day_data)
    for idx, column_name in enumerate(processed_trade_day_data.columns):
        print(f"column {idx}: name={column_name}, type={type(processed_trade_day_data[column_name][0])}")
