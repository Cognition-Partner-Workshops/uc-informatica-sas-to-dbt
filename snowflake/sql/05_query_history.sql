select query_id, start_time, end_time, user_name, role_name, warehouse_name,
       database_name, schema_name, execution_status, query_text
from table(information_schema.query_history(
    end_time_range_start => dateadd('hour', -24, current_timestamp()),
    result_limit => 10000
))
where user_name = current_user()
  and (
      upper(coalesce(schema_name, '')) in (
          'SOURCE_INFORMATICA_20260809T234500Z',
          'PYSPARK_INFORMATICA_20260809T234500Z',
          'BASELINE_INFORMATICA_20260809T234500Z'
      )
      or upper(query_text) like '%20260809T234500Z%'
  )
order by start_time;
