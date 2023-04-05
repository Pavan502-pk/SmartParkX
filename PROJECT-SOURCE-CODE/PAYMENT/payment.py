import pyqrcode
import png

def payment(amnt):

    upi_id="pavankalyanmahanthi-1@okaxis"

    reciver_name="PavanKalyanMahanty"

    amount= amnt

    currency="INR"

    trans_note="Parking Charges"

    upi_link=f'upi://pay?pa={upi_id}&pn={reciver_name}&cu={currency}&am={amount}&tn={trans_note}'

    result=pyqrcode.create(upi_link)

    result.png("E:\MAJOR_PROJECT\static\output.png" , scale=8) 
    
#payment(11.00)