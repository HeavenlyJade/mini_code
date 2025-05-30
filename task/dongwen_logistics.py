#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物流订单轨迹自动更新定时任务

该脚本用于定时查询已发货的物流订单信息，并通过顺丰(SF)物流查询API
获取最新的物流轨迹，更新到订单物流信息表中。
"""


import datetime as dt
import requests
import logging
from loguru import logger
from task import celery
from celery.signals import worker_ready
from flask import current_app

# 设置日志


from kit.sf_api.api import SF

class LogisticsTrackingTask:
    """物流轨迹更新定时任务"""

    def __init__(self):
        """初始化任务"""
        self.app = current_app

        # 从配置中获取顺丰API凭证
        self.sf_client_code = self.app.config.get('SF_CLIENT_CODE')
        self.sf_check_word = self.app.config.get('SF_CHECK_WORD')

        # 初始化顺丰API客户端
        self.sf_client = SF(self.sf_client_code,  self.sf_check_word)

    def run(self):
        """运行任务"""
        logger.info("======开始执行物流轨迹更新任务======")
        # 获取所有需要更新的物流订单
        from backend.mini_core.repository import shop_order_logistics_sqla_repo
        data_args= {   'current_status': ['已发货','运送中'],'days': 7}
        logistics_orders = shop_order_logistics_sqla_repo.get_con_logistics(kwargs=data_args)
        logger.info(f"找到 {len(logistics_orders)} 个需要更新的物流订单")

        # 更新每个订单的物流信息
        from backend.mini_core.service import shop_order_logistics_service
        for logistics in logistics_orders:

            # 只处理顺丰快递
            if "顺丰" not in logistics.logistics_company and "SF" not in logistics.logistics_company.upper():
                logger.info(
                    f"跳过非顺丰物流订单: {logistics.order_no}, 物流公司: {logistics.logistics_company}")
                continue

            # 查询物流轨迹
            # 可以从订单中获取手机号后四位提高准确性
            phone_last_four = None
            if logistics.receiver_info:
                try:
                    receiver_info = logistics.receiver_info
                    phone = receiver_info.get("phone", "")
                    if phone and len(phone) >= 4:
                        phone_last_four = phone[-4:]
                except:
                    pass
            logistics_no= logistics.logistics_no
            order_result = self.sf_client.order.get_route_info(
                trackingNumber=logistics_no,
                checkPhoneNo=phone_last_four,)
            print(self.sf_client_code,self.sf_check_word,logistics_no,phone_last_four)

            routes = order_result.get("msgData", {}).get("routeResps", [{}])[0].get("routes", [])

            # if not routes:
            #     continue

            # 按时间排序（从新到旧）
            routes.sort(key=lambda x: x.get("acceptTime", ""), reverse=True)
            if not routes:
                continue
            # 获取最新节点
            latest_route = routes[0]

            # 准备新的轨迹数据以及当前状态
            new_route_items = []
            for route in routes:
                new_route_items.append({
                    "time": route.get("acceptTime", ""),
                    "status": f"{route.get('firstStatusName', '')}-{route.get('secondaryStatusName', '')}",
                    "location": route.get("acceptAddress", ""),
                    "remark": route.get("remark", "")
                })

            # 更新物流数据
            current_status = latest_route.get("firstStatusName", "运输中")
            current_location = latest_route.get("acceptAddress", "")
            current_accept_time = latest_route.get("acceptTime", "")
            logistics_route_data = logistics.logistics_route
            if logistics_route_data:
                logistics_cur_route = logistics_route_data[0]
                lo_time =logistics_cur_route["time"]
                if current_accept_time == lo_time:
                    logger.info(f"物流订单 {logistics.order_no} 的轨迹信息没有更新{current_accept_time},{lo_time}")
                    continue
            args = dict(route_info=new_route_items, current_status=current_status,
                        current_location=current_location, )
            if current_status == "已签收":
                receiving_time = latest_route.get("acceptTime", )
                args["receiving_time"] = receiving_time

            shop_order_logistics_sqla_repo.update_logistics_route(
                logistics.id,
                args=args)

            logger.info(f"成功更新物流订单 {logistics.order_no} 的轨迹信息")





@celery.task
def update_logistics_task():

    task = LogisticsTrackingTask()
    task.run()
    # task = LogisticsTrackingTask()
    # task.run()


@worker_ready.connect
def start_logistics_task(sender, **kwargs):
    logger.info("Worker 启动，立即执行一次物流轨迹更新任务")
    update_logistics_task.delay()

