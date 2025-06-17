def snowflake_pipeline():
    from etls.snowflake_etl import upload_to_snowflake, connect_to_snowflake

    conn = connect_to_snowflake()
    upload_to_snowflake(conn)
