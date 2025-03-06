import datetime
import random
from dataclasses import asdict

import factory
import typer

from backend.alarm.domain import Alarm
from backend.alarm.service import alarm_service
from backend.equipment.domain import (
    Chamber,
    ChamberRecord,
    ChamberState,
    EqpConnState,
    EqpProdMode,
    Equipment,
)
from backend.equipment.provider.redis_cli import api as redis_api
from backend.equipment.service import chamber_service, equipment_service
from backend.spot_checking.domain import SpotCheckingMoSource, SpotCheckingSetting
from backend.spot_checking.service import (
    spot_checking_mo_source_service,
    spot_checking_setting_service,
)
from kit.util import json as json_util

app = typer.Typer()


class EquipmentFactory(factory.Factory):
    class Meta:
        model = Equipment

    eqp_number = factory.Faker('uuid4')
    eqp_name = factory.Sequence(lambda n: f'ACTE{n + 1}')
    eqp_type = 'K123'
    eqp_mfr = 'IKAS'
    eqp_area = 'ETCH'
    eqp_comm_type = factory.Faker('random_element', elements=['IP', 'SECS GEM'])
    eqp_prod_mode = factory.Faker(
        'random_element', elements=EqpProdMode.comparison_map().keys()
    )
    eqp_conn_state = factory.Faker(
        'random_element', elements=EqpConnState.comparison_map().keys()
    )
    client_version = '0.1.0'
    eqp_ip = factory.Faker('ipv4')


class ChamberFactory(factory.Factory):
    class Meta:
        model = Chamber

    chamber_name = factory.Sequence(lambda n: f'K0{n + 1}')
    chamber_seq_number = factory.Sequence(lambda n: n + 1)
    chamber_state = factory.Faker(
        'random_element', elements=ChamberState.comparison_map().keys()
    )


class ChamberRecordFactory(factory.Factory):
    class Meta:
        model = ChamberRecord

    furnace_freq = factory.Faker('random_digit_not_null')
    recipe_number = factory.Faker('bothify', text='????-########')
    step_number = factory.Faker('random_element', elements=range(1, 11))
    start_time = factory.Faker('date_time_this_month')
    end_time = factory.LazyAttribute(
        lambda x: x.start_time + datetime.timedelta(random.randint(1, 3600 * 24))
    )


class AlarmRecordFactory(factory.Factory):
    class Meta:
        model = Alarm

    message = 'Alarm text.'
    alarm_time = factory.Faker('date_time_this_month')


class SpotCheckingSettingFactory(factory.Factory):
    class Meta:
        model = SpotCheckingSetting

    recipe_number = factory.Faker('bothify', text='????-########')
    start_time = factory.Faker('date_time_this_month')
    program_duration = factory.Faker('random_element', elements=range(1, 3600 * 24))
    end_time = factory.LazyAttribute(
        lambda x: x.start_time + datetime.timedelta(seconds=x.program_duration)
    )
    spot_checker = factory.Faker('first_name')
    check_time = factory.Faker('date_time_this_month')


class SpotCheckingMoSourceFactory(factory.Factory):
    class Meta:
        model = SpotCheckingMoSource

    mo_source_name = factory.Faker('bothify', text='????')
    furnace_consumption = factory.Faker(
        'pyfloat', positive=True, min_value=1, max_value=10
    )
    furnace_consume_upper_limit = factory.Faker(
        'pyfloat', positive=True, min_value=10, max_value=1000
    )
    furnace_consume_lower_limit = factory.Faker(
        'pyfloat', positive=True, max_value=1, min_value=0.01
    )


@app.command()
def create_dummy_equipments(e_qty: int = 10, c_qty: int = 4):
    """

    Args:
        e_qty: The qty of dummy equipments.
        c_qty:  The qty of dummy chambers per equipment.

    """
    from backend.app import create_app

    flask_app = create_app()
    equipments = equipment_service.repo.find_all()
    chambers = list()
    chamber_records = list()
    alarms = list()
    spot_checking_settings = list()
    spot_checking_mo_sources = list()
    for index, equipment in enumerate(equipments):
        # Faker chambers
        eqp_chambers = ChamberFactory.build_batch(c_qty, equipment_id=equipment.id)
        for idx, eqp_chamber in enumerate(eqp_chambers):
            eqp_chamber.id = c_qty * index + idx + 1
        chambers.extend(eqp_chambers)
        ChamberFactory.reset_sequence()
        for eqp_chamber in eqp_chambers:
            # Faker one chamber record per chamber.
            chamber_record = ChamberRecordFactory.build(chamber_id=eqp_chamber.id)
            chamber_records.append(chamber_record)
            # Faker one alarm message per chamber.
            alarm = AlarmRecordFactory.build(
                equipment_id=equipment.id,
                chamber_id=eqp_chamber.id,
            )
            alarms.append(alarm)
            # Faker one spot checking setting and mo-sources per furnace freq.
            for freq in range(1, 11):
                spot_checking_setting = SpotCheckingSettingFactory.build(
                    equipment_id=equipment.id,
                    chamber_id=eqp_chamber.id,
                    furnace_freq=freq,
                )
                spot_checking_settings.append(spot_checking_setting)
                spot_checking_mo_source = SpotCheckingMoSourceFactory.build(
                    equipment_id=equipment.id,
                    chamber_id=eqp_chamber.id,
                    furnace_freq=freq,
                )
                spot_checking_mo_sources.append(spot_checking_mo_source)

    with flask_app.app_context():
        equipment_service.create_many(equipments)
        chamber_service.create_many(chambers)
        spot_checking_setting_service.create_many(spot_checking_settings)
        spot_checking_mo_source_service.create_many(spot_checking_mo_sources)
        alarm_service.create_many(alarms)
        for chamber_record in chamber_records:
            redis_api.set_chamber_records(
                chamber_record.chamber_id, json_util.dumps(asdict(chamber_record))
            )


if __name__ == '__main__':
    typer.run(create_dummy_equipments)
