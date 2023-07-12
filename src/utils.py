import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)


logger.info("Load data from /data folder")

order_df = pd.read_csv(os.path.abspath('./data/orders.csv'))
order_line_df = pd.read_csv(os.path.abspath('./data/order_lines.csv'))
product_promotion_df = pd.read_csv(os.path.abspath('./data/product_promotions.csv'))
vendor_commissions_df = pd.read_csv(os.path.abspath('./data/commissions.csv'))
