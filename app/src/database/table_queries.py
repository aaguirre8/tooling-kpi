CREATE_COMPLETED_WORK_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS public.completed_work_orders(
    week INT,
    work_orders VARCHAR(255) PRIMARY KEY,
    status VARCHAR(255),
    engineer VARCHAR(255),
    technician VARCHAR(255),
    priority VARCHAR(255),
    modification_date TIMESTAMP,
    wip_date TIMESTAMP,
    finished_date TIMESTAMP,
    finished_week INT
);
"""