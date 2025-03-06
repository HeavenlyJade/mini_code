import json

from backend.app import create_app
from dataclasses import asdict
from collections import defaultdict
import os


def data_change(value):
    try:
        return float(value)
    except:
        return value


class FlowAnalysisTask:
    """ 策略分析任务"""

    def main(self):
        from backend.business.service import ama_service
        from backend.rtr.service import strategy_analysis_server

        self.add_strategy_analysis()
        strategy_items = self.get_strategy_analysis()
        flow_id_items = [i["flow_id"] for i in strategy_items]
        strategy_analysis_id_dict = {i["flow_id"]: {"id": i["id"],
                                                    "max_time": i["max_time"],
                                                    "avg_time": i["avg_time"],
                                                    "fail_runs": i["fail_runs"],
                                                    "total_runs": i["total_runs"]} for i in strategy_items}
        sub_lists = [flow_id_items[i:i + 100] for i in range(0, len(flow_id_items), 100)]
        flow_url = f'{ama_service.endpoint_url}/api/v1/tasks/strategy_analysis'
        for flow_id_list in sub_lists:
            flow_data = {i: {} for i in flow_id_list}
            for state in ["failed", "success"]:
                ama_params = {"flow_id_list": flow_id_list,
                              "state": state}
                ama_strategy_analysis_re = ama_service.post_req(url=flow_url, json=ama_params)
                data = ama_strategy_analysis_re["data"]

                for ama_strategy_analysis in data:
                    flow_id = ama_strategy_analysis["flow_id"]
                    total = ama_strategy_analysis["total"]
                    avg_time = ama_strategy_analysis["avg_time"]
                    max_time = ama_strategy_analysis["max_time"]
                    flow_data[flow_id][state] = {"total": total, "avg_time": avg_time, "max_time": max_time}

            for key, value in flow_data.items():
                if not value:
                    continue
                flow_se_data = strategy_analysis_id_dict[key]
                strategy_analysis_id = flow_se_data["id"]
                strategy_analysis_max_time = self.change_data_type(flow_se_data["max_time"])
                strategy_analysis_avg_time = self.change_data_type(flow_se_data["avg_time"])
                strategy_analysis_fail_runs = (flow_se_data["fail_runs"])
                strategy_analysis_total_runs = (flow_se_data["total_runs"])
                failed = value.get("failed", {})
                success = value.get("success", {})
                failed_total = failed.get("total", 0)
                success_total = success.get("total", 0)
                total_runs = failed_total + success_total
                suce_avg_time = success.get("avg_time")
                suce_max_time = success.get("max_time")
                suce_avg_time = self.change_data_type(suce_avg_time)
                suce_max_time = self.change_data_type(suce_max_time)
                if strategy_analysis_fail_runs == failed_total and strategy_analysis_max_time == suce_max_time \
                    and strategy_analysis_avg_time == suce_avg_time and strategy_analysis_total_runs == total_runs:
                    continue
                update_params = {"max_time": suce_max_time,
                                 "avg_time": suce_avg_time,
                                 "fail_runs": failed_total,
                                 "total_runs": total_runs
                                 }
                strategy_analysis_server.bulk_update_data(table_id=strategy_analysis_id,
                                                          update_data=update_params)

    def get_strategy_analysis(self):
        from backend.rtr.service import strategy_analysis_server
        data = strategy_analysis_server.find_data(kwargs={})
        items = data["items"]
        return items

    @staticmethod
    def change_data_type(data):
        try:
            if isinstance(data, str):
                data = float(data)
        except:
            pass
        return data

    def add_strategy_analysis(self):
        from backend.rtr.service import strategy_analysis_server
        data = strategy_analysis_server.find_join_strategy_version({})
        add_strategy_analysis = []
        for i in data:
            strategy_analysis = asdict(i[0]) if i[0] else i[0]
            strategy_version = asdict(i[-1])
            if strategy_analysis is None:
                strategy_id = strategy_version["strategy_id"]
                flow_id = strategy_version["flow_id"]
                version_number = strategy_version["version_number"]
                add_strategy_analysis.append({"strategy_id": strategy_id,
                                              "flow_id": flow_id,
                                              "version_number": version_number})
        if add_strategy_analysis:
            strategy_analysis_server.bulk_add_data(add_strategy_analysis)


