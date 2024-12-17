from dotenv import dotenv_values
from typing import Literal
import funcs

class Queries:
    def __init__(self):
        self.databases = dotenv_values('.databases.env')
        self.tcvs = dotenv_values('.tabs_cols_vals.env')

    def print_tcvs(self):
        for key, value in self.tcvs.items():
            print(f"{key}: {value}")

    def get_retail_sales(
            self, 
            brands: str | list[str],
            loc_brands: str | list[str],
            years: int | list[int] | None = None,
            intra_mode: Literal['IC','NIC'] | None = None,
            intras_loc: list[str] | None = None,
            in_details: bool = False
        ):
        no_years = years is None
        intra_non_intra = intra_mode is None
        brands_str = funcs.in_sql_concatenation(brands)
        loc_brands_str = funcs.in_sql_concatenation(loc_brands)
        years_str = '' if no_years else funcs.in_sql_concatenation(years)
        intras_str = (
            '' 
            if intra_non_intra else 
            funcs.in_sql_concatenation(intras_loc)
        )
        
        return f"""
            WITH bon_barcode_list AS (
                SELECT DISTINCT 
                    sales.{self.tcvs['c_receipt_no']} + sales.{self.tcvs['c_bc']} bon_barcode,
                    sales.{self.tcvs['c_bc']} barcode
                FROM {self.tcvs['t_ret_sales']} sales
                LEFT JOIN {self.tcvs['t_loc']} sh_room
                ON
                    sales.{self.tcvs['c_code']} = sh_room.{self.tcvs['c_code']}
                LEFT JOIN {self.tcvs['t_items']} items
                ON
                    sales.{self.tcvs['c_bc']} = items.{self.tcvs['c_bc']}
                WHERE 
                    sh_room.{self.tcvs['c_brand']} IN {loc_brands_str} AND
                    -- BAZZAR or BAZAAR are intracompany transaction
                    {
                        ''
                        if intra_non_intra
                        else f"sh_room.{self.tcvs['c_loc_code']} {"" if intra_mode == "IC" else "NOT"} LIKE {intras_str} AND"
                    }
                    items.{self.tcvs['c_item_brand']} IN {brands_str} AND
                    sales.{self.tcvs['c_t_price']} != 0 AND 
                    sales.{self.tcvs['c_canceled']} IS NULL 
                    {
                        ''
                        if no_years
                        else f"AND YEAR(sales.{self.tcvs['c_trx_date']}) IN {years_str}"
                    }
            ), barcode_max_fbulan AS (
                SELECT DISTINCT
                    {self.tcvs['c_bc']} barcode,
                    MAX({self.tcvs['c_month']}) OVER(PARTITION BY {self.tcvs['c_bc']}) year_month
                FROM {self.tcvs['t_cogs']}
                WHERE
                    {self.tcvs['c_bc']} IN (SELECT DISTINCT barcode FROM bon_barcode_list)
            ),
            sales_in_detail AS (
                SELECT
                    '{self.databases['SOS']}' source_db,
                    '{self.tcvs['v_retail']}' channel,
                    CASE
                        WHEN sales.{self.tcvs['c_code']} IN {intras_str}
                        THEN '{self.tcvs['v_ic']}'
                        ELSE '{self.tcvs['v_nic']}'
                    END ic_or_nic,
                    CAST(sales.{self.tcvs['c_trx_date']} AS DATE) transaction_date,
                    CAST(sales.{self.tcvs['c_created']} AS TIME) transaction_time,
                    YEAR(sales.{self.tcvs['c_trx_date']}) year,
                    MONTH(sales.{self.tcvs['c_trx_date']}) month,
                    sales.{self.tcvs['c_code']} store_code,
                    sh_room.{self.tcvs['c_brand']} store_brand,
                    sales.{self.tcvs['c_cust_code']} store_name,
                    NULL cust_code,
                    NULL cust_desc,
                    sales.{self.tcvs['c_receipt_no']} order_no,
                    UPPER(items.{self.tcvs['c_item_brand']}) item_brand,
                    sales.{self.tcvs['c_item_code']} item_code,
                    sales.{self.tcvs['c_bc']} item_barcode,
                    items.{self.tcvs['c_item_desc']} item_desc,
                    items.{self.tcvs['c_item_color']} item_color,
                    items.{self.tcvs['c_item_size']} item_size,
                    items.{self.tcvs['c_item_product']} item_product,
                    items.{self.tcvs['c_item_group']} item_group,
                    sales.{self.tcvs['c_returned']} returned,
                    sales.{self.tcvs['c_qty']} qty,
                    sales.{self.tcvs['c_disc_p']}/100 disc_percent,
                    ABS(sales.{self.tcvs['c_disc_a']}) disc_amount,
                    NULL margin_percent,
                    NULL margin_amount,
                    ABS(sales.{self.tcvs['c_b_price']}) srp_per_unit,
                    ABS(sales.{self.tcvs['c_amt_aft_tax']} + sales.{self.tcvs['c_tax_a']}) srp_per_unit_aft_disc,
                    ABS(sales.{self.tcvs['c_amt_aft_tax']}) srp_per_unit_aft_vat,
                    COALESCE(cogs.{self.tcvs['c_fin_cogs']}, cogs_fallback.{self.tcvs['c_fin_cogs']}, 0) cost_per_unit,
                    sales.{self.tcvs['c_qty']} * ABS(sales.{self.tcvs['c_b_price']}) retail_tag,
                    sales.{self.tcvs['c_qty']} * ABS(sales.{self.tcvs['c_amt_aft_tax']} + sales.{self.tcvs['c_tax_a']}) customer_paid,
                    sales.{self.tcvs['c_qty']} * ABS(sales.{self.tcvs['c_amt_aft_tax']}) net_sales,
                    sales.{self.tcvs['c_qty']} * COALESCE(cogs.{self.tcvs['c_fin_cogs']}, cogs_fallback.{self.tcvs['c_fin_cogs']}, 0) cost
                FROM {self.tcvs['t_ret_sales']} sales
                LEFT JOIN {self.tcvs['t_loc']} sh_room
                ON
                    sales.{self.tcvs['c_code']} = sh_room.{self.tcvs['c_code']}
                LEFT JOIN {self.tcvs['t_items']} items
                ON
                    sales.{self.tcvs['c_bc']} = items.{self.tcvs['c_bc']}
                LEFT JOIN barcode_max_fbulan
                ON
                    sales.{self.tcvs['c_bc']} = barcode_max_fbulan.barcode
                LEFT JOIN {self.tcvs['t_cogs']} cogs
                ON
                    sales.{self.tcvs['c_bc']} = cogs.{self.tcvs['c_bc']} AND
                    FORMAT(sales.{self.tcvs['c_trx_date']}, 'yyMM') = cogs.{self.tcvs['c_month']}
                LEFT JOIN {self.tcvs['t_cogs']} cogs_fallback
                ON
                    sales.{self.tcvs['c_bc']} = cogs_fallback.{self.tcvs['c_bc']} AND
                    barcode_max_fbulan.year_month = cogs_fallback.{self.tcvs['c_month']}
                WHERE
                    {
                        '' 
                        if no_years
                        else f"YEAR(sales.{self.tcvs['c_trx_date']}) IN {years_str} AND"
                    }
                    sales.{self.tcvs['c_receipt_no']} + sales.{self.tcvs['c_bc']} IN (SELECT bon_barcode FROM bon_barcode_list)
            )
            {
                f"""
                    SELECT
                    	*
                    FROM sales_in_detail
                    ORDER BY
                        item_brand DESC,
                        transaction_date DESC,
                        transaction_time DESC
                """
                if in_details
                else f"""
                    SELECT 
                        channel,
                        ic_or_nic,
                        year,
                        month,
                        item_brand,
                        item_product,
                        item_group,
                        SUM(qty) qty,
                        SUM(cost) cost,
                        SUM(retail_tag) retail_tag,
                        SUM(customer_paid) customer_paid,
                        SUM(net_sales) net_sales
                    FROM sales_in_detail
                    GROUP BY
                        channel,
                        ic_or_nic,
                        year,
                        month,
                        item_brand,
                        item_product,
                        item_group
                    ORDER BY
                        channel DESC,
                        item_brand DESC,
                        year DESC,
                        month DESC
                """
            }
        """