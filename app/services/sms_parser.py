import re

#sms example - ICICI Bank Acct XXXX debited for Rs 960.00 on 12-May-26; KANNURU SRINUVA credited.
def icici_sms_parser(sms: str) -> dict | None:
    transaction_details= {}
    amount_match= re.search(r"Rs\s?(\d+\.\d+)", sms)
    if not amount_match:
        return None
    amount=float(amount_match.group(1))

    merchant_match=re.search(r";\s?(.+?)\s?(?:credited|debited)",sms,re.I)
    if not merchant_match:
        return None
    merchant=merchant_match.group(1)

    bank_match=re.search(r"(.+?)\s?Bank",sms,re.I)
    if not bank_match:
        return None
    bank=bank_match.group(1)

    date_match=re.search(r"on\s?(\d{2}[-/]\w+[-/]\d{2,4})",sms,re.I)
    if not date_match:
        return None
    date=date_match.group(1)

    transaction_type_match=re.search(r"(credited|debited)\s?\w+",sms,re.I)
    if not transaction_type_match:
        return None
    transaction_type=transaction_type_match.group(1)

    transaction_details['amount']=amount
    transaction_details['merchant']=merchant
    transaction_details['bank']=bank
    transaction_details['date']=date
    transaction_details["type"]=transaction_type
    return transaction_details

#HDFC Sample- Spent Rs.477.95 On HDFC Bank Card XXXX At PYU*ZOMATO On 2026-05-05:14:34:59
def hdfc_sms_parser(sms: str) -> dict | None:
    transaction_details= {}
    amount_match=re.search(r"Rs\.?\s?(\d+\.\d+)",sms,re.I)
    if not amount_match:
        return None
    transaction_details["amount"]=float(amount_match.group(1))

    merchant_match=re.search(r"At\s?(\w+.*?)\s?On",sms, re.I)
    if not merchant_match:
        return None
    transaction_details["merchant"]=merchant_match.group(1)

    transaction_details["bank"]="HDFC"

    date_match=re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})",sms,re.I)
    if not date_match:
        return None
    transaction_details["date"]=date_match.group(1)

    transaction_type_match=re.search(r"(spent|received)",sms,re.I)
    if not transaction_type_match:
        return None
    transaction_details["type"]="debited" if transaction_type_match.group(1).lower()=="spent" else "credited"
    return transaction_details

#SBI-sample A/C XXXX debited by 14848.06 on date 28Apr26 trf to CRED Club
def sbi_sms_parser(sms: str) -> dict | None:
    transaction_details= {}
    amount_match=re.search(r"(?:debited|credited)\s?by\s?(\d+\.\d+)",sms,re.I)
    if not amount_match:
        return None
    transaction_details["amount"]=float(amount_match.group(1))

    merchant_match=re.search(r"trf\s?to\s?(\w+.+?)\s?Ref",sms, re.I)
    if not merchant_match:
        return None
    transaction_details["merchant"]=merchant_match.group(1)

    transaction_details["bank"]="SBI"

    date_match=re.search(r"(\d{2}\w{3}\d{2})",sms,re.I)
    if not date_match:
        return None
    transaction_details["date"]=date_match.group(1)

    transaction_type_match=re.search(r"(debited|credited)",sms,re.I)
    if not transaction_type_match:
        return None
    transaction_details["type"]=transaction_type_match.group(1)
    return transaction_details

def parse_sms(sms: str)-> dict | None:
    if "ICICI" in sms.upper():
        return  icici_sms_parser(sms)
    elif "HDFC" in sms.upper():
        return hdfc_sms_parser(sms)
    elif "SBI" in sms.upper():
        return sbi_sms_parser(sms)
    else:
        return None