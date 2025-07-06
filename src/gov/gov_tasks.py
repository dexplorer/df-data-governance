import logging
import os

from metadata import workflow as wf
from utils import http_io as ufh


def run_data_quality_task(
    required_parameters: dict, cycle_date: str
) -> list[dict]:
    dataset_id = required_parameters["dataset_id"]
    logging.info(
        "Start applying data quality rules on the dataset %s", dataset_id
    )
    # dq_results = dqc.apply_dq_rules(dataset_id=dataset_id, cycle_date=cycle_date)
    url = f"{os.environ['DF_SVC_BASE_URL']}:{os.environ['DF_DATA_QUALITY_SVC_PORT']}/apply-rules"
    payload = {"dataset_id": dataset_id, "cycle_date": cycle_date}
    dq_results = ufh.get_request_with_json_resp_as_dict(
        url=url, payload=payload, connection_timeout=3, read_timeout=60
    )
    logging.info(
        "Finished applying data quality rules on the dataset %s",
        dataset_id,
    )

    return dq_results


def run_data_quality_ml_task(
    required_parameters: dict, cycle_date: str
) -> list[dict]:
    dataset_id = required_parameters["dataset_id"]
    logging.info("Started detecting anomalies in the dataset %s", dataset_id)
    # dqml_results = dqmlc.detect_anomalies(dataset_id=dataset_id, cycle_date=cycle_date)
    url = f"{os.environ['DF_SVC_BASE_URL']}:{os.environ['DF_DATA_QUALITY_ML_SVC_PORT']}/detect-anomalies"
    payload = {"dataset_id": dataset_id, "cycle_date": cycle_date}
    dqml_results = ufh.get_request_with_json_resp_as_dict(
        url=url, payload=payload, connection_timeout=3, read_timeout=20
    )
    logging.info("Finished detecting anomalies in the dataset %s", dataset_id)

    return dqml_results


def run_data_profile_task(
    required_parameters: dict, cycle_date: str
) -> list[dict]:
    dataset_id = required_parameters["dataset_id"]
    logging.info("Start profiling the dataset %s", dataset_id)
    # dp_results = dpc.apply_ner_model(dataset_id=dataset_id, cycle_date=cycle_date)
    url = f"{os.environ['DF_SVC_BASE_URL']}:{os.environ['DF_DATA_PROFILE_SVC_PORT']}/profile-dataset"
    payload = {"dataset_id": dataset_id, "cycle_date": cycle_date}
    dp_results = ufh.get_request_with_json_resp_as_dict(
        url=url, payload=payload, connection_timeout=3, read_timeout=10
    )
    logging.info("Finished profiling the dataset %s", dataset_id)

    return dp_results


def run_data_recon_task(
    required_parameters: dict, cycle_date: str
) -> list[dict]:
    dataset_id = required_parameters["dataset_id"]
    logging.info(
        "Start applying data reconciliation rules on the dataset %s",
        dataset_id,
    )
    # dr_check_results = drc.apply_dr_rules(dataset_id=dataset_id, cycle_date=cycle_date)
    url = f"{os.environ['DF_SVC_BASE_URL']}:{os.environ['DF_DATA_RECON_SVC_PORT']}/apply-rules"
    payload = {"dataset_id": dataset_id, "cycle_date": cycle_date}
    dr_results = ufh.get_request_with_json_resp_as_dict(
        url=url, payload=payload, connection_timeout=3, read_timeout=20
    )
    logging.info(
        "Finished applying data reconciliation rules on the dataset %s",
        dataset_id,
    )

    return dr_results


def run_data_lineage_task(workflow_id: str, cycle_date: str) -> list[dict]:
    logging.info(
        "Start capturing data lineage for the workflow %s", workflow_id
    )
    url = f"{os.environ['DF_SVC_BASE_URL']}:{os.environ['DF_DATA_LINEAGE_SVC_PORT']}/capture-relationships"
    payload = {"workflow_id": workflow_id, "cycle_date": cycle_date}
    dl_relationships = ufh.get_request_with_json_resp_as_dict(
        url=url, payload=payload, connection_timeout=3, read_timeout=10
    )
    logging.info(
        "Finished capturing data lineage for the workflow %s", workflow_id
    )

    return dl_relationships


def run_management_tasks(
    tasks: list[wf.ManagementTask], cycle_date: str
) -> list[dict]:
    mgmt_task_results = []
    for task in tasks:
        if task.name == "data quality":
            dq_results = run_data_quality_task(
                required_parameters=task.required_parameters,
                cycle_date=cycle_date,
            )
            mgmt_task_results += dq_results
        if task.name == "data quality ml":
            dqml_results = run_data_quality_ml_task(
                required_parameters=task.required_parameters,
                cycle_date=cycle_date,
            )
            mgmt_task_results += dqml_results
        if task.name == "data profile":
            dp_results = run_data_profile_task(
                required_parameters=task.required_parameters,
                cycle_date=cycle_date,
            )
            mgmt_task_results.append(dp_results)
        if task.name == "data reconciliation":
            dr_results = run_data_recon_task(
                required_parameters=task.required_parameters,
                cycle_date=cycle_date,
            )
            mgmt_task_results.append(dr_results)
    return mgmt_task_results
