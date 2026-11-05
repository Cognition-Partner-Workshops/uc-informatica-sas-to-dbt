{#-
  Land the m_demo_mapping1 seed inputs from legacy/informatica/data/ into
  var('infa_source_schema'). Column types are explicit (no sniffing) so codes
  and markers stay text. Lookup tables carry SEED_ROW, the physical seed row
  order, which drives the "Use Last Value" multiple-match policy.
  Usage: dbt run-operation load_infa_inputs
-#}
{% macro load_infa_inputs() %}
  {%- set schema = var('infa_source_schema') -%}
  {%- if schema | lower == 'main' -%}
    {{ exceptions.raise_compiler_error('infa_source_schema must not be main') }}
  {%- endif -%}
  {%- set data_dir = var('infa_data_dir') | replace('\\', '/') -%}
  {%- set tables = [
    ('DEMO_SOURCE3', 'demo_source3.csv', false, {
      'TX_ID': 'BIGINT', 'ACCT_ID': 'BIGINT', 'FIRST_NM': 'VARCHAR', 'LAST_NM': 'VARCHAR',
      'TX_DTTM': 'TIMESTAMP', 'TX_AMT': 'DOUBLE', 'TX_TYPE_CD': 'VARCHAR', 'BAL_AMT': 'DOUBLE',
      'TX_DESC': 'VARCHAR', 'CRDT_SCORE': 'BIGINT', 'CUST_ID': 'BIGINT'}),
    ('DEMO_SOURCE4', 'demo_source4.csv', false, {
      'ACCT_ID': 'BIGINT', 'ACCT_TYP': 'VARCHAR', 'ACCT_DESC': 'VARCHAR', 'CRDT_LN': 'VARCHAR',
      'CR8_DT': 'DATE', 'CLSR_DT': 'DATE', 'ACCT_STAT_CD': 'VARCHAR'}),
    ('DEMO_SOURCE5', 'demo_source5.csv', false, {
      'PRODUCT_ID': 'VARCHAR', 'PRODUCT_NM': 'VARCHAR', 'PRODUCT_NO': 'VARCHAR', 'COLOR': 'VARCHAR',
      'STD_COST': 'VARCHAR', 'LIST_PRICE': 'VARCHAR', 'SELL_ST_DT': 'VARCHAR', 'SELL_ED_DT': 'VARCHAR'}),
    ('LKP_DEMO_SOURCE1', 'lkp_demo_source1.csv', true, {
      'ACCT_ID': 'BIGINT', 'CUST_ID': 'BIGINT', 'FIRST_NM': 'VARCHAR', 'LAST_NM': 'VARCHAR',
      'CUST_ADDR': 'VARCHAR', 'CUST_PHN': 'VARCHAR', 'CUST_EML_ADDR': 'VARCHAR', 'AGE': 'VARCHAR',
      'DOB': 'VARCHAR', 'CUST_TYP': 'VARCHAR'}),
    ('LKP_DEMO_SOURCE2', 'lkp_demo_source2.csv', true, {
      'CUST_ID': 'BIGINT', 'CRDT_SCORE': 'BIGINT', 'MAX_CRDT_SCORE': 'BIGINT', 'MIN_CRDT_SCORE': 'BIGINT',
      'MAX_CRDT_LMT': 'BIGINT', 'CURR_CRDT_BAL_AMT': 'DOUBLE', 'AVG_INC_AMT': 'DOUBLE'}),
    ('LKP_DEMO_SOURCE3', 'lkp_demo_source3.csv', true, {
      'ACCT_ID': 'BIGINT', 'TX_TYPE_CD': 'VARCHAR', 'TX_TYPE_DESC': 'VARCHAR'}),
  ] -%}
  {% do run_query('CREATE SCHEMA IF NOT EXISTS ' ~ schema) %}
  {%- for name, file, seed_row, columns in tables %}
    {%- set cols = [] -%}
    {%- for col, typ in columns.items() -%}
      {%- do cols.append("'" ~ col ~ "': '" ~ typ ~ "'") -%}
    {%- endfor -%}
    {%- set reader = "read_csv('" ~ data_dir ~ "/" ~ file ~ "', header=true, auto_detect=false, columns={" ~ cols | join(', ') ~ "})" -%}
    {%- if seed_row -%}
      {%- set select = 'SELECT row_number() OVER () AS SEED_ROW, * FROM ' ~ reader -%}
    {%- else -%}
      {%- set select = 'SELECT * FROM ' ~ reader -%}
    {%- endif -%}
    {% do run_query('CREATE OR REPLACE TABLE ' ~ schema ~ '.' ~ name ~ ' AS ' ~ select) %}
    {%- set n = run_query('SELECT count(*) FROM ' ~ schema ~ '.' ~ name).columns[0].values()[0] -%}
    {{ log('loaded ' ~ schema ~ '.' ~ name ~ ' (' ~ n ~ ' rows)', info=True) }}
  {%- endfor %}
{% endmacro %}