class ControllerAnalysisTask:
    """ 控制系统分析的任务"""

    @property
    def controller_server_repo(self):
        from backend.rtr.service import control_system_server
        return control_system_server

    def main(self):
        items = self.get_controller_list()
        self.update_analysis(items)
        self.update_target(items)

    def update_target(self, items):
        from backend.rtr.service import control_system_log_server, controller_analysis_server

        for i in items:
            control_system_id = i.id
            log_data = control_system_log_server._repo.find_all(**{"control_system_id": control_system_id})
            lst = self.process_log_data(log_data)
            avg_dict = self.average_dicts(lst)
            diff_value_list, per_list, diff_target_value_list, per_target_list = self.extract_lists(avg_dict)

            update_control_system_analysis_data = {"dev_output": json.dumps(diff_value_list),
                                                   "dev_output_per": json.dumps(per_list),
                                                   "dev_target": json.dumps(diff_target_value_list),
                                                   "dev_target_per": json.dumps(per_target_list),
                                                   "control_system_id": control_system_id}
            controller_analysis_server.repo.add_or_update_data(kwargs=update_control_system_analysis_data)

    @staticmethod
    def extract_lists(data):
        diff_value_list = []
        per_list = []
        diff_target_value_list = []
        per_target_list = []

        for key, subdict in data.items():
            diff_value = subdict.get('diff_value', None)
            per_value = subdict.get('per', None)
            diff_target_value = subdict.get('diff_target_value', None)
            per_target = subdict.get('per_target', None)

            diff_value_list.append({key: diff_value})
            per_list.append({key: per_value})
            diff_target_value_list.append({key: diff_target_value})
            per_target_list.append({key: per_target})
        return diff_value_list, per_list, diff_target_value_list, per_target_list

    @staticmethod
    def process_log_data(log_data):
        lst = []
        for i in log_data:
            content = i.content
            system_field = i.system_field
            arithmetic_params = i.arithmetic_params
            system_field: dict = json.loads(system_field) if isinstance(system_field, str) else system_field
            if not system_field:
                system_field = {}
            output_y: dict = content.get("output_y", {})
            predicted_output: dict = system_field.get("PredictedOutput", {})
            target: dict = system_field.get("Target", {})
            key_value_dict = {i: {} for i in output_y.keys()}
            for key in output_y.keys():
                pre_value = output_y.get(key)
                real_value = predicted_output.get(key)
                target_value = target.get(f"{key}_t")
                pre_value = data_change(pre_value)
                real_value = data_change(real_value)
                target_value = data_change(target_value)
                if isinstance(pre_value, (float, int)) and isinstance(real_value, (float, int)):
                    diff_value = real_value - pre_value
                    per = diff_value / real_value
                else:
                    diff_value = None
                    per = None
                if isinstance(target_value, (float, int)) and isinstance(pre_value, (float, int)):
                    diff_target_value = pre_value - target_value
                    per_target = diff_target_value / pre_value
                else:
                    diff_target_value = None
                    per_target = None
                key_value_dict[key] = {
                    "diff_value": diff_value,
                    "per": per,
                    "diff_target_value": diff_target_value,
                    "per_target": per_target
                }
            lst.append(key_value_dict)
        return lst

    @staticmethod
    def average_dicts(lst):
        sum_dict = defaultdict(lambda: defaultdict(float))
        count_dict = defaultdict(lambda: defaultdict(int))

        for item in lst:

            for key, subdict in item.items():
                for subkey, val in subdict.items():
                    if val is not None:
                        sum_dict[key][subkey] += val
                        count_dict[key][subkey] += 1

        avg_dict = defaultdict(dict)
        for key, subdict in sum_dict.items():
            for subkey, sum_val in subdict.items():
                avg_val = sum_val / count_dict[key][subkey]
                avg_dict[key][subkey] = round(avg_val, 3)
        return avg_dict

    def update_analysis(self, items):
        from backend.business.service import ama_service
        from backend.rtr.service import controller_analysis_server
        flow_history_url = f'{ama_service.endpoint_url}/api/v1/tasks/history_analysis'
        id_list = [i.id for i in items]
        state_est = "state_est"
        update_params = {"control_system_id_list": id_list,
                         "state_est": state_est
                         }
        ama_strategy_analysis_re = ama_service.post_req(url=flow_history_url, json=update_params)
        items = ama_strategy_analysis_re["items"]
        if not items:
            return
        for control_system_id, value in items.items():
            if not value:
                continue

            fail_runs = 0
            success_runs = 0
            for i in value:
                avg_time = i["avg_time"]
                state = i["state"]
                sum_count = i["sum_count"]
                avg_time = FlowAnalysisTask.change_data_type(avg_time)
                sum_count = FlowAnalysisTask.change_data_type(sum_count)
                if state == "failed" and sum_count is not None:
                    fail_runs = sum_count
                elif state == "success" and sum_count is not None:
                    success_runs = sum_count
            total_runs = fail_runs + success_runs
            update_control_system_analysis_data = {"fail_runs": fail_runs, "total_runs": total_runs,
                                                   "control_system_id": control_system_id}
            controller_analysis_server.repo.add_or_update_data(kwargs=update_control_system_analysis_data)

    def get_controller_list(self):
        controller_data = self.controller_server_repo.list({})
        items = controller_data["items"]
        return items


if __name__ == '__main__':
    import time
    import platform

    os_name = platform.system()
    if os_name == 'Windows':
        os.chdir("../..")

    app = create_app()
    app.app_context().push()
    try:
        FlowAnalysisTask().main()
    except  Exception as e:
        print(f"FlowAnalysisTask:{e}")
    try:
        ControllerAnalysisTask().main()
    except  Exception as e:
        print(f"ControllerAnalysisTask:{e}")
    time.sleep(3000)
