from logging import getLogger
from pathlib import Path
from logargparser import LoggingArgumentParser
import pandas as pd


logger = getLogger(__name__)


def main():
    parser = LoggingArgumentParser(logger)

    parser.add_argument("-o", "--output", required=True, help="Output csv file.")
    parser.add_argument("left", help="Left input file.")
    parser.add_argument("right", help="Right input file.")

    args = parser.parse_args()

    left_file = Path(args.left)
    right_file = Path(args.right)

    output_file = Path(args.output)

    logger.info(f"Joining {left_file} to {right_file} to produce {output_file}.")

    join_on = ['STATE', 'COUNTY', 'TRACT']

    logger.info(f"Reading {left_file}.")
    df_left = pd.read_csv(left_file, header=0)
    logger.info(f"Left shape: {df_left.shape}")

    logger.info(f"Reading {right_file}.")
    df_right = pd.read_csv(right_file, header=0)
    logger.info(f"Right shape: {df_right.shape}")

    df_join = df_left.merge(df_right, on=join_on)

    logger.info(f"Join shape: {df_join.shape}")

    logger.info(f"Writing to {output_file}")
    df_join.to_csv(output_file, header=True, index=False)


if __name__ == '__main__':
    main()
