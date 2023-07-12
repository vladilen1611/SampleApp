import logging
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from utils import order_df, order_line_df, product_promotion_df, vendor_commissions_df

router = APIRouter()

logger = logging.getLogger(__name__)


class Commissions(BaseModel):
    promotions: dict[str, float]
    total: Optional[float]
    order_average: Optional[float]


class Report(BaseModel):
    customers: Optional[int]
    total_discount_amount: Optional[float]
    items: Optional[int]
    order_total_avg: Optional[float]
    discount_rate_avg: Optional[float]
    commissions: Commissions


@router.get("/report", response_model=Report)
async def get_info_by_date(date: date):
    logger.info("Start calculation stat")
    orders_by_date = order_df[(order_df['created_at'] >= str(date)) & (order_df['created_at'] < str(date + timedelta(days=1)))]
    customers = orders_by_date['customer_id'].nunique()
    items = order_line_df[order_line_df['order_id'].isin(orders_by_date['id'])]['quantity'].sum()
    total_discount_amount = order_line_df[order_line_df['order_id'].isin(orders_by_date['id'])]['discount_rate'].sum()
    order_total_avg = order_line_df[order_line_df['order_id'].isin(orders_by_date['id'])]['total_amount'].mean()
    discount_rate_avg = order_line_df[order_line_df['order_id'].isin(orders_by_date['id'])]['discount_rate'].mean()

    vendor_commissions_on_date = vendor_commissions_df[vendor_commissions_df['date'] == str(date)]
    total = (order_line_df[order_line_df['order_id'].isin(orders_by_date['id'])]['total_amount'].sum() *
                                vendor_commissions_on_date['rate']).sum()
    order_average = total / orders_by_date.shape[0]
    promotions_on_date = product_promotion_df[product_promotion_df['date'] == str(date)]
    promotions: dict = {}
    for promotion_id in promotions_on_date['promotion_id'].unique():
        id_order = orders_by_date[orders_by_date['vendor_id'] == promotion_id]
        promotions[str(promotion_id)] = (
                    order_line_df[order_line_df['order_id'].isin(id_order['id'])]['total_amount'].sum() *
                    vendor_commissions_on_date[vendor_commissions_on_date['vendor_id'] == promotion_id]['rate']).sum()
    commissions = Commissions(
        promotions=promotions,
        total=total,
        order_average=order_average
    )
    response = Report(
        customers=customers,
        total_discount_amount=total_discount_amount,
        items=items,
        order_total_avg=order_total_avg,
        discount_rate_avg=discount_rate_avg,
        commissions=commissions
    )

    return response
