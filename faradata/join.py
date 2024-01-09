from logging import getLogger
from pathlib import Path
from logargparser import LoggingArgumentParser
import pandas as pd
import matplotlib.pyplot as plt

from censusdis.data import add_inferred_geography
from censusdis.maps import plot_map


logger = getLogger(__name__)


def main():
    parser = LoggingArgumentParser(logger)

    parser.add_argument("-o", "--output", required=True, help="Output csv file.")
    parser.add_argument("--map", type=str, help="Output file for a map of the joined geographies.")
    parser.add_argument("--map-y", type=str, help="Column to render on the map.")
    parser.add_argument("left", help="Left input file.")
    parser.add_argument("right", help="Right input file.")

    args = parser.parse_args()

    left_file = Path(args.left)
    right_file = Path(args.right)

    output_file = Path(args.output)

    logger.info(f"Joining {left_file} to {right_file} to produce {output_file}.")

    join_on = ['STATE', 'COUNTY', 'TRACT']
    dtype = {col: str for col in join_on + ['PLACE']}

    logger.info(f"Reading {left_file}.")
    df_left = pd.read_csv(left_file, header=0, dtype=dtype)
    logger.info(f"Left shape: {df_left.shape}")

    logger.info(f"Reading {right_file}.")
    df_right = pd.read_csv(right_file, header=0, dtype=dtype)
    logger.info(f"Right shape: {df_right.shape}")

    df_join = df_left.merge(df_right, on=join_on)

    logger.info(f"Join shape: {df_join.shape}")

    logger.info(f"Writing to {output_file}")
    df_join.to_csv(output_file, header=True, index=False)

    if args.map is not None:
        gdf = add_inferred_geography(df_join, 2019)
        if args.map_y is not None:
            logger.info(f"Shape before dropping {args.map_y} NaNs: {gdf.shape}")
            gdf2 = gdf.dropna(subset=args.map_y)
            logger.info(f"Shape after dropping {args.map_y} NaNs: {gdf2.shape}")
        else:
            gdf2 = gdf
        ax = plot_map(
            gdf2,
            with_background=True,
            color="purple",
            alpha=0.5,
            figsize=(10, 10)
        )
        plot_map(gdf.boundary, color='black', ax=ax)
        plt.savefig(args.map)


if __name__ == '__main__':
    main()
