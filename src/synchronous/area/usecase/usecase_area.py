import asyncio

from math import ceil

import requests

from configs.config import Config
from src.shared import usecase as uc
from src.shared.response import response_object as ro
from src.shared.response.response_object import CommonResponse
from src.synchronous.area.serializers.area_serializers import AllAreaBaseSchema


class ListAllAreaUsecase(uc.UseCaseSync):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_objects):
        try:
            data = self.repo.area.get_all_area(request_objects)
            total = self.repo.area.get_total_area(request_objects)
            data_plankton = self.repo.plankton.get_variant('/variants?noCache=true')
            plankton_include = self.repo.plankton.get_variant('/variants?include=product,offers&page[number]=1&page[size]=100&filter[status]=published&channel=b2b&noCache=true')

            total_page = ceil(total / request_objects.limit)

            serializer_area = AllAreaBaseSchema().dump(data, many=True)

            plankton_tmp = []
            for i, row in enumerate(data_plankton.get('data')):
                if i == 3:
                    break
                else:
                    plankton_tmp.append(
                        {
                            'skuNo': row.get('skuNo'),
                            'fullname': row.get('fullname')
                        }
                    )

            for i, data in enumerate(serializer_area):
                if i == 11:
                    break
                else:
                    data['plankton'] = plankton_tmp

            response = {
                'success': True,
                'code': Config.STATUS_CODES[Config.SUCCESS],
                'message': Config.SUCCESS.lower(),
                'meta': {
                    'page': request_objects.page,
                    'limit': request_objects.limit,
                    'totalRecords': total,
                    'totalPages': total_page,
                },
                'data': serializer_area
            }

            return ro.ResponseSuccess(response)

        except requests.Timeout:
            return CommonResponse.build_common_message("time out error", Config.SYSTEM_ERROR)

        except Exception as e:
            return CommonResponse.build_common_message(str(e), Config.SYSTEM_ERROR)


class ListAllOnlyAreaUsecase(uc.UseCaseSync):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_objects):
        try:
            data = self.repo.area.get_all_area(request_objects)
            total = self.repo.area.get_total_area(request_objects)

            total_page = ceil(total / request_objects.limit)

            serializer_area = AllAreaBaseSchema().dump(data, many=True)

            response = {
                'success': True,
                'code': Config.STATUS_CODES[Config.SUCCESS],
                'message': Config.SUCCESS.lower(),
                'meta': {
                    'page': request_objects.page,
                    'limit': request_objects.limit,
                    'totalRecords': total,
                    'totalPages': total_page,
                },
                'data': serializer_area
            }

            return ro.ResponseSuccess(response)

        except requests.Timeout:
            return CommonResponse.build_common_message("time out error", Config.SYSTEM_ERROR)

        except Exception as e:
            return CommonResponse.build_common_message(str(e), Config.SYSTEM_ERROR)
