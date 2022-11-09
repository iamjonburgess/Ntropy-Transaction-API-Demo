
!pip install ntropy_sdk

# we'll need the 'random' and 'string' libraries to emulate data we don't have for this demonstration.
import random
import string
from io import StringIO
from ntropy_sdk import SDK, Transaction, EnrichedTransaction
import pandas as pd

# for demonstration purposes we'll use a transaction string instead of a .csv file commonly used in financial services.

txns = """description	amount	iso_currency_code
Aktywna Warszawa   S	21.07	PLN
Crv*Ww Beauty Lukasz Mich	18.83	PLN
Bolt.Eu/R/2207180715	96.34	EUR
Purchase from AMZN	3.64	EUR
## DEPOSIT	95.77	EUR
CARD TRANSACTION #69420	74.05	EUR
>> ^0_o^ <<	64.97	EUR
Crypto.com: Allegro.pl gift card purchase	74.7	EUR
Paypal help ukraine donate	68.76	EUR
OPENPAY*CERVEZASIEMPRE CIUDAD DE MEXIC	26.47	USD
PAYPAL INST XFER MICROSOFT ACH_DEBIT	4.9	USD
Paypal *xsolla mtgarena	70.35	USD
M10GRAPHIC   CA venture capital call	27.71	USD
Compra Cart Elo Estacao Imperial Ltd	52.88	USD
PIERRE CARD IN	79.28	USD
twitch blizzard overwatch Mr Streamer	45.76	USD
Dep Transf Bdn Maria Jose Resende	46.07	USD
AMZN Mktp US AWS	85.94	USD
LATE FEE FOR PAYMENT DUE transbank	86.89	USD
ntropy api pmnt	1.84	USD
BTC sell: 0.000343298	0.03	USD
BTC sell: 0.00343449	25.2	USD
BTC sell: 0.0440243	130.34	USD
BTC sell: 0.0332351	1040.22	USD
BTC sell: 1.317991	55000.12	USD
"""
# we'll create this function to emulate transaction data that we'd normally have in a real world scenario.
def generate_random_string(length):
  for j in range(len(length)):
    return "".join(random.choice(string.ascii_lowercase + string.digits))

# we'll use pandas to create a dataframe for the api to process.
def df_from_csv(transactions=None):
    csv = StringIO(txns)
    csv.seek(0)
    df = pd.read_csv(csv, sep='\t')
    txs = []
	# since this is a demo we don't have real accounts so we'll generate them here.
    account_name = generate_random_string(transactions) 

    for i, row in df.iterrows():
        tx = {
            "date": "2022-01-01",
            "entry_type": "outgoing",
            "amount": row['amount'],
            "iso_currency_code": row["iso_currency_code"],
            "description": row["description"],
            "transaction_id": f"id_{i}",
            "account_holder_type": "consumer", # we'll use consumer, but there's more categories which can be found in the Ntropy documentation.
            "account_holder_id": account_name,
        }
        txs.append(tx)

    return pd.DataFrame(txs)

# we'll enter our key here (a key can be requested at https://ntropy.com/)
sdk = SDK('API KEY')

# now lets enrich the transactions into a dataframe object and store in a variable
result = sdk.add_transactions(df_from_csv(txns))

# lets update the dataframe and remove extraneous columns (data missing in tuples for demonstration)
result = result[['description', 'amount', 'iso_currency_code', 'transaction_id', 'labels', "merchant", "website"]]

# finally we can view the table and analyze any discrepancies with the transaction data
result
