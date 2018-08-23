# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import math
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['ProductSupplier', 'PurchaseRequest', 'CreatePurchase']
__metaclass__ = PoolMeta


class ProductSupplier:
    __name__ = 'purchase.product_supplier'
    multiple_quantity = fields.Float('Multiple Quantity')


class PurchaseRequest:
    __name__ = 'purchase.request'
    multiple_quantity = fields.Function(fields.Float('Multiple Quantity'),
        'on_change_with_multiple_quantity')

    @fields.depends('supplier', 'product')
    def on_change_with_multiple_quantity(self, name):
        if not self.product:
            return
        for product_supplier in self.product.product_suppliers:
            if product_supplier.party == self.party:
                return product_supplier.multiple_quantity


class CreatePurchase:
    __name__ = 'purchase.request.create_purchase'

    @classmethod
    def compute_purchase_line(cls, key, requests, purchase):
        line = super(CreatePurchase, cls).compute_purchase_line(key,
            requests, purchase)
        request = requests[0]
        if request.multiple_quantity:
            line.quantity = (math.ceil(line.quantity /
                    request.multiple_quantity) * request.multiple_quantity)
        return line
