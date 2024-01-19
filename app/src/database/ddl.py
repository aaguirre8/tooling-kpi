CREATE_COMPLETED_WORK_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS public.completed_work_orders(
    start_week INT,
	finish_week INT,
    work_order VARCHAR(255) PRIMARY KEY,
    priority VARCHAR(255),
    status VARCHAR(255),
    engineer VARCHAR(255),
    technician VARCHAR(255),
    modified_by VARCHAR(255),
    start_date TIMESTAMP,
    finish_date TIMESTAMP
);
"""