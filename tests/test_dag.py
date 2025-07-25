from airflow.models import DagBag

def test_dag_imports():
    dagbag = DagBag(include_examples=False)
    dag = dagbag.get_dag('e_commerce_etl')
    assert dag is not None
    # expect three tasks: load_sales, load_products, transform
    assert len(dag.tasks) == 3
