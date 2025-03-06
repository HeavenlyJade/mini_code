import json
import datetime
import copy

from backend.app import create_app
import os


def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError("Type not serializable")


class LoadParameterRedis:

    def main(self):
        from backend.rtr.service import parameter_server, parameter_log_server
        from backend.extensions import redis as redis_client
        query_params = dict(area="Litho")
        query_data = parameter_server.repo.query_data(**query_params)
        for i in query_data:

            DETAILS = json.loads(i.details)

            find_params = dict(param_id=i.id, need_total_count=False, context_dict={"key": 1}, context_set=DETAILS)

            new_list = []
            parameter = json.loads(i.parameter)
            parameter_list = [i["name"] for i in parameter]
            new_list.extend(DETAILS)
            new_list.extend(parameter_list)
            parameter_data, count_data = parameter_log_server._repo.find_data_join_table_query(find_params)
            for q in parameter_data:
                new_value = self.new_value_func(new_list, q)
                lodas_value = json.dumps([new_value])
                unique_representation = self.combined_keys(DETAILS, data=q, params_id=str(i.id))
                redis_client.set_key_with_expiration(unique_representation,
                                                     lodas_value)
                value = redis_client.client.get(unique_representation)

    def new_value_func(self, new_list, data: dict):
        re_data = {}
        for i in new_list:
            re_data[i] = data.get(i, "")
        return re_data

    def combined_keys(self, context_names, data, params_id: str):
        context_names_copy = copy.deepcopy(context_names)
        sorted_list = sorted(context_names_copy)

        combined_keys_values = ["official", params_id]

        for key in sorted_list:
            value = data.get(key)
            value = self.remove_trailing_zero(value)
            combined_keys_values.append(f"{key}:{value}")
        unique_representation = "_".join(combined_keys_values)
        return unique_representation

    @staticmethod
    def remove_trailing_zero(number: float):
        if not isinstance(number, float):
            return number
        if int(number) == number:
            return int(number)
        return number


if __name__ == '__main__':
    import time
    import platform

    os_name = platform.system()
    if os_name == 'Windows':
        os.chdir("../..")
    from backend.extensions import redis as redis_client

    app = create_app()
    app.app_context().push()
    redis_client.client.flushdb()
    LoadParameterRedis().main()

    #
