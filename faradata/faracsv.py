from logging import getLogger
from pathlib import Path
from logargparser import LoggingArgumentParser
import pandas as pd


logger = getLogger(__name__)


def main():
    parser = LoggingArgumentParser(logger)

    parser.add_argument("-o", "--output", required=True, help="Output csv file.")
    parser.add_argument("xls", help="Input .xls file.")

    args = parser.parse_args()

    xls = Path(args.xls)
    output_file = Path(args.output)

    logger.info(f"Reading excel file {xls}.")

    df_xls = pd.read_excel(
        xls,
        sheet_name="Food Access Research Atlas",
        # The list of indices here comes from manually looking up the
        # variables we want in the "Variable Lookup" tab of the
        # FoodAccessResearchAtlasData2019.xls spreadsheet. The indices
        # here are each two less than the row number describing the
        # variables we want.
        usecols=(
            0,  # Census Tract
            3,  # Urban
            4,  # Population
            5,  # housing units
            16,  # Median family income
            # 67,963 rows out of 72,531 have values
            31,  # lapophalf
            32,  # lapophalfshare
            # 52,542 rows
            57,  # lapop1
            58,  # lapop1share
            # Only 7,766 rows
            83,  # lapop10
            84,  # lapop10share
            # Only 1,506 rows
            109,  # lapop20
            110,  # lapop20share
        ),
        dtype={"CensusTract": str},
    )

    logger.info(f"Read {len(df_xls.index)} rows.")

    logger.info("Computing/rearranging columns.")

    # Pull apart the tract geo into typical censusdis components.
    df_xls['STATE'] = df_xls['CensusTract'].str[:2]
    df_xls['COUNTY'] = df_xls['CensusTract'].str[2:5]
    df_xls['TRACT'] = df_xls['CensusTract'].str[5:]

    df = df_xls[
        ['STATE', 'COUNTY', 'TRACT'] + list(df_xls.columns)[1:-3]
    ]

    logger.info(f"Writing to {output_file}")
    df.to_csv(output_file, header=True, index=False)


if __name__ == "__main__":
    main()
