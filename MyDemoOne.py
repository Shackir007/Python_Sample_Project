data_table_spec = 'bigquery-Mydemo-352121:dataset_Unicorn_Companies.divided_data1'
other_table_spec = 'bigquery-Mydemo-352121:dataset_Unicorn_Companies.divided_data2'

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse
from google.cloud import bigquery

parser = argparse.ArgumentParser()

parser.add_argument('--input',
                    dest='input',
                    required=True,
                    help='Input file to process.')

path_args, pipeline_args = parser.parse_known_args()

inputs_pattern = path_args.input

options = PipelineOptions(pipeline_args)

p = beam.Pipeline(options=options)


def remove_last_colon(row):
    cols = row.split(',')
    item = str(cols[4])

    if item.endswith(':'):
        cols[9] = item[:-1]

    return ','.join(cols)


def remove_special_characters(row):
    import re
    cols = row.split(',')  #
    ret = ''
    for col in cols:
        clean_col = re.sub(r'[?%&]', '', col)
        ret = ret + clean_col + ','
    ret = ret[:-1]
    return (ret)


def print_row(row):
    print(row)


cleaned_data = (
        p
        | beam.io.ReadFromText(inputs_pattern, skip_header_lines=1)
        | beam.Map(remove_last_colon)
        | beam.Map(lambda row: row.lower())
        | beam.Map(remove_special_characters)
        | beam.Map(lambda row: row + ',1')
)

divided_data1 = (
        cleaned_data
        | 'continent_one' >> beam.Filter(lambda row: row.split(',')[6].lower() == 'north america')
)

divided_data2 = (
        cleaned_data
        | 'continent_two' >> beam.Filter(lambda row: row.split(',')[6].lower() == 'europe')
)
(
        cleaned_data
        | 'count total' >> beam.combiners.Count.Globally()
        | 'total map' >> beam.Map(lambda x: 'Total Count:' + str(x))
        | 'print total' >> beam.Map(print_row)

)

(divided_data1
 | 'count data1' >> beam.combiners.Count.Globally()
 | 'data1 map' >> beam.Map(lambda x: 'Delivered count:' + str(x))
 | 'print data1 count' >> beam.Map(print_row)
 )

(divided_data2
 | 'count data2' >> beam.combiners.Count.Globally()
 | 'data2 map' >> beam.Map(lambda x: 'Others count:' + str(x))
 | 'print data2' >> beam.Map(print_row)
 )

# BigQuery 
client = bigquery.Client()

dataset_id = "{}.dataset_Unicorn_Companies".format(client.project)

try:
    client.get_dataset(dataset_id)

except:
    dataset = bigquery.Dataset(dataset_id)  #

    dataset.location = "US"
    dataset.description = "dataset for unicorn companies"

    dataset_ref = client.create_dataset(dataset, timeout=30)  # Make an API request.


def to_json(csv_str):
    fields = csv_str.split(',')

    json_str = {"Company": fields[0],
                "Valuation": fields[1],
                "Date Joined": fields[2],
                "Industry": fields[3],
                "City": fields[4],
                "Country": fields[5],
                "Continent": fields[6],
                "Year Founded": fields[7],
                "Funding": fields[8],
                "Select Investors": fields[9],

                }

    return (json_str)


table_schema = 'Company:STRING,Valuation:STRING,Date Joined:STRING,Industry:STRING,City:STRING,Country:STRING,Continent:STRING,Year Founded:STRING,Funding:STRING,Select Investors:STRING'

(divided_data1
 | 'delivered to json' >> beam.Map(to_json)
 | 'write data one' >> beam.io.WriteToBigQuery(
            data_table_spec,
            schema=table_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            additional_bq_parameters={'timePartitioning': {'type': 'DAY'}}
        )
 )

(divided_data2
 | 'others to json' >> beam.Map(to_json)
 | 'write data two' >> beam.io.WriteToBigQuery(
            other_table_spec,
            schema=table_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            additional_bq_parameters={'timePartitioning': {'type': 'DAY'}}
        )
 )

from apache_beam.runners.runner import PipelineState

ret = p.run()
if ret.state == PipelineState.DONE:
    print('Success!!!')
else:
    print('Error Running beam pipeline')

view_name = "daily_Unicorn_count"
dataset_ref = client.dataset('dataset_Unicorn_Companies_latest')
view_ref = dataset_ref.table(view_name)
view_to_create = bigquery.Table(view_ref)

view_to_create.view_query = 'select * from `bigquery-Mydemo-352121.dataset_Unicorn_Companies_latest.divided_data1` where _PARTITIONDATE = DATE(current_date())'
view_to_create.view_use_legacy_sql = False

try:
    client.create_table(view_to_create)

except:
    print('View already exists')
