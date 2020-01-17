
from django.db.models.signals import pre_save
from django.dispatch import receiver
from transaction.models import TransactionSale,StorageTransaction
import pdfkit
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@receiver(pre_save,sender=TransactionSale)
def create_invoice_transactionsale(sender,instance,**kwargs):
    var=instance
    str="""<!DOCTYPE HTML PUBLIC"-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html><head> <title>Invoice</title> <style type="text/css">
                body {    font-weight: 200; font-size: 20px;}
                .first {     font-weight: 200;    text-align: center;        color: #007cae;}
                .title {    font-size: 22px; font-weight: 100;  padding: 10px 20px 0px 20px; }
                .details {    padding: 10px 20px 0px 20px;    text-align: left !important; }
            </style>
        </head><body>
                <div class='first'>    <p class='title'style="font-size: 50px;">Invoice </p></div>
            <div class='details'style="padding-left: 50px">
              <span style="font-weight:bold;">Transaction ID : </span>{}<br/>
                <span style="font-weight:bold;">Date : </span> {}<br/>
                <span style="font-weight:bold;">Bill to : </span> {}<br/>
                <span style="font-weight:bold;">FoodGrain : </span> {}</br>
                <span style="font-weight:bold;">Quantity : </span> {}<br/>
                <span style="font-weight:bold;">Price : </span> {} <br/><br><br><br>
                  <span style="font-weight:bold;">Sold By  :</span> {} <br/>
            </div>
        </div>
        </body>
    </html>
""".format(var.transno,datetime.date.today,var.buyer,var.type,var.quantity,var.amount,var.seller)
    output_path='transaction_sale_invoice/invoice_{}.pdf'.format(var.transno)
    pdfkit.from_string(str, output_path)
    var.invoice=os.path.join(ROOT_DIR,output_path)




@receiver(pre_save,sender=StorageTransaction)
def create_invoice_storage_transactions(sender,instance,**kwargs):
    var=instance
    """<!DOCTYPE HTML PUBLIC"-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html><head> <title>Invoice</title> <style type="text/css">
                body {    font-weight: 200; font-size: 20px;}
                .first {     font-weight: 200;    text-align: center;        color: #007cae;}
                .title {    font-size: 22px; font-weight: 100;  padding: 10px 20px 0px 20px; }
                .details {    padding: 10px 20px 0px 20px;    text-align: left !important; }
            </style>
        </head><body>
                <div class='first'>    <p class='title'style="font-size: 50px;">Invoice </p></div>
            <div class='details'style="padding-left: 50px">
              <span style="font-weight:bold;">Transaction ID : </span>{}<br/>
                <span style="font-weight:bold;">Date : </span> {}<br/>
                <span style="font-weight:bold;">Warehouse : </span> {}<br/>
                <span style="font-weight:bold;">Quantity : </span> {}<br/>
                <span style="font-weight:bold;">Price : </span> {} <br/><br><br><br>
                  <span style="font-weight:bold;">Farmer  :</span> {} <br/>
            </div>
        </div>
        </body>
    </html>
""".format(var.transno,var.date,var.warehouse,var.quantity,var.cost,var.farmer)
    output_path='storage_transaction_invoice/invoice_{}.pdf'.format(var.transno)
    pdfkit.from_string(str, output_path)
    var.invoice=os.path.join(ROOT_DIR,output_path)
